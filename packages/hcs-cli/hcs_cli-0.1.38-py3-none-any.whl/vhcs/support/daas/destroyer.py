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

import traceback
import subprocess
import sys

from vhcs.plan.provider.azure import _az_facade
from . import helper
from vhcs.common.ctxp import context, panic
from vhcs.service import admin

tenant_request: str = None
runtime = None

def destroy(req: dict):
    
    global tenant_request, runtime
    tenant_request = req

    ctx_name = 'daas-runtime-' + tenant_request['deploymentId']
    runtime = context.get(ctx_name, default={})

    try:
        helper.prep_az_cli(tenant_request)
        _delete_template()

        _delete_subnet()
        _delete_nsg()
        _delete_resource_group()
    except subprocess.CalledProcessError as e:
        return e
    except:
        raise
    finally:
        context.set(ctx_name, runtime)

def _res_name():
    return 'titan-lite-' + tenant_request['deploymentId']


label_deleting   = '[Deleting ]'
label_deleted    = '[Deleted  ]'
label_error      = '[Error    ]'
label_not_found  = '[Not found]'

def _delete(type, name, impl):
    label = type + ": " + name
    print(label_deleting, label)
    try:
        ret = impl()
        if ret == False:
            print(label_not_found, label)
        else:
            print(label_deleted, label)
    except:
        print(label_error, label)
        raise
    

def _delete_template():
    if runtime.template_ret:
        id = runtime.template_ret['id']
    else:
        # find by name
        # TODO
        search = f"name $eq {_res_name()}"
        templates = admin.template.list(search=search, limit=1)
        if templates:
            id = templates[0]['id']
        else:
            id = None
    
    if id:
        def impl():
            admin.template.delete(id, force=True)
            admin.template.wait_for_template_deleted(id)
            del runtime.template_ret
            return True
        _delete("template", id, impl)
    else:
        print(label_not_found, "template not found:", _res_name())
    

def _delete_resource_group():
    rg_name = _res_name()
    def impl():
        return _az_facade.delete_resource_group(name=rg_name)
    _delete("resource group", rg_name, impl)
    

def _delete_subnet():
    if runtime.subnet:
        id = runtime.subnet['id']
        def impl():
            ret = _az_facade.delete_subnet_by_id(id)
            del runtime.subnet
            return ret
        _delete("subnet", id, impl)
    else:
        if not runtime.vnet:
            vnet = _az_facade.get_vnet(tenant_request['network']['vNetId'])
            runtime.vnet = vnet
            runtime.location = vnet['location']
        rg_name = runtime.vnet['resourceGroup']
        vnet_name = runtime.vnet['name']
        subnet_name = _res_name()

        def impl():
            return _az_facade.delete_subnet(rg_name, vnet_name, subnet_name)
        _delete("subnet", f"{rg_name}/{vnet_name}/{subnet_name}", impl)
        
def _delete_nsg():
    if runtime.nsg:
        id = runtime.nsg['id']
        def impl():
            ret = _az_facade.delete_nsg_by_id(id)
            del runtime.nsg
            return ret
        _delete("NSG", id, impl)
    else:
        vnet = runtime.vnet
        if not vnet:
            vnet = _az_facade.get_vnet(tenant_request['network']['vNetId'])
            runtime.vnet = vnet
            runtime.location = vnet['location']
        rg_name = vnet['resourceGroup']
        nsg_name = _res_name()

        def impl():
            return _az_facade.delete_nsg(rg_name, nsg_name)
        _delete("NSG", f"{rg_name}/{nsg_name}", impl)

