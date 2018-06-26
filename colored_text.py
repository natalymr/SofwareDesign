from typing import NewType

Color = NewType("Color", str)

ANSI_RESET = Color("\u001B[0m")
ANSI_RED = Color("\u001B[31m")
ANSI_RED_BOLD = Color("\u001b[1;31m")


def ansii_colored(s: str, c: Color):
    return c + s + ANSI_RESET


def color_range(updated_line, start, end, color: Color) -> str:
    return updated_line[:start] \
           + ansii_colored(updated_line[start:end], color) \
           + updated_line[end:]

