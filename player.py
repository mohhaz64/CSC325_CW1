import numpy
from gomokuAgent import GomokuAgent


class Player(GomokuAgent):
    def __init__(self, ID, BOARD_SIZE, X_IN_A_LINE):
        super().__init__(ID, BOARD_SIZE, X_IN_A_LINE)

    def move(self, board):
        # TODO: override move method from GomokuAgent class
        return ()

