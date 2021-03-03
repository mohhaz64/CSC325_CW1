import math

from time import time

from misc import legalMove, winningTest, rowTest, diagTest
from gomokuAgent import GomokuAgent


class Player(GomokuAgent):
    def move(self, board):
        t = time()
        while True:
            m, position_x, position_y = self.max(board, 0)
            move_position = (position_x, position_y)
            if legalMove(board, move_position):
                t1 = time()
                print("Time to do move: ", t1-t)
                return move_position

    def max(self, board, depth):
        depth += 1
        max_score = -2
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
                    board[i][j] = self.ID
                    value, min_x, min_y = self.min(board, depth)
                    if value > max_score:
                        max_score = value
                        position_x = i
                        position_y = j
                    board[i][j] = 0
        return max_score, position_x, position_y

    def min(self, board, depth):
        min_score = 2
        depth +=1
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
                    board[i][j] = -self.ID
                    value, max_x, max_y = self.max(board, depth)
                    if value < min_score:
                        min_score = value
                        position_x = i
                        position_y = j
                    board[i][j] = 0
        return min_score, position_x, position_y
