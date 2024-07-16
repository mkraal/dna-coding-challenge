"""
Main module
"""

import argparse
from pathlib import Path

from file_searcher import FileSearcher
from helpers import clear_cache, configure_logging

from constants import CLEAR_CACHE


logger = configure_logging()


def main():
    # Parse args
    parser = argparse.ArgumentParser(
        description="This script looks for an arbitrary line in an input text file. \n Usage: python"
    )
    parser.add_argument("input_path", type=Path, help="Path to the input text file")
    parser.add_argument("target", type=int, help="Target index of the row to look up")
    args = parser.parse_args()
    input_path = args.input_path
    target = args.target

    # optionally clear cached files
    if CLEAR_CACHE:
        clear_cache(input_path.parent)

    # search the row
    searcher = FileSearcher(input_path, target)
    searcher.print_result()


if __name__ == "__main__":
    main()
