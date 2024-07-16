import unittest
from pathlib import Path
from file_searcher import FileSearcher


class TestFileSearcher(unittest.TestCase):
    """Unit test for FileSearcher"""

    @classmethod
    def setUpClass(cls):
        cls.test_file_path = Path("data/small_sample.txt")
        cls.searcher = FileSearcher(cls.test_file_path, 0)

    def test_first_index(self):
        "Test first index"
        expected_line = "nula"
        self.searcher.target = 0
        result = self.searcher.run()
        self.assertEqual(result, expected_line)

    def test_valid_index(self):
        "Test an arbitrary valid index"
        index = 3
        expected_line = "tri"
        self.searcher.target = index
        result = self.searcher.run()
        self.assertEqual(result, expected_line)

    def test_out_of_bounds_index(self):
        "Test an index that is bigger than input row count"
        out_of_bounds_index = 10
        self.searcher.target = out_of_bounds_index
        with self.assertRaises(IndexError):
            self.searcher.run()


if __name__ == "__main__":
    unittest.main(verbosity=2)
