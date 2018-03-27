import random

class Game():
    def __init__(self):
        self.id = "%030x" % random.randrange(16**30)
        self.player1 = ""
        self.player2 = ""
        self.board = [None] * 9
