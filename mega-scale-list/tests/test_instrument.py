# tests/test_instrument.py
# Unit tests for Instrument class in mymusiclib.instrument.

import unittest
from mymusiclib.instrument import Instrument
from mymusiclib.notes import note_to_midi

class TestInstrument(unittest.TestCase):
    def test_instrument_init_string_notes(self):
        # Test with alto sax range (Bb3 to Bb7)
        inst = Instrument('Alto Sax', 'B\u266D3', 'B\u266D7')
        self.assertEqual(inst.name, 'Alto Sax')
        self.assertEqual(inst.get_min_midi(), note_to_midi('B\u266D3'))  # 58
        self.assertEqual(inst.get_max_midi(), note_to_midi('B\u266D7'))  # 106
        self.assertEqual(inst.get_min_note(), 'B\u266D3')
        self.assertEqual(inst.get_max_note(), 'B\u266D7')

    def test_instrument_init_midi_notes(self):
        # Test with MIDI numbers
        inst = Instrument('Piano', 60, 72)  # C4 to C5
        self.assertEqual(inst.get_min_midi(), 60)
        self.assertEqual(inst.get_max_midi(), 72)
        self.assertEqual(inst.get_min_note(), 'C4')
        self.assertEqual(inst.get_max_note(), 'C5')

    def test_invalid_range(self):
        # Test min > max
        with self.assertRaises(ValueError):
            Instrument('Alto Sax', 'C5', 'C4')  # C5 > C4

    def test_invalid_note(self):
        # Test invalid note string
        with self.assertRaises(KeyError):
            Instrument('Alto Sax', 'X9', 'C4')

if __name__ == '__main__':
    unittest.main()