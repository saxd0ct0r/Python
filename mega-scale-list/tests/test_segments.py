# tests/test_segments.py
# Unit tests for segment generator in mymusiclib.segments.

import unittest
from mymusiclib.segments import generate_segments, generate_weight_vector
from mymusiclib.instrument import Instrument

class TestSegments(unittest.TestCase):
    def test_generate_weight_vector(self):
        # Test Bb3, C4, Db4 (MIDI 58, 60, 61)
        midis = [58, 60, 61]
        self.assertEqual(generate_weight_vector(midis), [3, 2, 2, 1])

    def test_generate_segments_alto_sax(self):
        inst = Instrument('Alto Sax', 'B\u266D3', 'B\u266D7')
        collections = ['Major', 'Major 7']
        segments = generate_segments(inst, collections, min_len=3)
        # Check first few segments (smallest range, top-weighted)
        expected = [
            'B\u266D3 Dorian from B\u266D3 to D\u266D4',  # MIDI 58,60,61
            'B\u266D3 Phrygian from B\u266D3 to D\u266D4'  # MIDI 58,59,61
        ]
        self.assertGreater(len(segments), 0)
        found = [s['entry'] for s in segments[:2]]
        self.assertEqual(found, expected)

    def test_generate_segments_arpeggio(self):
        inst = Instrument('Alto Sax', 'B\u266D3', 'B\u266D7')
        collections = ['Major 7']
        segments = generate_segments(inst, collections, min_len=3)
        # Check a 3-note arpeggio segment
        expected = 'B\u266D3 Maj7 from B\u266D3 to F4'
        found = [s['entry'] for s in segments]
        self.assertIn(expected, found)

    def test_empty_collections(self):
        inst = Instrument('Alto Sax', 'B\u266D3', 'B\u266D7')
        segments = generate_segments(inst, [], min_len=3)
        self.assertEqual(segments, [])

    def test_invalid_collection(self):
        inst = Instrument('Alto Sax', 'B\u266D3', 'B\u266D7')
        segments = generate_segments(inst, ['Unknown'], min_len=3)
        self.assertEqual(segments, [])

if __name__ == '__main__':
    unittest.main()