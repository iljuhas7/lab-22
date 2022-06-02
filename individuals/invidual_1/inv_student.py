#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import inv_command
import inv_sqlite3
import inv_jsonschema
import sys

list_students = []

_main_ = True
mem_db = inv_sqlite3.connect_memory()


def student_add(name: str = '', group: int = 0, year: int = 0, cl: bool = False) -> bool:
    global list_students

    student = {
        'name': name,
        'group': group,
        'z': year,
    }

    if cl:
        in_name = str(input('Фамилия и инициалы? ' + '[' + name + ']: '))
        in_number = int(input('Номер группы? ' + '[' + str(group) + ']: '))
        in_year = int(input('Успеваемость? ' + '[' + str(year) + ']: '))

        if in_name:
            student['name'] = in_name

        if in_number:
            student['number'] = in_number

        if in_year:
            student['z'] = in_year

    for cur_student in list_students:
        if cur_student['name'] == name:
            return False

    if not inv_jsonschema.test(student):
        print("[Error]", inv_jsonschema.test_msg(student))
        return False

    list_students.append(student)

    if len(student) > 1:
        list_students.sort(key=lambda item: item.get('name', ''))


def student_print_line() -> None:
    print('+-{}-+-{}-+-{}-+-{}-+'.format(
        '-' * 4,
        '-' * 30,
        '-' * 20,
        '-' * 15
    )
    )


def student_print_list() -> None:
    global list_students

    student_print_line()
    print(
        '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
            "№",
            "Ф.И.О.",
            "Номер группы",
            "Успеваемость"
        )
    )
    student_print_line()
    for idx, worker in enumerate(list_students, 1):
        print(
            '| {:>4} | {:<30} | {:<20} | {:>15} |'.format(
                idx,
                worker.get('name', ''),
                worker.get('number', 0),
                worker.get('z', 0)
            )
        )
    student_print_line()


def student_print_list_select(period: int) -> None:
    global list_students

    cn = 0

    student_print_line()
    print(
        '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
            "№",
            "Ф.И.О.",
            "Номер группы",
            "Успеваемость"
        )
    )
    student_print_line()
    for idx, student in enumerate(list_students, 1):
        if period == student.get('z', 0):
            cn -= 1

            print(
                '| {:>4} | {:<30} | {:<20} | {:>15} |'.format(
                    idx,
                    student.get('name', ''),
                    student.get('number', 0),
                    student.get('z', 0)
                )
            )

    student_print_line()

    if cn == 0:
        print('Таких студентов нет')


def student_save(file_path: str) -> bool:
    global list_students, mem_db

    get = inv_sqlite3.get(mem_db, '*', 'student')

    if get and len(get):
        inv_sqlite3.delete(mem_db, 'student')

    inv_sqlite3.create(mem_db, 'student', name=str, number=int, z=int)

    for current in list_students:
        inv_sqlite3.add(mem_db, 'student', 
                        current['name'], 
                        (current['group'] if current['group'] else 0),
                        current['z'])

    inv_sqlite3.save(file_path)

    return True


def student_load(file_path: str) -> bool:
    global list_students, mem_db

    inv_sqlite3.laod(file_path)

    get = inv_sqlite3.get(mem_db, '*', 'student')

    if not get:
        return False

    list_students = [{'name': x[1], 'group': x[2], 'z': x[3]} for x in get]
    
    return True


def parse_call_command(command_line: str = None, not_cmd: bool = False) -> object:
    p = inv_command.parse_call_command(command_line, not_cmd)

    if p.get('command'):
        if p.get('filename', None):
            student_load(p['filename'])

        f = inv_command.call_command(p['command'])

        if not f['error']:
            return f['return']

    return None


def student_exit() -> None:
    pass


def student_terminal(command_line: str = None, not_cmd: bool = False) -> None:
    global list_students

    while True:
        if not_cmd:
            send = command_line
        else:
            send = inv_command.send_command(cl=True, s=False)

        arg = inv_command.parse_call_command(send, not_cmd)

        cmd = arg.get('command', None)
        if arg.get('command', None):
            arg.pop('command')

        file = arg.get('filename', 'unknown_file.json')
        if arg.get('filename', None):
            arg.pop('filename')

        if not_cmd:
            student_load(file)

        if cmd == 'exit' and (not not_cmd):
            break

        if (cmd == 'load' or cmd == 'save') and (not not_cmd):
            arg['file_path'] = file

        if cmd == 'add' and (not not_cmd):
            print(arg)

        err = inv_command.call_command(cmd, **arg)['error']

        if err and command_line:
            print("Неизвестная команда", file=sys.stderr)

        if cmd == 'add' and not_cmd:
            student_save(file)

        if not_cmd:
            break


if _main_:
    _main_ = False

    # registr method
    inv_command.regist_command('add', student_add, 'добавить студента')
    inv_command.regist_command(
        'select', student_print_list_select, 
        'вывести список студентов, имеющих Успеваемость')
    inv_command.regist_command(
        'list', student_print_list, 'вывести список студентов')
    inv_command.regist_command(
        'save', student_save, 'Сохранить', inv_command.cl_or_cmd['cmd'])
    inv_command.regist_command(
        'load', student_load, 'Загрузить', inv_command.cl_or_cmd['cmd'])
    inv_command.regist_command(
        'exit', student_exit, 'Выход', inv_command.cl_or_cmd['cmd'])
    inv_command.regist_command(
        'cl', student_terminal, 'Терминал', inv_command.cl_or_cmd['cl'])

    # add help
    inv_command.add_arg_command('add', 'name', 'n', True, 'Ф.И.О.', str)
    inv_command.add_arg_command(
        'add', 'group', 'g', False, 'Номер группы', int)
    inv_command.add_arg_command('add', 'year', 'y', True, 'Успеваемость', int)

    inv_command.add_arg_command(
        'select', 'period', 'p', True, 'Успеваемость', int)
