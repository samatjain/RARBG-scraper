#!/usr/bin/env python

import csv
import functools

from pathlib import Path, PurePath

import typer

from typing import Final, List


def main(csv_file: Path) -> bool:
    with csv_file.open() as fp:
        reader = csv.reader(fp)
        for line_no, row in enumerate(reader):
            title = row[0]
            fn = row[-1]

            # skip header
            if "title" in title:
                continue

            blacklist = {"VXT", "RARBG"}

            fn_endswith = functools.partial(title.endswith)
            if any(map(fn_endswith, blacklist)):
                continue

            if not fn.startswith('magnet'):
                print(f"# Missing magnet for {line_no=} {title=}")

            print(f"# {title}")
            print(fn)


if __name__ == "__main__":
    typer.run(main)
