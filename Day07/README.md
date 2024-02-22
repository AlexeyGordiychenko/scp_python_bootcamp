# Day 07 - Python Bootcamp

### Exercise 00: Retirement Plan

You have to design your own version of [Voight-Kampff test](https://bladerunner.fandom.com/wiki/Voight-Kampff_test).
For this you should prepare a set of questions (at least 10 is enough) with three or four responses
to randomly choose from. These questions and answers should be stored in a separate file of any
format (e.g. SQLite or simply JSON).

After each response a set of variables should be typed in manually by a person
asking questions:

- Respiration (measured in BPM, normally around 12-16 breaths per minute)
- Heart rate (normally around 60 to 100 beats per minute)
- Blushing level (categorical, 6 possible levels)
- Pupillary dilation (current pupil size, 2 to 8 mm)

After ten questions and variable measurements, the test should print out a strict binary decision
whether a responding subject is a human or a replicant. In this exercise, you can invent your own
logic to use for making this decision.

Try to split your business logic into separate files based on tasks components solve. The starting 
script should be called `main.py`. All interaction with the test should work via command line.

### Exercise 01: Human Life

You already have the implementation of the test from EX00. But does it really work properly?
In this exercise, you need to write tests to cover all the possible positive and negative cases.

What if the file with questions is empty? Could it be that there is an equal probability for an
output to be human or replicant based on the data?

Your VK test implementation most likely consists of several functions and, supposedly, classes.
Your goal here is to cover all the corner cases for all the components with tests. Basically, 
whenever a test operator inputs something wrong (like, selecting non-existent answer or
out-of-bounds numbers for measurements, e.g. negative heart rate) he or she should receive a
meaningful information message and a possibility to repeat the input.

During this exercise you will most likely rewrite at least some of the code from EX00, but that's
the whole point. Also, it is highly recommended to use Pytest framework when writing tests.
All the tests should be inside `tests` directory.

### Exercise 02: For the Future

You need to use Sphinx project to auto-generate documentation for your code written in EX00/EX01.

The resulting documentation should consist of at least two parts:

- Quickstart, which is the description of how to work with the test
- Auto-generated reference over the code (see link to Sphinx Autodoc in Reading section)

For the first part, you can use either Markdown or RST for the text and formatting.
For the second part, you'll need to add comments to all entities in your code - modules,
functions, classes, etc. You can find a link to the guide on how to write docstrings in Reading
section.

You should also add a proper title and logo to your project for the documentation. Don't include 
the generated docs into your submission though, it should be buildable with `make html` on your 
peer's side if all the requirements are installed.
