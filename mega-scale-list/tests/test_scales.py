# tests/test_scales.py
# Unit tests for scales and arpeggios in mymusiclib.scales.

import unittest
from mymusiclib.scales import get_preferred_spelling, Scale, Arpeggio
from mymusiclib.notes import note_to_midi

class TestScales(unittest.TestCase):
    def test_major_scale_spelling(self):
        # C Major (Ionian)
        self.assertEqual(get_preferred_spelling('Major', 0, 0), ['C', 'D', 'E', 'F', 'G', 'A', 'B'])
        # F# Major prefers Gb (fewer accidentals)
        self.assertEqual(get_preferred_spelling('Major', 0, 6), ['G\u266D', 'A\u266D', 'B\u266D', 'C\u266D', 'D\u266D', 'E\u266D', 'F'])
        # D Dorian (mode 1 of C Major)
        self.assertEqual(get_preferred_spelling('Major', 1, 2), ['D', 'E', 'F', 'G', 'A', 'B', 'C'])

    def test_invalid_collection_spelling(self):
        self.assertIsNone(get_preferred_spelling('Unknown', 0, 0))

    def test_no_double_accidentals(self):
        spelling = get_preferred_spelling('Major', 0, 6)
        self.assertFalse(any('##' in n or 'bb' in n for n in spelling))

    def test_scale_generate_major(self):
        scale = Scale('Major', 'C4', mode_index=0)
        self.assertEqual(scale.generate(), [60, 62, 64, 65, 67, 69, 71])
        self.assertEqual(scale.get_mode_name(), 'Ionian')
        # Dorian mode (2nd mode)
        scale = Scale('Major', 'D4', mode_index=1)
        self.assertEqual(scale.generate(), [62, 64, 65, 67, 69, 71, 72])

    def test_scale_generate_harmonic_minor(self):
        scale = Scale('Harmonic Minor', 'A4', mode_index=0)
        self.assertEqual(scale.generate(), [69, 71, 72, 74, 76, 77, 80])
        self.assertEqual(scale.get_mode_name(), 'Aeolian #7')

    def test_scale_generate_melodic_minor(self):
        scale = Scale('Melodic Minor', 'C4', mode_index=0)
        self.assertEqual(scale.generate(), [60, 62, 63, 65, 67, 69, 71])
        self.assertEqual(scale.get_mode_name(), 'Dorian #7')

    def test_scale_generate_major_b6(self):
        scale = Scale('Major b6', 'C4', mode_index=0)
        self.assertEqual(scale.generate(), [60, 62, 64, 65, 67, 68, 71])
        self.assertEqual(scale.get_mode_name(), 'Ionian b6')

    def test_scale_generate_diminished(self):
        scale = Scale('Diminished', 'C4', mode_index=0)
        self.assertEqual(scale.generate(), [60, 62, 63, 65, 66, 68, 69, 71])
        self.assertEqual(scale.get_mode_name(), 'Dim 0')

    def test_scale_generate_whole_tone(self):
        scale = Scale('Whole-Tone', 'C4', mode_index=0)
        self.assertEqual(scale.generate(), [60, 62, 64, 66, 68, 70])
        self.assertEqual(scale.get_mode_name(), 'WT 0')

    def test_scale_invalid_type(self):
        with self.assertRaises(ValueError):
            Scale('Unknown', 'C4')

    def test_scale_too_many_notes(self):
        scale = Scale('Major', 'C4')
        with self.assertRaises(ValueError):
            scale.generate(num_notes=8)

    def test_scale_partial(self):
        scale = Scale('Major', 'C4')
        self.assertEqual(scale.generate(num_notes=3), [60, 62, 64])

    def test_arpeggio_generate_major_triad(self):
        arp = Arpeggio('Major triad', 'C4', inversion_index=0)
        self.assertEqual(arp.generate(), [60, 64, 67])
        self.assertEqual(arp.get_inversion_name(), 'Maj')
        # First inversion (Maj/3)
        arp = Arpeggio('Major triad', 'E4', inversion_index=1)
        self.assertEqual(arp.generate(), [64, 67, 72])

    def test_arpeggio_generate_minor_triad(self):
        arp = Arpeggio('Minor triad', 'C4', inversion_index=0)
        self.assertEqual(arp.generate(), [60, 63, 67])
        self.assertEqual(arp.get_inversion_name(), 'Min')

    def test_arpeggio_generate_major_7(self):
        arp = Arpeggio('Major 7', 'C4', inversion_index=0)
        self.assertEqual(arp.generate(), [60, 64, 67, 71])
        self.assertEqual(arp.get_inversion_name(), 'Maj7')
        # Second inversion (Maj7/5)
        arp = Arpeggio('Major 7', 'G4', inversion_index=2)
        self.assertEqual(arp.generate(), [67, 71, 72, 76])

    def test_arpeggio_generate_minor_7(self):
        arp = Arpeggio('Minor 7', 'C4', inversion_index=0)
        self.assertEqual(arp.generate(), [60, 63, 67, 70])
        self.assertEqual(arp.get_inversion_name(), 'Min7')

    def test_arpeggio_generate_dominant_7(self):
        arp = Arpeggio('Dominant 7', 'C4', inversion_index=0)
        self.assertEqual(arp.generate(), [60, 64, 67, 70])
        self.assertEqual(arp.get_inversion_name(), 'Dom7')

    def test_arpeggio_generate_half_diminished_7(self):
        arp = Arpeggio('Half-Diminished 7', 'C4', inversion_index=0)
        self.assertEqual(arp.generate(), [60, 63, 66, 70])
        self.assertEqual(arp.get_inversion_name(), 'HalfDim7')

    def test_arpeggio_generate_diminished_7(self):
        arp = Arpeggio('Diminished 7', 'C4', inversion_index=0)
        self.assertEqual(arp.generate(), [60, 63, 66, 69])
        self.assertEqual(arp.get_inversion_name(), 'Dim7')

    def test_arpeggio_invalid_type(self):
        with self.assertRaises(ValueError):
            Arpeggio('Unknown', 'C4')

    def test_arpeggio_too_many_notes(self):
        arp = Arpeggio('Major 7', 'C4')
        with self.assertRaises(ValueError):
            arp.generate(num_notes=5)

    def test_arpeggio_partial(self):
        arp = Arpeggio('Major 7', 'C4')
        self.assertEqual(arp.generate(num_notes=3), [60, 64, 67])

    def test_arpeggio_spelling(self):
        # C Major 7
        self.assertEqual(get_preferred_spelling('Major 7', 0, 0), ['C', 'E', 'G', 'B'])
        # Gb Major 7 prefers flats
        self.assertEqual(get_preferred_spelling('Major 7', 0, 6), ['G\u266D', 'B\u266D', 'D\u266D', 'F'])
        # C Dim7 (enharmonic to avoid doubles, late duplicate)
        self.assertEqual(get_preferred_spelling('Diminished 7', 0, 0), ['C', 'E\u266D', 'F\u266F', 'A'])

if __name__ == '__main__':
    unittest.main()