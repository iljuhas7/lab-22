#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os

is_connect: bool = False
memory_sql3: sqlite3.Connection = None;


def gen_create(table_name: str, **typeOrName: type) -> str:  # Создать
    text = "CREATE TABLE " + table_name + "(\n\t"
    text += "ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\n"

    ltext = []

    for key, value in typeOrName.items():
        ttext = "\t" + key + " "

        if value == int:
            ttext += "INTEGER"

        elif ttext == float:
            ttext += "REAL"

        elif value == str:
            ttext += "TEXT"

        else:
            ttext += "TEXT"

        ltext.append(ttext)

    text += ",\n".join(ltext)
    text += "\n);"

    return text


def gen_insert(table_name: str, *typeOrName) -> str:  # Вставка строк
    text = "INSERT INTO " + table_name + " VALUES ("
    text += 'NULL, '
    text += ', '.join(["'" + value + "'" if type(value) ==
                      str else str(value) for value in typeOrName])
    text += ");"

    return text


def gen_select(select: str, frm: str = None, where: str = None) -> str:  # Выборка
    return "SELECT " + select + \
        (" FROM " + frm if frm else "") + \
        (" WHERE " + where if where else "") + ";"


def gen_update(table_name: str, vset: dict, where: dict = None) -> str:  # Обновление
    return "UPDATE " + table_name + \
        " SET " + ", ".join([key + ' = ' + gen_types(value)
                             for key, value in vset.items()]) + \
        ((" WHERE " + ", ".join([key + ' = ' + gen_types(value)
         for key, value in where.items()])) if where else "") + ";"
    pass


def gen_delete(table_name: str, **where) -> str:  # Удаление
    return "DELETE FROM " + table_name + \
        ((" WHERE " + ", ".join([key + ' = ' + gen_types(value)
         for key, value in where.items()])) if where else "") + ";"


def gen_types(val: any) -> str:
    if type(val) == str and (len(str.split(val, " ")) == 1):
        return '\'' + val + '\''
    else:
        return str(val)

    pass


def connect_memory() -> sqlite3.Connection:
    global memory_sql3, is_connect;
    
    if not is_connect:
        memory_sql3 = connect(":memory:")
        
    is_connect = not (memory_sql3 == None)
        
    return memory_sql3


def disconnect_memory() -> None:
    global memory_sql3, is_connect;
    
    if is_connect:
        disconnect(memory_sql3)
        is_connect = False

def save(file_path: str) -> None:
    global memory_sql3, is_connect;
    
    if( is_connect ):
        con = connect(file_path)
        memory_sql3.backup(con)
        con.close()
    else:
        pass

def laod(file_path: str) -> None:
    global memory_sql3, is_connect;
    
    if( is_connect and os.path.exists(file_path) ):
        con = connect(file_path)
        con.backup(memory_sql3)
        con.close()
    else:
        pass

def connect(file_path: str, autoclose: bool = False) -> sqlite3.Connection:
    try:
        con = sqlite3.connect(file_path)
        return con

    except sqlite3.Error:
        print(sqlite3.Error)

    finally:
        if autoclose:
            con.close()

    return None


def disconnect(con: sqlite3.Connection) -> None:
    con.close()


def create(con: sqlite3.Connection, table_name: str, **args) -> None:
    if not table_name:
        return None
    
    cursor_obj = con.cursor()
    cursor_obj.execute(gen_create(table_name, **args))
    con.commit()


def add(con: sqlite3.Connection, table_name: str, *args) -> None:
    if not table_name:
        return None
    
    cursor_obj = con.cursor()
    cursor_obj.execute(gen_insert(table_name, *args))
    con.commit()


def get(con: sqlite3.Connection, select: str, frm: str = None, where: str = None) -> any:
    if not select:
        return None

    try:
        cursor_obj = con.cursor()
        cursor_obj.execute(gen_select(select, frm, where))
        lget = cursor_obj.fetchall()
        
        if(len(lget)):
            return lget
        
    except:
        pass
    
    return None

def delete(con: sqlite3.Connection, table_name: str) -> None:
    if not table_name:
        return None
    
    cursor_obj = con.cursor()
    cursor_obj.execute(gen_delete(table_name))
    con.commit()
    