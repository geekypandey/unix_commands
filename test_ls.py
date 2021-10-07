import unittest

import ls

class TestLsCommand(unittest.TestCase):
    def test_ls_command_with_no_options_and_no_arguments(self):
        output = ls.ls()
        expected = []
        self.assertEqual(output, expected)
