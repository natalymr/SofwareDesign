import os
import sys
import subprocess

from IO_classes import *


def exit(arg=None):
    """
    Function that emulates command "exit".
    Exit from CLI.
    :param arg:
    :return:
    """

    sys.exit()


def pwd(arg=None):
    """
    Function that emulates command "pwd".
    Print current directory.
    :param arg:
    :return:
    """

    output = output_stream()
    output.write_to_stream(os.getcwd())
    return output


def echo(args):
    """
    Function that emulates command "echo".
    Print received arg.
    :param args: list of files OR list with output_object of previous command.
    :return:
    """
    output = output_stream()

    output_str = " ".join(
        str(i) for i in args
        if type(i) != type(output)
    )

    output.write_to_stream(output_str)

    return output


def cat(args):
    """
    Function that emulates command "cat".
    Print content.
    :param args: list of files OR list with output_object of previous command.
    :return:
    """

    output = output_stream()
    if type(args[0]) != type(output):

        for each_file in args:

            if type(each_file) != type(output):
                with open(each_file, "r") as file_to_read:

                    for line in file_to_read:
                        output.write_to_stream(line)
    else:
        tmp_input = input_stream()
        tmp_input = args[0].convert_to_input()
        data_by_lines = tmp_input.get_input().split('\n')

        for line in data_by_lines:
            output.write_to_stream(line)

    return output


def wc(args):
    """
    Function that emulates command "wc".
    Print number of lines, words and bytes.
    :param args: list of files OR list with output_object of previous command.
    :return:
    """

    output = output_stream()

    if type(args[0]) != type(output):
        it = 0

        tmp_output = []

        num_of_lines = []
        num_of_words = []
        num_of_symbols = []

        for each_file in args:
            with open(each_file, "r") as opened_file:

                tmp_lines = 0
                tmp_words = 0
                tmp_symbols = 0

                for line in opened_file:
                    line_in_list = line.split()
                    tmp_lines += 1
                    tmp_words += len(line_in_list)
                    tmp_symbols += len(line)

                num_of_lines.append(tmp_lines)
                num_of_words.append(tmp_words)
                num_of_symbols.append(tmp_symbols)

                output_str = " ".join(
                    str(i) for i in args
                    if type(i) != type(output)
                )

                tmp_output.append(str(num_of_lines[it]) + ' ' + str(num_of_words[it]) + ' ' +
                                       str(num_of_symbols[it]))

                it += 1

        output.write_to_stream("\n".join(tmp_output))
    else:

        tmp_input = args[0].convert_to_input()
        data_by_lines = tmp_input.get_input().split('\n')

        lines = 0
        words = 0
        symbols = 0

        for line in data_by_lines:
            line_in_list = line.split()
            lines += 1
            words += len(line_in_list)
            symbols += len(line)
            #for each_word in line_in_list:
            #    symbols += len(each_word)

        output.write_to_stream(str(lines) + ' ' + str(words) + ' ' + str(symbols))

    return output


def not_implemented_functions(args):
    """
    This function is called when not implemented function was called.
    This function call subprocess with specified command with args.
    :param args: list
    :return:
    """

    tmp = subprocess.run(args,
                         stdout=subprocess.PIPE,
                         encoding=sys.stdout.encoding)

    outp = output_stream()
    outp.write_to_stream(str(tmp.stdout))

    return outp
