## Make sure you're in the Team00/ folder

## Create and activate virtual enviroment
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## EX00

To run `EX00` with the default parameters use:

```bash
python3 EX00/cache_wiki.py
```

You can also specify the article name using the `-p` flag and the depth using the `-d` flag.

To run the neo4j server make sure you have `docker` installed.

First create `.env` file with provided password (should be at least 8 characters):
```
S21_NEO4J_PASS=[your password]
```

Then use `make` to start a container.

After that you can use `python3 EX00/neo4j_db.py EX00/wiki.json` to load the `wiki.json` file into the neo4j database. If you want to load another file you can use `python3 EX00/neo4j_db.py [file]`.

The database will be running on `localhost:7474`, to log in use `neo4j` as the username and the password you provided in the `.env` file.

## EX01

For EX01 to work you need to either add the path to `wiki.json` file to the `WIKI_FILE` environment variable or to specify the path as a command line argument.

If you add it to the `.env` file it should look like this now:

```
S21_NEO4J_PASS=[your password]
WIKI_FILE=EX00/wiki.json
```

To find the shortest path between two pages use:

```bash
python3 EX01/shortest_path.py --from [page1] --to [page2]
```

or with the file specified:

```bash
python3 EX01/shortest_path.py --from [page1] --to [page2] EX00/wiki.json
```

You can also use the `--non-directed` flag to treat all links as 'non-directed' and `-v` flag to print the path.

## EX02

For EX02 to work you need to either add the path to `wiki.json` file to the `WIKI_FILE` environment variable or to specify the path as a command line argument.

If you add it to the `.env` file it should look like this now:

```
S21_NEO4J_PASS=[your password]
WIKI_FILE=EX00/wiki.json
```

To render the graph use:

```bash
python3 EX02/render_graph.py
```

or with the file specified:

```bash
python3 EX02/render_graph.py EX00/wiki.json
```

The graph will be saved as `graph.png` in the EX02 folder.