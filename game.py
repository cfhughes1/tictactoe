import random

class Game():
    """ A game of tic-tac-toe

    Attributes:
        id (str): 30-character randomly-assigned identifier
        player1 (str): name of player one
        player1symbol (bool): 0 (for o's) or 1 (for x's)
        player2symbol: name of player two
        player2symbol (bool): 0 (for o's) or 1 (for x's)
        current_turn (bool): the symbol of the player who's turn it is

    """
    def __init__(self):
        self.id = "%030x" % random.randrange(16**30)
        self.player1 = ""
        self.player1symbol = None
        self.player2 = ""
        self.player2symbol = None
        self.board = [None] * 9

        self.current_turn = None
