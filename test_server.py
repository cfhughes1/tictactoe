import game

import pickle
import json
import requests

import sys
sys.modules['game'] = game

BASE_URL = "http://localhost:8888"

""" Test helper functions """
def build_games_url():
    return BASE_URL + "/api/games/"

def make_new_game():
    r = requests.post(build_games_url())
    r.raise_for_status
    print json.loads(r.text)
    return pickle.loads(json.loads(r.text)["data"])

""" Tests """
def test_get_games():
    r = requests.get(build_games_url())
    r.raise_for_status()
    assert json.loads(r.text)

def test_post_game():
    new_game = make_new_game()
    assert new_game.id is not None

def test_get_specific_game():
    new_game_id = make_new_game().id
    r = requests.get(build_games_url() + new_game_id)
    r.raise_for_status()
    print json.loads(r.text)["data"]
    assert isinstance(pickle.loads(json.loads(r.text)["data"]), game.Game)

def test_getting_nonexistent_game():
    r = requests.get(build_games_url() + "totallynotagameid")
    assert r.status_code == 404

def test_posting_new_game_data():
    new_game = make_new_game()
    r_before = requests.post(build_games_url() + new_game.id, json='{"player1": "wade"}')
    r_before.raise_for_status()
    r_after = requests.get(build_games_url() + new_game.id)
    r_after.raise_for_status()
    assert pickle.loads(json.loads(r_after.text)["data"]).player1 == "wade"
