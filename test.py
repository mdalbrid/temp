import unittest
import pathlib
import filecmp

from io import StringIO
from scoros_test_task import Differences

FILE_PATH = pathlib.Path(__file__).parents[0]

PATH1 = pathlib.Path(FILE_PATH, "test", "1.txt")
PATH2 = pathlib.Path(FILE_PATH, "test", "2.txt")

OK1 = pathlib.Path(FILE_PATH, "test", "ok1.txt")
OK2 = pathlib.Path(FILE_PATH, "test", "ok2.txt")


class TestDifferences(unittest.TestCase):
    
    def setUp(self):
        self.d = Differences(PATH1, PATH2)


    def test_diff(self):
        #print('pass ', end='')
        pass


    def test_diff_in_html(self):
        #print('pass ', end='')
        pass


    def test_create_files(self):
        diff = self.d.diff()

        out1, out2 = StringIO(), StringIO()
        self.d.create_files(diff, "test", out1, out2)
        
        out1.seek(0)
        out2.seek(0)
        with open(OK1) as f, open(OK2) as s:
            self.assertEqual(out1.readline(), f.readline())
            self.assertEqual(out2.readline(), s.readline())


if __name__ == "__main__":
  unittest.main()
