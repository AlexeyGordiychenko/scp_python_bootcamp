# Day 04 - Python Bootcamp

Day 04 is about iterators and generators, working with `pytest`, `pytest-cov` and `pylint`

You can just run the scripts to test it, no additional requirements are needed.

If you want to run the tests, make sure you have `pytest` installed.

## Task

### [Exercise 00](EX00/energy.py): Energy Flow

You need to write a script `energy.py` with a function called `fix_wiring()`, which should accept 
three iterables (you can test the functionality with just lists) called `cables`, `sockets` and 
`plugs`. This function shouldn't make any assumptions about the length of those iterables, which 
may be different. It should return another iterable over strings with commands like:

`plug cable1 into socket1 using plug1`
`weld cable2 to socket2 without plug`

You can see that the only iterator which length doesn't matter is `plugs`, because at the worst
case cables can be welded to sockets. If there is not enough cables or sockets, there is nothing
you can do, so they shouldn't be present in a resulting iterator.

This means, for a code like this:

```
plugs = ['plug1', 'plug2', 'plug3']
sockets = ['socket1', 'socket2', 'socket3', 'socket4']
cables = ['cable1', 'cable2', 'cable3', 'cable4']

for c in fix_wiring(cables, sockets, plugs):
    print(c)
```

the output should be:

```
plug cable1 into socket1 using plug1
plug cable2 into socket2 using plug2
plug cable3 into socket3 using plug3
weld cable4 to socket4 without plug
```

Also, input iterators can contain other non-string datatypes, which should be filtered out. So, for
an input like

```
plugs = ['plugZ', None, 'plugY', 'plugX']
sockets = [1, 'socket1', 'socket2', 'socket3', 'socket4']
cables = ['cable2', 'cable1', False]
```

it should be just

```
plug cable2 into socket1 using plugZ
plug cable1 into socket2 using plugY
```

To have fun, you can get additional points if the body of your function could be written using only
one line (starting with `return`), meaning no block-starting colons (like in `if` conditions or 
`try/except`) are used.

### Exercise 01: Personalities

You need to implement a generator function for turrets called `turrets_generator()` in a file
called `personality.py`. The tricky part is, you shouldn't describe the Turret class separately
(there is a way to generate *both* the class and the instance dynamically without using the
word `class` at all).

```
class: Turret
personality traits: neuroticism, openness, conscientiousness, extraversion, agreeableness
actions: shoot, search, talk
```

Also, three methods should just print 'Shooting', 'Searching' and 'Talking', correspondently.
Each personality trait should be a random number between 0 and 100, and the sum of all five
for every instance should be equal to 100.

### Exercise 02: Backpressure

First, you need to create a file `pressure.py` a generator function `emit_gel()` which should
simulate the measured pressure of a liquid. It should generate an infinite stream of numbers going
from 0 to 100 (values > 100 are considered an error) with a random step sampled from range 
`[0, step]` where `step` is an argument of a generator `emit_gel()`.

Second, you need to follow the guidelines for the pressure control. Operating pressure is supposed
to be between 20 and 80, meaning if a generator at some point emits a value below 20 or above 80
the action should be applied that will reverse the sign of the step. To implement this kind of
valve you need to write another function called `valve()`, which will loop over values of
`emit_gel()` and use `.send()` method to flip the current step sign.

Third, you should implement an emergency break. If a pressure is above 90 or below 10, the
`emit_gel()` generator should be gracefully closed and the script should exit.

Feel free to experiment around and pick a `step` so that your script will run for a few seconds
before exiting. You can add a delay between "pressure measurements" to avoid spending too much
CPU on generating and processing the sequence.
