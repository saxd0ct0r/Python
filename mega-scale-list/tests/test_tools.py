# tests/test_tools.py
# Unit tests for tools in mymusiclib.tools.

import unittest
from mymusiclib.tools import generate_distribution_table

class TestTools(unittest.TestCase):
    def test_distribution_table_major(self):
        rows = generate_distribution_table()
        major_ionian = next(r for r in rows if r['parent'] == 'Major' and r['mode'] == 'Ionian')
        expected = {'0': 'Do', '2': 'Re', '4': 'Mi', '5': 'Fa', '7': 'Sol', '9': 'La', '11': 'Ti', '12': 'Do'}
        for i in range(13):
            key = str(i)
            if key in expected:
                self.assertEqual(major_ionian[key], expected[key])
            else:
                self.assertEqual(major_ionian[key], '')

    def test_distribution_table_dorian(self):
        rows = generate_distribution_table()
        major_dorian = next(r for r in rows if r['parent'] == 'Major' and r['mode'] == 'Dorian')
        expected = {'0': 'Re', '2': 'Mi', '3': 'Fa', '5': 'Sol', '7': 'La', '9': 'Ti', '10': 'Do', '12': 'Re'}
        for i in range(13):
            key = str(i)
            if key in expected:
                self.assertEqual(major_dorian[key], expected[key])
            else:
                self.assertEqual(major_dorian[key], '')

    def test_distribution_table_major_7(self):
        rows = generate_distribution_table()
        maj7 = next(r for r in rows if r['parent'] == 'Major 7' and r['mode'] == 'Maj7')
        expected = {'0': 'Do', '4': 'Mi', '7': 'Sol', '11': 'Ti', '12': 'Do'}
        for i in range(13):
            key = str(i)
            if key in expected:
                self.assertEqual(maj7[key], expected[key])
            else:
                self.assertEqual(maj7[key], '')

if __name__ == '__main__':
    unittest.main()