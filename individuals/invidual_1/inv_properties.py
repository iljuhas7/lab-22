#!/usr/bin/env python3
# -*- coding: utf-8 -*-

version = {
    'release': '0.0.1'
}

file = {
    "json": {
        'name': 'inv_1.json',
    },

    "sqlite3": {
        'name': 'inv_1.db',
    }
}

default = {
    "file": file["sqlite3"]
}

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "number": {"type": "number"},
        "z": {"type": "number"}
    }
}
