# Requirements #
## For basic usage ##
json
pickle
redis
tornado

## For testing ##
py.test
requests

# To play #
python server.py
navigate to http://localhost:8888
enter two player names and click Start
take turns clicking on squares to place your markers

# API Documentation #
Note: all Game objects come pickled and should be unpickled with pickle.loads(myGameObject) for consumption.

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
