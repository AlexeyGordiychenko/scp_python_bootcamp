# Day 00 - Python Bootcamp

### Exercise 00: Blockchain

Write a Python script which will be able to receive a text from its standard input, and then
print out only those lines that start with exactly 5 zeroes.

Keep in mind that the data has been corrupted, so you have to be very careful. 
That means, only lines that fit into certain criteria are considered valid:

- Correct lines are 32 characters long
- They start with exactly 5 zeroes, so e.g. line starting with 6 zeroes is NOT
  considered correct

So, for the example above your script should print:

```
00000254b208c0f43409d8dc00439896
0000085a34260d1c84e89865c210ceb4
0000071f49cffeaea4184be3d507086v
```

Your code should accept the number of lines as an argument, like this:

`~$ cat data_hashes_10lines.txt | python blocks.py 10`

This way the program will stop when it processed 10 lines. Keep in mind that in this approach
the program may hang if the number of lines in a file is smaller than the one in the argument.
This is not considered an error.

### Exercise 01: Decypher

Write a Python script that can be used to decrypt the messages like "The only way
everyone reaches Brenda rapidly is delivering groceries explicitly" or 
"Britain is Great because everyone necessitates". It should be launchable like this:

`~$ python decypher.py "Have you delivered eggplant pizza at restored keep?"`

and print out the answer as a single word without spaces.

### Exercise 02: Track and Capture

As an input your code is given a 2d "image" as text in a file `m.txt`. File contains five
characters over three lines, like this:

```
*d&t*
**h**
*l*!*
```

You may notice that there is a pattern of stars here, with a letter M. All
your code has to do is to print 'True' if this M-pattern exists in a given
input image or 'False' otherwise. Other characters (outside the M pattern)
should be different, so these examples should print out 'False':

```
*****
*****
*****
```

```
*s*f*
**f**
*a***
```

If a given pattern is not 3x5, then 'Error' word should be printed instead.
The file with code should be named `mfinder.py`.
