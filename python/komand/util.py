import sys
import python_jsonschema_objects as pjs
import pprint
import copy

def default_for(prop):
    if not prop['type']:
        return ''

    if prop['type'] == 'object':
        return {} 

    if prop['type'] == 'string':
        return ''

    if prop['type'] == 'integer' or prop['type'] == 'number':
        return 0 

def sample(source):

    if not source:
        return {}

    schema = {
                'title': 'Example',
                'properties': {},
                'type': 'object',
                'required': [],
                }

    defaults = {}

    for key, prop in source['properties'].iteritems():
        prop = copy.copy(prop)
        defaults[key] = default_for(prop) 
        schema['properties'][key] = prop
        schema['required'].append(key)

    builder = pjs.ObjectBuilder(schema)
    ns = builder.build_classes()
    Obj = ns.Example
    o = Obj(**defaults)
    return o.as_dict()

def trace(exception):
    """Returns the trace from an exception"""
    return sys.exc_info()[2]

