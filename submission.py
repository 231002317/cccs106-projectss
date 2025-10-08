#!/usr/bin/env python3

import sys
from typing import TextIO


def solve(input_stream: TextIO = sys.stdin, output_stream: TextIO = sys.stdout) -> None:
    """Generic entry point for graders.

    Reads all input from ``input_stream`` and writes the result to ``output_stream``.
    Currently this echoes the input unchanged so the file runs without errors.
    Replace the body with your assignment logic if required.
    """
    data = input_stream.read()
    output_stream.write(data)


if __name__ == "__main__":
    solve()

