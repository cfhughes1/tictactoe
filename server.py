import game

import json
import pickle
import redis
import tornado.ioloop
import tornado.web

KNOWN_KEYS = ["player1", "player2"]

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class GamesHandler(tornado.web.RequestHandler):
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
            update_game(game_id, self.request.body)
        json_data = {"data": pickle.dumps(make_new_game())}
        self.write(json_data)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/api/games/?(\w+)?/?", GamesHandler)
    ])

def get_all_games():
    json_data = {}
    games = []

    keys = db.keys()
    for key in keys:
        games.append(db.get(key))
    json_data["data"] = games

    return json_data

def get_specific_game(game_id):
    json_data = {}
    json_data["data"] = db.get(game_id)
    return json_data

def make_new_game():
    new_game = game.Game()
    db.set(new_game.id, pickle.dumps(new_game))
    return new_game

def update_game(game_id, new_game_data):
    json_data = json.loads(tornado.escape.json_decode(new_game_data))
    for data_point in json_data:
        if data_point in KNOWN_KEYS:
            game_data = pickle.loads(db.get(game_id))
            setattr(game_data, data_point, json_data[data_point])
            db.set(game_id, pickle.dumps(game_data))
    

if __name__ == "__main__":
    db = redis.StrictRedis()
    game1 = game.Game()
    game2 = game.Game()
    db.set(game1.id, pickle.dumps(game1))
    db.set(game2.id, pickle.dumps(game2))
    app = make_app()
    app.listen(8888)
    print 'listening...'
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        db.flushall()
