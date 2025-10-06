from mymusiclib.instrument import Instrument
inst = Instrument('Alto Sax', 'Bb3', 'Bb7')
print(inst.get_min_note())  # Prints B♭3
print(inst.get_max_note())  # Prints B♭7