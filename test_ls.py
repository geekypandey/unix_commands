import shutil
import unittest
import itertools
import os
from tempfile import mkstemp, mkdtemp

import ls


class TestLsCommand(unittest.TestCase):
    def setUp(self) -> None:
        self.dirname = mkdtemp()
        self.to_clean = [self.dirname]
        os.chdir(self.dirname)

    def create_temp_files(
        self, dirname=None, count: int = 1, prefix=None, suffix=None
    ) -> list:
        files = [
            mkstemp(dir=dirname, prefix=prefix, suffix=suffix)[1] for _ in range(count)
        ]
        self.to_clean.extend(files)
        return files

    def create_temp_folders(self, dirname=None, prefix=None, count: int = 1) -> list:
        folders = [mkdtemp(dir=dirname, prefix=None) for _ in range(count)]
        self.to_clean.extend(folders)
        return folders

    def get_base_names(self, files) -> list:
        return [os.path.basename(f) for f in files]

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
        expected = sorted(self.get_base_names(files))
        self.assertEqual(output, expected)

    def test_ls_command_with_directory_containing_files_and_folders(self) -> None:
        dirs = self.create_temp_folders(self.dirname, count=2)
        files = self.create_temp_files(self.dirname, count=3)
        output = ls.ls()
        expected = sorted(os.path.basename(f) for f in itertools.chain(files, dirs))
        self.assertEqual(output, expected)

    def test_ls_command_with_relative_path(self) -> None:
        folder = self.create_temp_folders(self.dirname, count=1)[0]
        os.chdir(folder)
        output = ls.ls("../")
        expected = [os.path.basename(folder)]
        self.assertEqual(output, expected)

    def test_ls_command_to_not_return_hidden_files_with_no_options(self) -> None:
        self.create_temp_files(self.dirname, prefix=".")
        output = ls.ls()
        expected = []
        self.assertEqual(output, expected)

    def test_ls_command_to_return_hidden_files_with_show_hidden_option(self) -> None:
        files = self.create_temp_files(self.dirname, prefix=".")
        output = ls.ls(show_hidden=True)
        expected = [os.path.basename(f) for f in files]
        self.assertEqual(output, expected)

    def test_ls_command_with_reverse_option(self) -> None:
        files = self.create_temp_files(self.dirname, count=3)
        output = ls.ls(reverse=True)
        expected = sorted(self.get_base_names(files), reverse=True)
        self.assertEqual(output, expected)

    def test_ls_command_with_home_directory_as_tilde(self) -> None:
        HOME = os.path.expanduser("~")
        folder = self.create_temp_folders(dirname=HOME)[0]
        folder = os.path.basename(folder)
        output = ls.ls("~")
        self.assertIn(folder, output)

    def tearDown(self) -> None:
        for c in self.to_clean:
            if not os.path.exists(c):
                continue

            if os.path.isdir(c):
                shutil.rmtree(c)
            else:
                os.unlink(c)
