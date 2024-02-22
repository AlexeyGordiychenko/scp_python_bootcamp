## Make sure you're in the src/ folder

## Create and activate virtual enviroment
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the gen bot:

#### Create `.env` file with a bot token:
```
TOKEN_GEN_BOT=[your token]
```

#### Run the bot

```
python3 gen_bot.py
```

### Generate the documentation:

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

### To run the game bot, please refer to the documentation