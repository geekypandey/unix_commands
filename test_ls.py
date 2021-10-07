import shutil
import unittest
import os
from tempfile import mkstemp, mkdtemp

import ls


class TestLsCommand(unittest.TestCase):
    def setUp(self) -> None:
        self.dirname = mkdtemp()
        self.to_clean = [self.dirname]
        os.chdir(self.dirname)

    def create_temp_files(self, dirname=None, count: int = 1) -> list:
        files = [mkstemp(dir=dirname)[1] for _ in range(count)]
        self.to_clean.extend(files)
        return files

    def test_ls_command_with_no_arguments(self) -> None:
        output = ls.ls()
        expected = []
        self.assertEqual(output, expected)

    def test_ls_command_with_argument_as_current_directory(self) -> None:
        output = ls.ls(".")
        expected = []
        self.assertEqual(output, expected)

    def test_ls_command_with_directory_with_two_files(self) -> None:
        files = self.create_temp_files(dirname=self.dirname, count=3)
        output = ls.ls()
        expected = sorted(os.path.basename(file) for file in files)
        self.assertEqual(output, expected)

    def tearDown(self) -> None:
        for c in self.to_clean:
            if not os.path.exists(c):
                continue

            if os.path.isdir(c):
                shutil.rmtree(c)
            else:
                os.unlink(c)
