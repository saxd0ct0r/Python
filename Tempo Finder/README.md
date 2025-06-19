For anyone who has worked with a metronome to try to master a piece of music, how often have you heard, "Slow practice is the key"? Well, how slow?

I have always thought that advice was incomplete. I try to practice difficult passages at a tempo that I know I can play cleanly, but I also want to
push myself systematically to uncover flaws that aren't always apparent when I am practicing slowly.

The basic idea behind this practice is to use a binary search-like pattern. Imagine that the range of tempos (in this case, from 30bpm to 240bpm)
is the search space. Hidden within that search space is the magical tempo that is the fastest you can play a scale, for example, without mistakes,
without stress, and everything is smooth, as governed by your present ability.
If you start at an arbitrary tempo in the middle, you determine if the target tempo is above or below
what you played based on whether you succeeded at that tempo. You then move up or down the range of tempos with finer and finer increments, until
you zero in on that target. This should have an O(1) time complexity. The only potentially wasted effort is if you hit the target tempo early
on in the sequence, but you don't know it's the target until you have failed to play it faster. Even so, you are only "wasting" three or four
repetitions instead of dozens.

The scripts in this project folder help with that process. The "all_tempo_sequences" files demonstrate that the algorithm can hit all potential 
tempos within a range of 1/4x to 4x of the starting tempo; the "tempo_finder_random" file simulates someone setting the metronome randomly and working
through a difficult passage for the first time, or in other words, they have no idea what their ability holds, so the target is unknown. My next step is
to encapsulate the algorithm into a function or even a class that can be integrated into a web interface, so you can have the script take your starting
tempo and reports of your subsequent successes or failures, and provide you with the next tempo to attempt. 

This version of the algorithm is suited for
anything that has an arbitrary tempo, i.e., it doesn't have a maximum tempo. You want to play your scales as fast as possible. Other versions
are for pieces that have specific tempos specified by the composer, for example. But that's for another time.
