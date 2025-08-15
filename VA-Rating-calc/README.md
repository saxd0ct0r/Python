This is a quick little utility that calculates the VA's total disability rating given the inputs
of individual claims. The calculation works like this. Assume you start with 100% ability. A
disability claim that is identified as 30% means your ability is reduced to 70% by *multiplying*
1.00 * (1 - 0.30) == 0.70. The next individual claim, 20%, is again *multiplied* 
0.70 * (1 - 0.20) == 0.56, and so on. The final rating is 100% minus your remaining ability, rounded
to the nearest ten, so 95.0% rounds up to 100% but 94.9% rounds to 90%.

A lot of my peers in the Army complained about how byzantine the VA calculation works. I hope this widget
and the explanation above demystify it, at least a little. Cheers!
