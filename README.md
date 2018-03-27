# Tic-Tac-Toe #

# Introduction #
This module is provides an API and backend for playing tic-tac toe.
It should have a frontend, too, but it is still a work in progress.
It was developed on Linux using Python 2.7.12 and Firefoxand has not been tested
on other platforms (yet).

# Setup #
## For basic usage ##
Run the folowing commands:

sudo pip install -r requirements.txt
sudo apt-get install redis-server

## For testing ##
Run the following command:

sudo pip install -r testing-requirements.txt

# To play #
1. Run the following command:

python server.py

2. Navigate in your web browser to:

http://localhost:8888

3. Enter two player names and click Start

4. Contact christinafayehughes2@gmail.com and ask her to finish her code
   so that you can play. :)

# To test #
Run the following command:

py.test

# API Documentation #
Note: all Game objects come pickled and should be unpickled with pickle.loads(myGameObject) for consumption. See code for further documentation.

GET /api/games
Returns a list of games known to the server in the following format:
{"data": [Game1, Game2]}

POST /api/games
Creates a new Game with a randomly-generated ID. Returns new Game instance as:
{"data": Game}

GET /api/games/{id}
Returns a Game by id. Returns 404 if the game id is not in the database. Format:
{"data": Game}

POST /api/games/{id}
Updates a game with new data. Expects json with one or more of the known keys (player1 [string], player2 [string], board [list of bools]). For example:
{"player1": "Bob", "player2": "Sue"}
