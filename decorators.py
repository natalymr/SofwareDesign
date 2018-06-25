from IO_classes import *


def func_with_args(func, *args):
    """
    Decorator for calling specified fucntions with args
    """
    return func(*args)


def print_func_output(func, *args):
    """
    Decorator that wrapped a calling of last command to print the result to CLI.
    """
    output = output_stream()
    output = func(*args)
    to_show = input_stream()
    to_show = output.convert_to_input()
    print(to_show.get_input())
