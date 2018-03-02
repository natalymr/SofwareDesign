import re

from src.aux_functions import *
from src.decorators import *
from src.utilites import *

dict_of_implemented_commands = {'exit' : exit, 'pwd' : pwd, 'echo' : echo, 'cat' : cat, 'wc' : wc}
dict_of_variables = {}


# main function
def console_emulator():
    global dict_of_implemented_commands
    global dict_of_variables

    while True:
        input_str = input()
        input_list = input_str.split()

        if '"' in input_str:
            first_ind = 0
            second_ind = 0
            for i in range(0, len(input_list)):
                regex = re.compile(".*(\").*")
                tmp = regex.search(input_list[i])
                if tmp:
                    first_ind = i
                    break

            for j in range(first_ind, len(input_list)):

                regex = re.compile(".*(\").*")
                tmp = regex.search(input_list[j])
                if tmp:
                    second_ind = j

            input_list[first_ind : second_ind + 1] = [''.join(input_list[first_ind : second_ind + 1])]

        if "'" in input_str:
            pass


        if "|" in input_list:
            pipe_execution(input_list)
        else:
            print_func_output(execute_command, input_list, 0, len(input_list))


def pipe_execution(input_list):

    # get indices of |
    pipe_indices = []
    idx = -1
    while True:
        try:
            idx = input_list.index("|", idx + 1)
            pipe_indices.append(idx)
        except ValueError:
            break

    # execute each command
    start_ind_command = 0
    stream_io = output_stream()
    for end_ind_command in pipe_indices:
        stream_io = execute_command(input_list, start_ind_command, end_ind_command, stream_io)
        start_ind_command = end_ind_command + 1
    print_func_output(execute_command, input_list, start_ind_command, len(input_list), stream_io)


def execute_command(list, first_ind, last_ind, stream_arg=None):
    global dict_of_implemented_commands
    global dict_of_variables

    # if there is a $
    regex = re.compile(".*(\$).*")
    dol_sign = [m.group(0) for ind in range(first_ind, last_ind)
              for m in [regex.search(list[ind])] if m]

    if dol_sign:
        dol_sign = dol_sign[0]

        var_output = output_stream()

        var_output.write_to_stream(exe_dollar_sign(dol_sign))

        return var_output

    # if there is a =
    regex = re.compile(".*(=).*")
    eq_sign = [m.group(0) for ind in range(first_ind, last_ind)
           for m in [regex.search(list[ind])] if m]

    if eq_sign:
        eq_sign = eq_sign[0]

        empty_output = output_stream()

        exe_equal_sign(eq_sign)

        return empty_output

    # usual commands
    command = list[first_ind]
    args = []

    # command has no args
    if last_ind - first_ind <= 1:
        if stream_arg is None:
            if command in dict_of_implemented_commands:
                result = dict_of_implemented_commands[command]()
            else:
                args.insert(0, command)
                result = func_with_args(not_implemented_functions, args)
        else:
            args.append(stream_arg)
            if command in dict_of_implemented_commands:
                result = func_with_args(dict_of_implemented_commands[command], args)
            else:
                result = func_with_args(not_implemented_functions(command), args)

    # command has arguments
    else:

        for trans_arg in range(first_ind + 1, last_ind):
            args.append(list[trans_arg])

        if stream_arg is None:
            if command in dict_of_implemented_commands:
                result = func_with_args(dict_of_implemented_commands[command], args)
            else:
                args.insert(0, command)
                result = func_with_args(not_implemented_functions, args)
        else:
            args.append(stream_arg)
            if command in dict_of_implemented_commands:
                result = func_with_args(dict_of_implemented_commands[command], args)
            else:
                args.insert(0, command)
                result = func_with_args(not_implemented_functions, args)

    return result
