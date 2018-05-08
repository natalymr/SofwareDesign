import os
import shlex
import sys
import subprocess

from IO_classes import *


def exit(arg=None):
    sys.exit()


def cd(args):
    output = output_stream()
    try:
        if args is not None and isinstance(args[0], str):
            dir = args[0]
            os.chdir(dir)
    except Exception:
        output.write_to_stream('no such file or directory')
    return output


def ls(args=None):
    output = output_stream()
    try:
        if args is None or type(args[0]) == type(output):
            dir = '.'
        else:
            dir = args[0]
        if not dir.startswith('/'):
            dir = os.path.join(os.curdir, dir)
        content = '\n'.join(os.listdir(dir))
        output.write_to_stream(content)
    except Exception:
        output.write_to_stream('no such file or directory')
    return output


def pwd(arg=None):
    output = output_stream()
    output.write_to_stream(os.getcwd())
    return output


def echo(args):
    output = output_stream()

    for i in args:
        if type(i) != type(output):
            output.write_to_stream(str(i))

    return output


def cat(args):
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

    output = output_stream()

    if type(args[0]) != type(output):
        it = 0

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
                    for each_word in line_in_list:
                        tmp_symbols += len(each_word)

                num_of_lines.append(tmp_lines)
                num_of_words.append(tmp_words)
                num_of_symbols.append(tmp_symbols)

                output.write_to_stream(str(num_of_lines[it]) + ' ' + str(num_of_words[it]) + ' ' +
                                       str(num_of_symbols[it]) + '\n')
                it += 1
    else:

        tmp_input = input_stream()
        tmp_input = args[0].convert_to_input()
        data_by_lines = tmp_input.get_input().split('\n')

        lines = 0
        words = 0
        symbols = 0

        for line in data_by_lines:
            line_in_list = line.split()
            lines += 1
            words += len(line_in_list)
            for each_word in line_in_list:
                symbols += len(each_word)
        output.write_to_stream(str(lines) + ' ' + str(words) + ' ' + str(symbols) + '\n')

    return output


def not_implemented_functions(args):

    tmp = subprocess.run(args,
                         stdout=subprocess.PIPE,
                         encoding=sys.stdout.encoding)

    outp = output_stream()
    outp.write_to_stream(str(tmp.stdout))

    return outp
