#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import inv_argparse

list_commands = []
cl_or_cmd = inv_argparse.cl_or_cmd
_main_ = True



def regist_command(name: str, fun, dest: str = "", cl_or_cmd: int = 3) -> bool: 
    if not name:
        return False
    
    if not fun:
        return False
    
    global list_commands
    
    list_commands.append({
            'name': name, 
            'fun': fun,
            #'dest': dest
        })
    
    inv_argparse.add_help(name, dest, cl_or_cmd)
    
    return True


def add_arg_command(name_cmd: str, name: str, short: str, required: bool = False, dest: str = "", T = str) -> bool:
    cmd = get_command(name_cmd)
    
    if not cmd:
        return False
    
    if not cmd.get('arg', None):
        cmd['arg'] = []
        
    cmd['arg'].append({
        'name': name,
        #'name_short': short,
        #'required': required,
        #'dest': dest,
        #'type': T,
    })
    
    if required:
        dest += ' (обязательно)'
    
    inv_argparse.add_arg_help(name_cmd, name, short, required, dest, T)
    
    return True

def is_arg_command(name_cmd: str) -> bool:
    cmd = get_command(name_cmd)
    
    if not cmd:
        return False
    
    if not cmd.get('arg', False):
        return False
    
    return True
    

def send_command(text: str = None, s: bool = True,  cl: bool = False) -> str:
    
    if cl:
        print('>>> ', ( ('[' + (text if text else '') + ']') if s else ''), end='', sep='')
        in_text = str(input()).lower()
        
        if in_text:
            return in_text
            
        return text
    
    if not text:
        return ''
    
    return text.lower()


def get_command(is_command_name) -> dict:
    for cur_command in list_commands:
        command_name = cur_command.get('name', None)
        
        if not command_name:
            continue
        
        if is_command_name == command_name:
            return cur_command

    return None


def call_command(command_name: str, **args) -> dict:
    cmd = get_command(command_name)
    
    if not cmd:
        return {
            'return': None,
            'error': 1,
        }
    
    if not cmd.get('fun', None):
        return {
            'return': None,
            'error': 2,
        }
    
    return {
        'return': cmd['fun'](**args),
        'error': 0,
    }

def help_command(command_name: str = None, not_cl: bool = False) -> str:
    if command_name:
        return inv_argparse.parse_args(command_name + ' -h', not_cl)
    
    else:
        return inv_argparse.parse_args('-h', not_cl)


def parse_call_command(command_line: str=None, not_cmd: bool = False) -> dict:
    return vars(inv_argparse.parse_args(command_line, not_cmd))