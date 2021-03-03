import math

import numpy as np

from misc import legalMove, winningTest
from gomokuAgent import GomokuAgent


class Player(GomokuAgent):
    def move(self, board):
        print("Player have move: {}".format(self.ID))
        while True:
            board_next = board.copy()
            m, position_x, position_y = self.max(board_next)
            move_position = (position_x, position_y)
            if legalMove(board, move_position):
                return move_position

    def max(self, board):
        max_score = -math.inf
        first_result = winningTest(self.ID, board, self.X_IN_A_LINE)
        second_result = winningTest(-self.ID, board, self.X_IN_A_LINE)
        position_x = None
        position_y = None

        if first_result is True and second_result is False:
            return 1, 0, 0
        elif first_result is False and second_result is True:
            return -1, 0, 0
        elif (first_result and second_result) is False and 0 not in board:
            return 0, 0, 0

        for i in range(0, self.BOARD_SIZE):
            for j in range(0, self.BOARD_SIZE):
                if board[i][j] == 0:
                    print(board[i][j])
                    board[i][j] = self.ID
                    value, min_x, min_y = self.min(board)
                    if value > max_score:
                        max_score = value
                        position_y = j
                        position_x = i
                    board[i][j] = 0
        print("Max function returns score:{} X:{} Y:{}".format(max_score,position_x,position_y))
        return max_score, position_x, position_y

    def min(self, board):
        min_score = math.inf
        first_result = winningTest(self.ID, board, self.X_IN_A_LINE)
        second_result = winningTest(-self.ID, board, self.X_IN_A_LINE)
        position_x = None
        position_y = None

        if first_result is True and second_result is False:
            return 1, 0, 0
        elif first_result is False and second_result is True:
            print(board)
            print("-1")
            return -1, 0, 0
        elif (first_result and second_result) is False and 0 not in board:
            return 0, 0, 0

        for i in range(0, self.BOARD_SIZE):
            for j in range(0, self.BOARD_SIZE):
                if board[i][j] == 0:
                    board[i][j] = -self.ID
                    value, max_x, max_y = self.max(board)
                    if value < min_score:
                        min_score = value
                        position_y = j
                        position_x = i
                    board[j][i] = 0
        print("Max function returns score:{} X:{} Y:{}".format(min_score, position_x, position_y))
        return min_score, position_x, position_y
