# Day 05 - Python Bootcamp

### Exercise 00: Fool Me Once

Your goal is to implement a WSGI server with an HTTP wrapper without using any external 
dependencies. It should listen on local port 8888 and parse GET parameters from a URL,
for any species title giving you back a JSON (it should be HTTP code 200, also mind the
appropriate 'Content-Type' header and URL encoding). Exaple using cURL might look like this:

```
~$ curl http://127.0.0.1:8888/?species=Time%20Lord
{"credentials": "Rassilon"}
```

If it doesn't know the species passed it should return `{"credentials": "Unknown"}` along with
HTTP status code 404

The whole application for this task should be just a single file `credentials.py`.

The list of species with examples:

```
Cyberman: John Lumic
Dalek: Davros
Judoon: Shadow Proclamation Convention 15 Enforcer
Human: Leonardo da Vinci
Ood: Klineman Halpen
Silence: Tasha Lem
Slitheen: Coca-Cola salesman
Sontaran: General Staal
Time Lord: Rassilon
Weeping Angel: The Division Representative
Zygon: Broton
```

### Exercise 01: Screwdriver Song

This time you need to create a simple WSGI+HTTP client-server application for managing sound files.

First, the server. It shouldn't use any kind of database, just storing files on disk is okay. Web
interface should run on port 8888. When opened, the webpage should show a list of sound files
already uploaded as well as the button for uploading one more. As a user, you should be able to
click on that button, upload the file to the server and it should appear in a list of files shown
on the webpage.

Also, the server should perform a [MIME type](https://en.wikipedia.org/wiki/Media_type) check, so
only audio files are accepted (e.g. `mp3`, `ogg` and `wav`). If a non-audio file is uploaded (e.g.
`jpg`, `exe` or `docx`), it should be discarded and the webpage should show the message "Non-audio
file detected". 

For some bonus points, you can implement playing uploaded sound files directly from the webpage.

This time you are not limited to built-in WSGI server, so it is recommended to use either [Flask](https://flask.palletsprojects.com/)
or [Django](https://www.djangoproject.com/) framework for this task, even though it is not a strict
requirement. Don't forget to add any third-party dependencies you've used into file
`requirements.txt`. Please also include file `README` explaining how to start the HTTP server
(it should contain the specific command to run).

Second, the client. It should be a command-line application with two possible actions:

- `python screwdriver.py upload /path/to/file.mp3` should upload the local audio file
  `/path/to/file.mp3` to the server
- `python screwdriver.py list` should retrieve and print out the names of all the files currently
  present on the server.

All the client-server intercommunication should be using HTTP. It is recommended (though not
strictly required) to use either [Requests](https://docs.python-requests.org/en/latest/) or [HTTPX](https://www.python-httpx.org/) library for
performing HTTP queries.

### Exercise 02: Good Timing

Oh boy. There are five unpredictable time lords at our hands. Think of them as threads, so at any
moment in time there is no way to predict which of them will be acting. So you have to synchronize
their actions somehow.

Each Doctor has a screwdriver it his/her right hand, but the required minimum to act is two. So, 
to get two at a time, the Doctor should grab the screwdriver from another Doctor on the left. But
if everybody does it, then nothing is really changed, as every doctor will still have just one 
screwdriver left.

Start by representing both doctors and screwdrivers as Python classes. Doctors are numbered from 
9 to 13, and everyone of them has to make one blast using two screwdrivers.

*NOTE:* this is a variation of a well-known parallel programming problem usually referred to as 
"Dining Philosophers".

The output of your threaded program should look like this:
```
Doctor 11: BLAST!
Doctor 9: BLAST!
Doctor 12: BLAST!
Doctor 10: BLAST!
Doctor 13: BLAST!
```

The order may be different on each run, because all Doctors (threads) will be competing with one
another for the next turn to grab two screwdrivers. The code itself should be in file `doctors.py`.
