from src.IO_classes import *


def func_with_args(func, *args):
    return func(*args)


def print_func_output(func, *args):
    output = output_stream()
    output = func(*args)
    to_show = input_stream()
    to_show = output.convert_to_input()
    print(to_show.get_input())
