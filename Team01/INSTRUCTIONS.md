## Make sure you're in the src/ folder

## Create and activate virtual enviroment
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the game bot:

#### Create a telegram bot for the game:

Open [@BotFather](https://t.me/BotFather) and follow the instructions to create a new bot.

#### Create `.env` file with provided token:
```
TOKEN=[your token]
```

#### Load game’s data:

To fill the database with locations, NPCs, enemies, items etc., use:
```
python3 load_all.py
```

#### Run the game bot:
```
python3 bot.py
```

You can now use the bot in the telegram app. Use /start command to start the game.

### Generate the documentation:

The documentation is generated using Sphinx. It contains all the instruction on how to run the game and play. To generate it, run:
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


### Run the generation bot:

#### Create `.env` file with a bot token:
```
TOKEN_GEN_BOT=[your token]
```

#### Run the bot

```
python3 gen_bot.py
```