Installation
===============================

To run the Game you need to follow these instructions (make sure you're in the src/folder):

#. **Enviroment:**
    Create and activate virtual enviroment with
    ::

        python3 -m venv .venv
        source .venv/bin/activate
        pip install -r requirements.txt

#. **Create a telegram bot for the game:**
    Open `BotFather <https://t.me/BotFather>`__ and follow the instructions to create a new bot.
    Create *.env* file with provided token:
    ::

        TOKEN='your token'

#. **Load game's data:**
    To fill the database with locations, NPCs, enemies, items etc., use:
    ::

        python3 load_all.py

#. **Run the game bot:**
    To run the bot use:
    ::

        python3 bot.py

    You can now use the bot in the telegram app. Use */start* command to start the game.