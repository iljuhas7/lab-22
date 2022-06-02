#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import inv_properties

parsers = {}
cl_or_cmd = {'none': 0, 'cmd': 1, 'cl': 2, 'any': 3}


_main_ = True

def add_help(name: str, desc: str, cl_or_cmd: int = 3) -> bool: 
    global parsers
    
    if not name:
        return False
    
    if parsers['cmd'].get(name, None):
        return False
    
    if cl_or_cmd & 1:
        parsers['cmd'][name] = parsers['sub_command'].add_parser(
            name,
            parents=[parsers['file']],
            help=desc
        )

    if cl_or_cmd & 2:
        parsers['cl'][name] = parsers['sub_console'].add_parser(
            name,
            parents=[parsers['file']],
            help=desc
        )

def get_help(name: str) -> object:
    global parsers
    
    if not name:
        return None
    
    return parsers['cmd'].get(name, None)
    


def add_arg_help(name_help: str, name: str, short: str, required: bool = False, dest: str = '', t: type = str) -> bool:
    global parsers
    
    if not name_help:
        return False
    
    if not name:
        return False
    
    if not short:
        return False
    
    sel_help = parsers['cmd'].get(name_help, None)
    
    if not sel_help:
        return False
    
    sel_help.add_argument(
        "-" + short,
        "--" + name,
        required = required,
        help = dest,
        type = t,
        action="store"
    )

    sel_help = parsers['cl'].get(name_help, None)

    if sel_help:
        sel_help.add_argument(
            "-" + short,
            "--" + name,
            required = required,
            help = dest,
            type = t,
            action="store"
        )


def parse_args(command_line: str=None, not_cmd: bool = False) -> argparse.Namespace:
    global parsers
    
    if not command_line:
        command_line = ''

    try:
        # Выполнить разбор аргументов командной строки.
        p = parsers[('console' if not_cmd else 'command')].parse_known_args(command_line.split())
        
        if len(p[1]):
            print("Не найден параметр:", p[1])
            
        return p[0]
    
    except SystemExit:
        return parsers[('console' if not_cmd else 'command')].parse_known_args('')[0]


if _main_:
    _main_ = False
    
    # Создать родительский парсер для определения имени файла.
    parsers['file'] = argparse.ArgumentParser(add_help=False)
    parsers['file'].add_argument(
        "filename",
        action="store",
        nargs='?',
        default=inv_properties.default['file']['name'],
        type=str,
        help="Имя файла"
    )

    # Создать основной парсер командной строки.
    parsers['command'] = argparse.ArgumentParser("command", )
    parsers['command'].add_argument(
        "-v",
        "--version",
        action="version",
        version="version: " + inv_properties.version.get('release', '0.0.0')
    )
    
    parsers['console'] = argparse.ArgumentParser("console")
    parsers['console'].add_argument(
        "-v",
        "--version",
        action="version",
        version="version: " + inv_properties.version.get('release', '0.0.0')
    )
    
    parsers['sub_command'] = parsers['command'].add_subparsers(dest="command",)
    parsers['sub_console'] = parsers['console'].add_subparsers(dest="command")
    parsers['cmd'] = {}
    parsers['cl'] = {}
    
    init_main=True