"""
Copyright 2023-2023 VMware Inc.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import threading
import time
from subprocess import CalledProcessError
from copy import deepcopy
import vhcs.common.util as util
from . import helper
from . import dag
from .helper import PlanException
from importlib import import_module

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def deploy(data: dict, resource_name: str = None, concurrency: int = 4):
    #data = helper.load_files(files)
    blueprint, pending = helper.process_template(data)

    deployment_id = blueprint['deploymentId']
    state_file = deployment_id + '.state.yml'
    prev = _load_state(state_file)
    state = {'pending': pending}
    state.update(blueprint)
    state.update(prev)
    state['log']['deploy'] = []    # clear log

    def process_resource(name: str, res_data: dict):
        if name == 'defaults':
            return
        if res_data.get('type'):    #provider
            return
        
        _deploy_res(res_data, state)
        _resolve_pending_keys(blueprint, state, name)
        if resource_name and name == resource_name:
            return False

    try:
        dag.process_blueprint(blueprint, process_resource, concurrency)
    except CalledProcessError as e:
        raise PlanException(str(e))
    finally:
        util.save_data_file(state, state_file)

def _load_state(state_file):
    state = util.load_data_file(state_file, default={})
    if 'output' not in state:
        state['output'] = {}
    if 'destroy_output' not in state:
        state['destroy_output'] = {}
    if 'log' not in state:
        state['log'] = {}
    exec_log = state['log']
    if 'deploy' not in exec_log:
        exec_log['deploy'] = []
    if 'destroy' not in exec_log:
        exec_log['destroy'] = []
    return state

def _deploy_res(res, state):
    kind = res['kind']
    name = res['name']
    handler = _get_resource_handler(kind, state)

    def add_log(action: str, details = None):
        labels = {
            'start': '[+ ]',
            'success': '[ok]',
            'error': '[x ]'
        }
        log.info(f'{labels[action]} {kind}:{name}')
        entry = {
            'name': name,
            'time': time.time(),
            'action': action
        }
        if details:
            entry['details'] = str(details)
        state['log']['deploy'].append(entry)

    add_log('start')
    
    data = res.get('data', {})
    if data:
        _assert_all_vars_resolved(data, name)
        data = deepcopy(data)
    
    try:
        output = handler.deploy(data)
    except Exception as e:
        add_log('error', str(e))
        log.warning('Plugin "%s:%s" failed.', kind, name)
        log.warning('Dump data: %s', util.to_json(data))
        raise
    state['output'][name] = deepcopy(output)
    add_log('success')

def _resolve_pending_keys(blueprint, state, resource_name):
    prefix = resource_name + "."
    for attr_path, var_name in state['pending'].items():
        if not var_name.startswith(prefix):
            continue
        # found a key to solve
        try:
            value = util.deep_get_attr(state, "output." + var_name)
        except:
            log.warn('output.%s: %s', resource_name, util.to_json(state['output'][resource_name]))
            raise PlanException(f"Plugin error: plugin output '{var_name}' does not exist in the output of resource '{resource_name}', which is required by key path '{attr_path}'")
        
        # update that key
        v = util.deep_get_attr(blueprint, attr_path)
        if isinstance(value, str):
            v = v.replace('${' + var_name + '}', value)
        else:
            # replacement is an object. Make sure this var is the entire value.
            if len(v) != len(var_name) + 3:
                raise PlanException(f"Invalid replacing variable with object. attr_path={attr_path}, var_name={var_name}, replacement={str(value)}")
            v = value
        log.debug('Resolved. %s: %s -> %s', attr_path, var_name, v)
        util.deep_set_attr(blueprint, attr_path, v)

def _assert_all_vars_resolved(data, name):
    def fn_on_value(path, value):
        if isinstance(value, str) and value.find('${') >= 0:
            log.error('Dump plugin "%s" input: %s', name, util.to_json(data))
            raise PlanException(f"Unresolved variable '{path}' for plugin '{name}'. Value={value}")
        return value
    util.deep_update_object_value(data, fn_on_value)

_providers = {}
_provider_lock = threading.Lock()
def _get_resource_handler(kind: str, state: dict):
    provider_type, res_handler_type = kind.split('/')
    res_handler_type = res_handler_type.replace('-', '_')
    # Ensure provider initialized
    with _provider_lock:
        if not provider_type in _providers:
            provider = import_module("vhcs.plan.provider." + provider_type)
            # Get provider data
            filter_by_type = lambda m: m['type'] == provider_type
            providers = state.get('providers', {})
            meta = next(filter(filter_by_type, providers), None)
            data = meta.get('data') if meta else None
            if data:
                _assert_all_vars_resolved(data, provider_type)
            log.info("[. ] Provider: %s", provider_type)
            state['output'][provider_type] = provider.prepare(data)
            log.info("[ok] Provider: %s", provider_type)
            _providers[provider_type] = 1

    module_name = f"vhcs.plan.provider.{provider_type}.{res_handler_type}"
    return import_module(module_name)

def _destroy_res(res, state):
    
    kind = res['kind']
    name = res['name']

    def add_log(action: str, details = None):
        labels = {
            'start': '[- ]',
            'success': '[ok]',
            'error': '[x ]'
        }
        log.info(f'{labels[action]} {kind}:{name}')
        entry = {
            'name': name,
            'time': time.time(),
            'action': action
        }
        if details:
            entry['details'] = str(details)
        state['log']['destroy'].append(entry)
    
    add_log('start')
    
    data = None
    previous_output = None
    try:
        handler = _get_resource_handler(kind, state)

        data = res.get('data', {})
        if data:
            _assert_all_vars_resolved(data, name)
            data = deepcopy(data)
        previous_output = state['output'].get(name, {})
        if previous_output:
            previous_output = deepcopy(previous_output)

        ret = handler.destroy(data, previous_output)
    except Exception as e:
        add_log('error', e)
        log.warning('Plugin "%s:%s" failed.', kind, name)
        if data:
            log.warning('Dump data: %s', util.to_json(data))
        if previous_output:
            log.warning('Dump prev: %s', util.to_json(previous_output))
        raise
    state['destroy_output'][name] = deepcopy(ret)
    add_log('success')

def _deployed(state, resource_name: str):
    for i in state['log']['deploy']:
        if i['name'] == resource_name:
            return True

def destroy(data, resource_name: str = None, concurrency: int = 4):
    blueprint, pending = helper.process_template(data)
    deployment_id = blueprint['deploymentId']
    state_file = deployment_id + '.state.yml'
    prev = _load_state(state_file)
    state = {}
    state.update(blueprint)
    state.update(prev)
    state['log']['destroy'] = []    # clear log

    try:
        reversed_resources = list(state['resources'])
        reversed_resources.reverse()
        for res in reversed_resources:
            name = res['name']

            if not _deployed(state, name):
                continue

            _destroy_res(res, state)
            if resource_name and resource_name == res['name']:
                break

    except CalledProcessError as e:
        raise PlanException(str(e))
    finally:
        util.save_data_file(state, state_file)

