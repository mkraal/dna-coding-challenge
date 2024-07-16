"""
Module for file search related classe
"""

import json
import sys
import logging

from datetime import datetime
from pathlib import Path

from helpers import clear_cache


logger = logging.getLogger(__name__)


class FileMeta:
    """Files Metadata class"""

    def __init__(
        self, input_lines: int, index_len: int, input_len: int, input_path: Path
    ):
        self.input_lines: int = input_lines
        self.index_len: int = index_len
        self.input_len: int = input_len
        self.input_path: Path = input_path

        self.generated: str = str(datetime.now())

        self.meta_path: Path = self.get_meta_path(self.input_path)

    @classmethod
    def from_json(cls, json_data: dict, input_path: Path) -> "FileMeta":
        """Create FileMeta object from json data"""
        return cls(
            input_lines=json_data["input_lines"],
            index_len=json_data["index_len"],
            input_len=json_data["input_len"],
            input_path=input_path,
        )

    @classmethod
    def get_meta_path(cls, input_path: Path) -> Path:
        """Get meta path based on the input path"""
        input_dir = input_path.parent
        stem = input_path.stem
        fname = f"{input_dir}/{stem}_meta.json"
        return Path(fname)

    def build_meta(self) -> dict:
        """Builds the content of the metadata file"""
        return {
            "input_lines": self.input_lines,
            "index_len": self.index_len,
            "input_len": self.input_len,
            "generated": self.generated,
        }

    def write_meta(self) -> None:
        """Writes meta to a json file"""
        with open(self.meta_path, "w") as fid:
            logger.info(f"Writing input file metadata to {self.meta_path}")
            json.dump(self.build_meta(), fid)


class FileSearcher:
    """Main class for searching an arbitrary row in an input file"""

    def __init__(self, input_path: Path, target: int):
        self.input_path: Path = input_path
        self.target: int = target
        self.meta: FileMeta = None

        self.index_path = self.get_index_path()
        self.validate_path()
        self.load_meta()

    def write_index(self) -> FileMeta:
        """Writes index and meta files to disk"""
        with open(self.input_path, "r") as input:
            with open(self.index_path, "w") as index:
                logger.info(f"Creating index file to {self.index_path}")
                input_lines = 0
                offset = 0
                for line in input:
                    index.write(f"{input_lines},{offset}\n")
                    offset += len(line)
                    input_lines += 1
                index_len = index.tell()
                meta = FileMeta(input_lines, index_len, offset, self.input_path)
                meta.write_meta()
                return meta

    def binary_search_file(self, low: int, high: int) -> int | None:
        """Perform binary search on index file using byte offsets"""
        with open(self.index_path, "r") as index:
            # Edge cases, that can be resolved O(1)
            if self.target == 0:
                return int(index.readline().split(",")[1])
            if self.target == self.meta.input_lines:
                index.seek(self.meta.index_len)
                return int(index.readline().split(",")[1])
            if self.target > self.meta.input_lines:
                raise IndexError(
                    f"Provided index: {self.target} is bigger than the number of input lines: {self.meta.input_lines}"
                )
            # Proceed with binary search
            while low <= high:
                mid = (low + high) // 2
                index.seek(mid)
                index.readline()
                line = index.readline().split(",")
                if int(self.target) == int(line[0]):
                    return int(line[1])
                elif self.target < int(line[0]):
                    high = mid - 1
                else:
                    low = mid + 1
        return None

    def load_meta(self) -> None:
        """Loads metadata from the JSON file"""
        try:
            with open(FileMeta.get_meta_path(self.input_path), "r") as fid:
                json_data = json.load(fid)
                self.meta = FileMeta.from_json(json_data, self.input_path)
        except FileNotFoundError:
            logger.info("Metadata file not found, creating new index and metadata.")
            self.meta = self.write_index()

    def get_index_path(self) -> Path:
        """Builds an index path based on the path of the index path"""
        input_dir = self.input_path.parent
        stem = self.input_path.stem
        fname = f"{str(input_dir)}/{stem}_index.idx"
        return Path(fname)

    def validate_path(self) -> None:
        """Validates if specified input file exists"""
        if not self.input_path.exists():
            raise FileNotFoundError("Selected file doesn't exist")

    def find_row(self, row_offset: int) -> str:
        """Find the target row in the input file"""
        with open(self.input_path, "r") as data:
            data.seek(row_offset)
            return data.readline().strip("\n")

    def run(self) -> str:
        """Main method of the class, performs binary search on the index file and returns the target row from the input file"""
        logger.info(
            f"Searching for line number {self.target} in {self.input_path.stem}"
        )
        low = 0
        high = self.meta.index_len
        row_offset = self.binary_search_file(low, high)
        return self.find_row(row_offset)

    def print_result(self) -> None:
        """Prints out the result"""
        print(self.run())


def main():
    CLEAR_CACHE = False
    if not len(sys.argv) == 3:
        raise SyntaxError(
            "Wrong usage, use: `python <filename>.py <path_to_dataset> <target row>"
        )
    input_path = Path(sys.argv[1])
    target = int(sys.argv[2])
    if CLEAR_CACHE:
        clear_cache(input_path.parent)
    searcher = FileSearcher(input_path, target)
    searcher.print_result()


if __name__ == "__main__":
    main()
