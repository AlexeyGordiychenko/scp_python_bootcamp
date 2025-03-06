## Make sure you're in the Day05/ folder

## Create and activate virtual enviroment
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## EX00

To run the server use `python3 EX00/exploit.py`. After that you can use `curl` to send requests to the server `http://127.0.0.1:8888` or use `pytest` to run tests.

## EX01

To run the server use `python3 EX01/server.py`. After that you can:

- go to `http://127.0.0.1:8888/` and test the site for audio upload
- use `python3 EX01/screwdriver.py` to use the CLI program to upload or list audio files
- use `pytest` to run tests

## EX02

Use `python3 EX02/doctors.py` to run the script.