from os import path
from typing import Tuple
import json
import yaml
import re

def load_data(file_name: str, class_type: str):
    data = load_data_file(file_name)
    if data == None:
        return
    return strict_dict_to_class(data, class_type)

def load_data_file(file_name: str, default = None, format='auto') -> dict | str | None:
    if not path.exists(file_name) or not path.isfile(file_name):
        return default

    with open(file_name, encoding='utf-8') as file:
        text = file.read()

    _, ext = path.splitext(file_name)
    if ext == ".json" or format == 'json':
        if format != 'auto' and format != 'json':
            raise Exception(f'File extension does not match specified format. File={file_name}, format={format}')
        return json.loads(text)
    if ext == ".yaml" or ext == ".yml" or format == 'yml' or format == 'yaml':
        if format != 'auto' and format != 'yaml' and format != 'yml':
            raise Exception(f'File extension does not match specified format. File={file_name}, format={format}')
        return yaml.safe_load(text)
    
    return text

def save_data_file(data: dict | list, file_name: str, format: str = 'yaml'):
    with open(file_name, "w") as file:
        if format == 'yaml':
            # TODO
            #yaml.safe_dump(data, file, sort_keys=False)
            yaml.safe_dump(json.loads(json.dumps(data)), file, sort_keys=False)
        elif format == 'json':
            json.dump(data, file, indent=4, default=vars)
        else:
            raise Exception("Invalid format: " + format)
        
def strict_dict_to_class(data: dict, class_type):

    actual_keys = set(data.keys())
    declared_keys = set(class_type.__annotations__.keys())
    unexpected_fields = actual_keys - declared_keys
    if unexpected_fields:
        raise ValueError(f"Unexpected fields: {unexpected_fields} while deserializing class {class_type.__name__}")
    
    mandatory_keys = set()
    for k in declared_keys:
        if not hasattr(class_type, k):
            mandatory_keys.add(k)
    missing_fields = mandatory_keys - actual_keys
    if missing_fields:
        raise ValueError(f"Missing fields: {class_type.__name__}.{missing_fields}")

    inst = class_type()

    for field_name, field_type in class_type.__annotations__.items():
        value = data.get(field_name)
        if isinstance(value, field_type):
            setattr(inst, field_name, value)
            continue
        if isinstance(value, dict):
            value = strict_dict_to_class(value, field_type)
            setattr(inst, field_name, value)
            continue
        raise ValueError(f"Field '{class_type.__name__}.{field_name}' has an incorrect type. Declared: {field_type}, actual: {type(value)}")
    return inst

def deep_update_object_value(obj, fn_change, _current_path: str = ""):

    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = deep_update_object_value(obj[i], fn_change, _current_path + f"[{i}]")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            item_path = _current_path + '.' + k if _current_path else k
            obj[k] = deep_update_object_value(v, fn_change, item_path)
    else:
        obj = fn_change(_current_path, obj)
    return obj

def deep_apply_defaults(to_obj: dict, from_obj: dict) -> bool:
    """If a property in to_obj is empty, use the value from from_obj if the same property is not empty"""
    if not from_obj:
        return
    changed = False
    for k, v in to_obj.items():
        v1 = from_obj.get(k)
        if not v1:
            continue
        if not v:
            to_obj[k] = v1
            changed = True
            continue
        if isinstance(v, dict):
            if deep_apply_defaults(v, v1):
                changed = True
    return changed

def deep_get_attr(obj: dict, path: str):
    parts = path.split('.')
    for k in parts:
        try:
            obj = _get_obj_attr(obj, k)
        except KeyError:
            raise Exception("Property path not found: " + path)
    return obj

def deep_set_attr(obj: dict, path: str, value):
    parts = path.split('.')
    k = None
    try:
        for i in range(len(parts)):
            k = parts[i]
            obj = _get_obj_attr(obj, k)

            if i == len(parts) - 2:
                # found the one before the leaf.
                _set_obj_attr(obj, parts[i + 1], value)
                break
        return obj
    except (KeyError, TypeError, IndexError) as e:
        raise Exception(f"Property path error: {path}. Cause={e}, current={k}, i={i}")

def _get_obj_attr(o, k):

    name, array_index = _parse_array_property_name(k)

    if isinstance(o, dict):
        ret = o[name]
    else:
        ret = getattr(o, name)

    if array_index != None:
        ret = ret[array_index]

    return ret

def _set_obj_attr(o, k, v):
    name, array_index = _parse_array_property_name(k)
    if isinstance(o, dict):
        if array_index is None:
            o[name] = v
        else:
            o[name][array_index] = v
    else:
        if array_index is None:
            setattr(o, name, v)
        else:
            array_elem = getattr(o, name)
            array_elem[array_index] = v

_array_index_matcher = re.compile('(.+)\[(\d+)\]')
def _parse_array_property_name(k: str) -> Tuple[str, int]:
    m = _array_index_matcher.match(k)
    if m:
        return m.group(1), int(m.group(2))
    return k, None

def deep_iterate(obj, fn_on_value):
    if isinstance(obj, list) or isinstance(obj, set):
        for v in obj:
            deep_iterate(v, fn_on_value)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            deep_iterate(v, fn_on_value)
    else:
        fn_on_value(obj)

def deep_find_variables(obj):
    collector = set()
    def fn_on_value(v):
        m = _pattern_var.match(v)
        if m:
            collector.add(m.group(1))
    deep_iterate(obj, fn_on_value)
    return collector

def process_variables(obj: dict, fn_get_var = None):
    if fn_get_var == None:
        def _fn_get_var(name):
            try:
                return deep_get_attr(obj, name), True
            except:
                return None, False
        fn_get_var = _fn_get_var

    total_changed = {}
    while True:
        ret = _process_variables_impl(obj, fn_get_var)
        total_changed.update(ret['changed'])
        if not ret['changed']:
            return {
                'data': ret['data'],
                'changed': total_changed,
                'pending': ret['pending'],
            }

_pattern_var = re.compile('.*?\$\{(.+?)\}.*')
def _process_variables_impl(obj: dict, fn_get_var = None):
    changed = {}
    pending = {}

    def fn_change(path, v):
        if not isinstance(v, str):
            return v
        
        m = _pattern_var.match(v)
        if not m:
            return v
        var_name = m.group(1)
        replacement, found = fn_get_var(var_name)
        if not found:
            pending[path] = var_name
            return v
        if isinstance(replacement, str):
            changed[path] = var_name
            return v.replace('${' + var_name + '}', replacement)
        # replacement is an object. Make sure this var is the entire value.
        if len(v) != len(var_name) + 3:
            raise Exception(f"Invalid replacing variable with object. attr_path={path}, var_name={var_name}, replacement={str(replacement)}")
        changed[path] = var_name
        return replacement  #replace the entire value using the new value.
    
    data = deep_update_object_value(obj, fn_change)
    return {
        'changed': changed,
        'pending': pending,
        'data': data
    }

def to_json(o) -> str:
    class SetEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, set):
                return list(obj)
            return json.JSONEncoder.default(self, obj)
    return json.dumps(o, cls=SetEncoder, indent=4)