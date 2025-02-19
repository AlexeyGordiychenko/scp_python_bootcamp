# Day 01 - Python Bootcamp

Day 01 is about functional programming and decorators in Python.

You can just run the scripts to test it, no additional requirements are needed.

## Task

### [Exercise 00](EX00/purse.py): Functional Purse

You need to write functions `add_ingot(purse)`, `get_ingot(purse)` and `empty(purse)` that accept a purse (a dictionary, which is, strictly speaking, a `typing.Dict[str, int]`) and return a purse (an empty dict in case of `empty(purse)`). They should not make assumptions about the content of the purse (it can be empty or store something completely different, like "stones").

Also, your functions shouldn't have side effects. This means, an object passed as an argument 
should not be modified inside a function. Instead, a new object should be returned. Thus, you 
*shouldn't use the code written by Tom*, as it makes a *direct assignment* to a field inside 
a purse. You should return a *new dict instance* with an updated number inside it instead.

So, a function composition like `add_ingot(get_ingot(add_ingot(empty(purse))))` should return
`{"gold_ingots": 1}`. Also, getting an ingot from an empty purse shouldn't lead to an error and should just return an empty one.

Side note: we are only interested in gold ingots in this task, so it doesn't really matter what happens with the rest of the stuff inside the purse. You can preserve it or throw away.

### [Exercise 01](EX01/splitwise.py): Splitwise

You need to write a function named `split_booty`, which will receive any number of purses (dictionaries) as arguments. Purses in arguments can possibly contain various items, but our men of honor are only interested in gold ingots (named `gold_ingots` as in examples above). Number of ingots can be zero or positive integer.

This function should return three purses (dictionaries) back so that in any two of three purses the difference between the number of ingots is no larger than 1. For example, if the booty includes `{"gold_ingots":3}`, `{"gold_ingots":2}` and `{"apples":10}`, then function should return `({"gold_ingots": 2}, {"gold_ingots": 2}, {"gold_ingots": 1})`.

While implementing this function you still shouldn't use direct assignment to fields inside dictionaries. You can reuse functions you wrote in EX00 instead. 

### [Exercise 02](EX02/squeak.py): Burglar Alarm

 So far you wrote several functions (`add_ingot(purse)`, `get_ingot(purse)` and `empty(purse)`) for the purse design, but now you need to figure out a way to add some new behaviour to all of them - whenever any of them is called a word `SQUEAK` should be printed. The trick is that you can't modify the body of those functions, but still provide that alarm.

It is encouraged (and graded as a bonus) to write some tests for various cases inside your scripts as well