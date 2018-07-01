import re

from typing import List, Dict, Callable
from decorators import *
from utilities import *
from exception import IncorrectCommand

CommandRegistry = Dict[str, Callable[[str], output_stream]]
dict_of_implemented_commands: CommandRegistry = {
    'exit' : exit,
    'pwd'  : pwd,
    'echo' : echo,
    'cat'  : cat,
    'wc'   : wc
}

dict_of_variables = {}


# main function
def console_emulator():
    """
    Function that emulate command line.
    There is an infinity loop in which commands with args are read from console
    After it if there are pipes in a readed line, pipe_execution is called.
    Otherwise execute_command is called and prints a result.
    """

    global dict_of_implemented_commands
    global dict_of_variables

    while True:
        input_str = input()
        input_list = input_str.split()

        # find expressions in "
        # and join it in one element of a list
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

            input_list[first_ind: second_ind + 1] = [' '.join(input_list[first_ind : second_ind + 1])]
            # delete "
            input_list[first_ind] = input_list[first_ind].replace('"', '')

        # find expressions in "
        # and join it in one element of a list
        if "'" in input_str:
            first_ind = 0
            second_ind = 0
            for i in range(0, len(input_list)):
                regex = re.compile(".*(\").*")
                tmp = regex.search(input_list[i])
                if tmp:
                    first_ind = i
                    break

            for j in range(first_ind, len(input_list)):

                regex = re.compile(".*(\').*")
                tmp = regex.search(input_list[j])
                if tmp:
                    second_ind = j

            input_list[first_ind + 1: second_ind + 1] = [' '.join(input_list[first_ind + 1: second_ind + 1])]

        if "|" in input_list:
            try:
                pipe_execution(input_list)
            except IncorrectCommand as e:
                print(f"Incorrect command: {e}")

        else:
            try:
                print_func_output(execute_command, input_list, 0, len(input_list))
            except TryExit as te:
                exit()
            except IncorrectCommand as e:
                print(f"Incorrect command: {e}")


def pipe_execution(input_list):
    """
    Identify pipes's indices, call each command separately.
    :param input_list: list of splitted by " " input string.
    """

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


def execute_command(list: List[str], first_ind: int, last_ind: int, stream_arg: output_stream = None) -> output_stream:
    """
    Function that execute given command with args.
    :param list: input string that was splotted by " "
    :param first_ind: first ind of current command
    :param last_ind: last ind of current command
    :param stream_arg: a result of previous command
    :return: output_stream
    """

    global dict_of_implemented_commands
    global dict_of_variables

    # if there is a $
    regex = re.compile(".*(\$).*")
    dol_sign = [m.group(0) for ind in range(first_ind, last_ind)
                for m in [regex.search(list[ind])] if m]
    # if there is a $. pause

    # add the logic related to '
    # if there is a ' we ignore additional special character, i.e. $
    # for example, we should use '$x' as $x as a str but not as value of x
    single_quote_dol_signs = False
    single_quote = False

    regex = re.compile(".*(\').*")
    quote_sign = [m.group(0) for ind in range(first_ind, last_ind)
                  for m in [regex.search(list[ind])] if m]
    if quote_sign:
        single_quote = True
        if dol_sign:
            single_quote_dol_signs = True

    # if there is a $. continue
    dol_sign_flag = False
    if dol_sign and not single_quote_dol_signs:
        dol_sign_flag = True
        dol_sign = dol_sign[0]

        var_output = output_stream()
        try:
            option, res = find_and_replace_values_of_all_variables(dol_sign)
        except BaseException as e:
            print(f"Incorrect command: {e}")
            return output_stream()

        if option:
            var_output.write_to_stream(res)
            return var_output
        else:
            list[first_ind] = res
            print(list[first_ind])
    # if there is a $. the end

    # if there is a =
    regex = re.compile(".*(=).*")
    eq_sign = [m.group(0) for ind in range(first_ind, last_ind)
               for m in [regex.search(list[ind])] if m]

    if eq_sign and not dol_sign_flag:
        eq_sign = eq_sign[0]

        try:
            exe_equal_sign(eq_sign)
        except BaseException as e:
            print(f"Incorrect command: {e}")

        return output_stream()

    # usual commands
    command = list[first_ind]
    args = []

    try:
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
                    result = func_with_args(not_implemented_functions, args)

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

    except IncorrectCommand as e:
        print(f"Incorrect command: {e}")
        return output_stream()

    return result


def exe_equal_sign(expression):
    """
    Function that correctly handle input str with =.
    Supplements dict, etc.
    :param expression: str that contains "="
    :return:
    """

    name = ""
    val  = ""
    ind_eq = expression.find("=")

    for i in range(0, ind_eq):
        name += expression[i]
    for i in range(ind_eq + 1, len(expression)):
        val += expression[i]

    dict_of_variables[name] = val

    return


def find_and_replace_values_of_all_variables(expression):
    """
    This function take a string and replace values of variables before which there are $
    :param expression: this is a string that contains at least one $ sign
    :return: expression, in which substituted all values
    """

    result = ""
    name = ""
    ind_dollar = expression.find("$")
    for i in range(ind_dollar):
        result += expression[i]

    if expression.find("$", ind_dollar + 1) == -1:
        ind_name_end = len(expression)
    else:
        ind_name_end = expression.find("$", ind_dollar + 1)

    for i in range(ind_dollar + 1, ind_name_end):
        name += expression[i]

    result += dict_of_variables[name]

    if "=" in expression:
        ind_equal = expression.find("=")
        var = ""
        for i in range(0, ind_equal):
            var += expression[i]
        exe_equal_sign(var + "=" + str(dict_of_variables[name]))

    # this was command call; for example 1. x=ho 2. ec$x 3
    if expression[:ind_dollar] + dict_of_variables[name] in dict_of_implemented_commands:
        return False, expression[:ind_dollar] \
               + dict_of_variables[name]

    while True:
        name = ""
        ind_dollar = expression.find("$", ind_name_end)

        if ind_dollar == -1:
            break
        else:
            if expression.find("$", ind_dollar + 1) == -1:
                ind_name_end = len(expression)
            else:
                ind_name_end = expression.find("$", ind_dollar + 1)

            for i in range(ind_dollar + 1, ind_name_end):
                name += expression[i]
            result += dict_of_variables[name]

    if result in dict_of_implemented_commands:
        return False, result

    return True, result


def main():
    console_emulator()


if __name__ == '__main__':
    main()
