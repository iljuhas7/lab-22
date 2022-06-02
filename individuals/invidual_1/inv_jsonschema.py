#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jsonschema
import inv_properties

def test(obj: object) -> bool:
    try:       
        jsonschema.validate(instance=obj, schema=inv_properties.schema)
    except jsonschema.ValidationError:
        return False;
    return True;

def test_msg(obj: object) -> str:
    try:
        jsonschema.validate(instance=obj, schema=inv_properties.schema)
    except jsonschema.ValidationError as err:
        return err.message;
    return "ok";
    
