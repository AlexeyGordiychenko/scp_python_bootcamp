## Make sure you're in the src/ folder

## Create and activate virtual enviroment
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## EX00

Run the test:
```
python main.py
```
Answer the questions, provide measurements and receive results.

## EX01

Run tests:
```
pytest
```

## EX02

Generate the documentation:

```
make -C docs/ html
```

Open it:

```
open docs/build/html/index.html
```
or run the http server
```
python -m http.server
```
and navigate to http://localhost:8000/docs/build/html/index.html