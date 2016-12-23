"""generate Json from Arguments and Schema"""
import copy
import json

def model_factory(schema, args):
    """generate copy of schema with new values in args"""
    schema = json.loads(copy.deepcopy(schema))
    for key in schema:
        if key in args:
            schema[key] = args[key]
    return schema
