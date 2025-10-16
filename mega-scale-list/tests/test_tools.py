# tests/test_tools.py
# Unit tests for utility functions in mymusiclib.tools.

import unittest
from mymusiclib.tools import generate_scale_table

class TestTools(unittest.TestCase):
    def test_generate_scale_table(self):
        table = generate_scale_table(root_pc=0)
        # Expected table data for C root (PC 0)
        expected = [
            {'scale': 'Major', 'mode': '', '0': 'Do', '1': '', '2': 'Re', '3': '', '4': 'Mi', '5': 'Fa', '6': '', '7': 'Sol', '8': '', '9': 'La', '10': '', '11': 'Ti', '12': 'Do'},
            {'scale': 'Harmonic Minor', 'mode': '', '0': 'La', '1': '', '2': 'Ti', '3': 'Do', '4': '', '5': 'Re', '6': '', '7': 'Mi', '8': 'Fa', '9': '', '10': '', '11': 'Si', '12': 'La'},
            {'scale': 'Melodic Minor', 'mode': '', '0': 'Re', '1': '', '2': 'Mi', '3': 'Fa', '4': '', '5': 'Sol', '6': '', '7': 'La', '8': '', '9': 'Ti', '10': '', '11': 'Di', '12': 'Re'},
            {'scale': 'Major b6', 'mode': '', '0': 'Do', '1': '', '2': 'Re', '3': '', '4': 'Mi', '5': 'Fa', '6': '', '7': 'Sol', '8': 'Le', '9': '', '10': '', '11': 'Ti', '12': 'Do'},
            {'scale': 'Diminished', 'mode': '', '0': 'Ti', '1': '', '2': 'Di', '3': 'Re', '4': '', '5': 'Mi', '6': 'Fa', '7': '', '8': 'Sol', '9': 'Le', '10': '', '11': 'Li', '12': 'Ti'},
            {'scale': 'Whole-Tone', 'mode': '', '0': 'Fa', '1': '', '2': 'Sol', '3': '', '4': 'La', '5': '', '6': 'Ti', '7': '', '8': 'Di', '9': '', '10': 'Ri', '11': '', '12': '1'}
        ]
        self.assertEqual(len(table), len(expected))
        for row, exp_row in zip(table, expected):
            self.assertEqual(row, exp_row)

if __name__ == '__main__':
    unittest.main()