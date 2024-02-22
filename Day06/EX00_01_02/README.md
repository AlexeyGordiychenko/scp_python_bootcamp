## Make sure you're in the src/ folder and have two terminals open (bash terminal 1, bash terminal 2)

## Create and activate virtual enviroment
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## EX00

#### bash terminal 1:
```
python reporting_server.py
```
#### bash terminal 2:
```
python reporting_client.py 17 45 40.0409 -29 00 28.118
```

## EX01

#### bash terminal 2 (run until a valid spacehip is generated):
```
python reporting_client_v2.py 17 45 40.0409 -29 00 28.118
```
#### run tests with
```
pytest
```

## EX02

#### Create `.env` file with the following content (you can put your own values):
```
POSTGRES_DB=ex02
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5433
```

#### Create the database
```
make start
```

#### bash terminal 2 (run until a valid spacehip is generated):
```
python reporting_client_v3.py scan 17 45 40.0409 -29 00 28.118
```

#### or relaunch the server with `test` argument in bash terminal 1:
```
python reporting_server.py test
```
#### Check for traitors
```
python reporting_client_v3.py list_traitors
```

#### Migrate the database with Alembic
```
make migrate
```

#### Stop the database:

```
make stop
```
