import game

import json
import pickle
import random
import redis
import tornado.ioloop
import tornado.web

# TODO(christina): read Game keys instead of hard-coding
KNOWN_KEYS = ["player1", "player2", "player1symbol", "player2symbol", "board"]


class MainHandler(tornado.web.RequestHandler):
    """ Main handler for base URL.

    GET renders welcome page where the user enters player info
        and starts new game. """
    def get(self):
        self.render("welcome.html")


class GamesHandler(tornado.web.RequestHandler):
    """ Games handler for API.

    GET /api/games/{game_id (optional)}
        Returns either all games known to server (if no game_id) or the
        specific game requested. Games come as pickled Game instances.

        404 status code if game_id not found in server.

        Response format (no game_id):
        {"data": [Game1, Game2, ..., GameN]}

        Response format (game_id included):
        {"data": Game}

    POST /api/games/{game_id (optional)}
        Returns a new game instance if no game_id. If game_id is included,
        updates specified game's data in database.

        Expects json payload in format {"key1": "val1", ..., "keyN, valN"}
        where key1 ... keyN are known keys.
        KNOWN_KEYS = ["player1",
                      "player2",
                      "player1symbol",
                      "player2symbol",
                      "board"]

        404 status code if game_id not found in server.

        Response format (no game_id):
        {"data": Game}

    """
    def get(self, game_id):
        if game_id:
            specific_game = get_specific_game(game_id)
            if specific_game["data"] is not None:
                self.write(get_specific_game(game_id))
            else:
                self.set_status(404)
        else:
            self.write(get_all_games())

    def post(self, game_id):
        if game_id:
            game_to_update = db.get(game_id)
            if game_to_update is not None:
                update_game(game_id, self.request.body)
            else:
                self.set_status(404)
        else:
            new_game = make_new_game()
            if self.request.body:
                update_game(new_game.id, self.request.body)
            json_data = {"data": db.get(new_game.id)}
            self.write(json_data)


class GamePlayHandler(tornado.web.RequestHandler):
    # TODO(christina): complete gameplay functionality
    """ Displays gameboard and handles updates.
        **Incomplete**

    GET /gameplay
        Renders gameboard that currently can not be played on. :(
    """
    def get(self):
        new_game = make_new_game()

        game_data = {}
        game_data["player1"] = self.get_argument("player1")
        game_data["player1symbol"] = bool(random.getrandbits(1))
        game_data["player2"] = self.get_argument("player2")
        game_data["player2symbol"] = not game_data["player1symbol"]

        update_game(new_game.id, game_data)

        self.write(str(game_data["player1symbol"]))
        self.write(str(game_data["player2symbol"]))

        self.render("board.html")

def make_app():
    """ Returns a new tornado.web.Application """
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/api/games/?(\w+)?/?", GamesHandler),
        (r"/gameplay/?", GamePlayHandler)
    ])

def get_all_games():
    """ Retrieve all known games from the database.

    Returns:
        json_data: dict of games in form {"data": [Game1, Game2, ..., GameN]}
                   where Game1 ... GameN are pickled Game instances
    """
    json_data = {}
    games = []

    keys = db.keys()
    for key in keys:
        games.append(db.get(key))
    json_data["data"] = games

    return json_data

def get_specific_game(game_id):
    """ Retrieve a specific game from the database.

    Args:
        game_id (str): id attribute of the Game instance
    Returns:
        json_data (dict): dict of game in form {"data": Game}
                          where Game is the pickled Game instance
    """
    json_data = {}
    json_data["data"] = db.get(game_id)
    return json_data

def make_new_game():
    """ Generates a new game with random id and saves to the database.

    Returns:
        new_game (Game): new Game instance
    """
    new_game = game.Game()
    db.set(new_game.id, pickle.dumps(new_game))
    return new_game

def update_game(game_id, new_game_data):
    """ Updates a Game in the database with new data.
        Will break if game_id is not known.

    Args:
        game_id (str): id attribute of the Game instance
        new_game_data (dict or str of dict): New data with known keys.
                                             Ignores unknown keys.
    """
    if isinstance(new_game_data, str):
        new_game_data = json.loads(tornado.escape.json_decode(new_game_data))
    for data_point in new_game_data:
        if data_point in KNOWN_KEYS:
            game_data = pickle.loads(db.get(game_id))
            setattr(game_data, data_point, new_game_data[data_point])
            db.set(game_id, pickle.dumps(game_data))
    

if __name__ == "__main__":
    db = redis.StrictRedis()
    app = make_app()
    app.listen(8888)
    print 'listening...'

    # by default, when the user exists the server we'll clear the database
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        db.flushall()
