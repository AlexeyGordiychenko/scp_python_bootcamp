# Day 06 - Python Bootcamp

### Exercise 00: Kirov Reporting

As gRPC is a client-server communication framework, two components had to be implemented - 
'reporting_server.py' and 'reporting_client.py'. The server should provide a response-streaming
endpoint, where it receives a set of coordinates (it's allowed to use [any particular system](https://en.wikipedia.org/wiki/Astronomical_coordinate_systems)),
and responds with a stream of Spaceship entries.

As this is currently a test environment, even though every Spaceship should still have all the 
parameters mentioned, they could be random. Also, they should be strictly typed, e.g.:
 
 - Alignment is an enum
 - Name is a string
 - Length is a float
 - Class is an enum
 - Size is an integer
 - Armed status is a bool
 - Each officer on board should have first name, last name and rank as strings

The number of officers on board is a random number from 0 (for enemy ships only) to 10.

The workflow should go like this:

1) the server is started
2) the client is started given a set of coordinates in some chosen form, e.g.:
    
`~$ ./reporting_client.py 17 45 40.0409 −29 00 28.118`

  An example given is galactic coordinates for [Sagittarius A\*](https://en.wikipedia.org/wiki/Sagittarius_A*)
3) these coordinates are sent to the server, and server responds with a random (1-10) number
  of Spaceships in a gRPC stream to the client
4) the client prints to standard output all the received ships as a set of serialized JSON
  strings, like:

  ```
  {
    "alignment": "Ally",
    "name": "Normandy",
    "class": "Corvette",
    "length": 216.3,
    "crew_size": 8,
    "armed": true,
    "officers": [{"first_name": "Alan", "last_name": "Shepard", "rank": "Commander"}]
  }
  {
    "alignment": "Enemy",
    "name": "Executor",
    "class": "Dreadnought",
    "length": 19000.0,
    "crew_size": 450,
    "armed": true,
    "officers": []
  }
  ```

NOTE: this output here is formatted for readability, your code can still print one JSON per string

### Exercise 01: Data Quality

List of classes with specific parameters:

| Class       | Length     | Crew    | Can be armed? | Can be hostile? |
|-------------|------------|---------|---------------|-----------------|
| Corvette    | 80-250     | 4-10    | Yes           | Yes             |
| Frigate     | 300-600    | 10-15   | Yes           | No              |
| Cruiser     | 500-1000   | 15-30   | Yes           | Yes             |
| Destroyer   | 800-2000   | 50-80   | Yes           | No              |
| Carrier     | 1000-4000  | 120-250 | No            | Yes             |
| Dreadnought | 5000-20000 | 300-500 | Yes           | Yes             |

Represent these limitations as Pydantic data types.

That way it will not just be easier to validate incoming data, but also serialization to JSON
becomes a lot easier. Make another version of the client ('reporting_client_v2.py'),
which will work with the same server. But this time it should validate the stream of Spaceships 
using Pydantic and filter out those which have some parameters out of bounds, according to the 
table above. The rest should be printed exactly as in EX00.

Additionally, Name could be 'Unknown' ONLY for enemy ships.

### Exercise 02: Keeping Records

How good are reports if we are not storing them? For the last Storage layer there had to be yet
another representation of a Spaceship, now as an ORM model.

Now the project will have to include 'reporting_client_v3.py' script which is responsible
for mapping incoming objects to a database via ORM.

The third version of the client should now not only print out filtered list of spaceships, but also
save them to PostgreSQL database (avoiding storing duplicates, as Name combined with a set of
officers is a unique combination). It is okay if database and user for PostgreSQL are created
manually, as long as there is a description in comments/text file in the submitted project.

Another case that you need to implement is searching for 'traitors'. Sometimes the same
officers (with unique combination of first name, last name and rank) may have been encountered
both on ally and enemy ships. So, the scan interface in version 3 should look like this (mind the 
word 'scan'):

`~$ ./reporting_client.py scan 17 45 40.0409 −29 00 28.118`

And listing of traitors would be

`~$ ./reporting_client.py list_traitors`

which should print a list of JSON strings with "traitors'" names:

```
{"first_name": "Lando", "last_name": "Calrissian", "rank": "Entrepreneur"}
{"first_name": "Red", "last_name": "Guy", "rank": "Impostor"}
```

OPTIONAL BONUS: think about what happens if the storage format will
change. Try using Alembic to generate migrations to bootstrap your database
and then an additional migration with adding the optional "speed" field to the Spaceship model.
