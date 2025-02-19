## Make sure you're in the Day03/ folder

## Create and activate virtual enviroment
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## EX00

`python3 EX00/exploit.py`

## EX01

Make sure you have `docker` installed. Then use `make -C EX01/` to start a container with `Redis`.

Run

`python3 EX01/producer.py`

and then in another terminal run

`python3 EX01/consumer.py -e [comma separated account numbers]`.

Use `make clean -C EX01/` to stop and remove the `Redis` container.

## EX02

To generate `deploy.html` use `python3 EX02/gen_ansible.py`

To deploy the scripts with ansible make sure you have `docker` installed and run `make`. This will run two containers: `app` and `redis`.

The `app` container will be used to test the `deploy.yml` file with `ansible` instrustions.

To see the docker logs you can use `make logs`. To stop the containers use `make down`.