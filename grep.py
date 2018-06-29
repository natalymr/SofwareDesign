import re
from argparse import ArgumentParser, Namespace  # command line library
from collections import namedtuple
from typing import Iterable, Set, Tuple

from IO_classes import output_stream, input_stream
from colored_text import ANSI_RED, color_range

from exception import IncorrectCommand


def grep(args: [str]) -> output_stream:
    result = output_stream()
    if isinstance(args[-1], output_stream):
        input: input_stream = args[-1].convert_to_input()

        args = parse_grep_args(args[0:-1])

        grep_worker = Grep(
            args.pattern,
            ignore_case=args.ignore_case,
            whole_word=args.whole_word
        )

        for line in grep_lines(grep_worker, iter(input), args.after_context):
            result.write_to_stream(line)

    else:
        args = parse_grep_args(args)

        grep_worker = Grep(
            args.pattern,
            ignore_case=args.ignore_case,
            whole_word=args.whole_word
        )

        for filename in args.files:
            result.write_to_stream(filename + ":\n")
            with open(filename) as file:
                for line in grep_lines(grep_worker, file.readlines(), args.after_context):
                    result.write_to_stream(line)

    return result


def configure_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description="grep command"
    )

    parser.add_argument(
        "-w", "--word-regexp",
        dest="whole_word",
        action='store_true',
        default=False
    )

    parser.add_argument("pattern")

    parser.add_argument("files", nargs="*")

    parser.add_argument(
        "-i", "--ignore-case",
        dest="ignore_case",
        action='store_true',
        default=False
    )

    parser.add_argument(
        "-A", "--after-context",
        type=int,
        dest="after_context",
        default=0
    )

    return parser


def parse_grep_args(args: [str]) -> Namespace:
    try:
        return configure_parser().parse_args(args)
    except BaseException:
        raise RuntimeError("Cannot parse arguments for grep command!")


def grep_lines(grep: "Grep", lines: Iterable[str], after_context: int = 0) -> Iterable[str]:
    lines_to_print = 0

    for line in lines:
        matches = grep.match(line)
        if len(matches) != 0:
            yield (make_matches_red(line, matches))
            lines_to_print = after_context
        elif lines_to_print != 0:
            lines_to_print -= 1
            yield line


def make_matches_red(line, matches):
    for start, end in reversed(matches):
        line = color_range(line, start, end, ANSI_RED)

    return line


GrepMatch = namedtuple("GrepMatch", ["start", "end"])

words_regex = re.compile("\\w+")


def find_words_ranges(line: str) -> Set[Tuple[int, int]]:
    return set(match.span() for match in words_regex.finditer(line))


class Grep:

    def __init__(self, pattern: str, ignore_case=False, whole_word=False):
        self._pattern = pattern
        self._ignore_case = ignore_case
        self._whole_world = whole_word

    def match(self, line: str) -> [GrepMatch]:

        words_matches = find_words_ranges(line)
        regex_flags = self._ignore_case and re.IGNORECASE

        return [
            GrepMatch(*match.span())
            for match in re.finditer(self._pattern, line, flags=regex_flags)
            if (not self._whole_world or match.span() in words_matches)
        ]
