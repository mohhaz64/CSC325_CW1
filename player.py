import numpy as np
from gomokuAgent import GomokuAgent

WIN_SCORE = 100000000


def get_set_score(stone_count, open_ends, ai_turn):

    if open_ends == 0 and stone_count < 5:
        return 0

    #case 5
    if stone_count == 5:
        return WIN_SCORE
    #case 4
    elif stone_count == 4:
        if ai_turn:
            return WIN_SCORE
        elif open_ends == 2:
            return WIN_SCORE / 4
        else:
            return 200

    #case 3
    elif stone_count == 3:
        if open_ends == 2:
            if ai_turn:
                return 50000
            else:
                return 200
        else:
            if ai_turn:
                return 10
            else:
                return 5

    #case 2
    elif stone_count == 2:
        if open_ends == 2:
            if ai_turn:
                return 7
            else:
                return 5
        else:
            return 3

    #case 1
    elif stone_count == 1:
        return 1

    return WIN_SCORE * (stone_count - 5)


class Player(GomokuAgent):
    def __init__(self, ID, BOARD_SIZE, X_IN_A_LINE):
        super().__init__(ID, BOARD_SIZE, X_IN_A_LINE)

    def move(self, board):
        move = tuple()
        best_move = self.search_wining_move(board)

        if best_move:
            move = (best_move[0], best_move[1])
        else:
            best_move = self.minimax(board, 3, True)
            if best_move[1]:
                move = None
            else:
                move[0] = best_move[0]
                move[1] = best_move[1]

        return move

    def eval_row(self, board, ai_turn):
        score = 0
        cons_stone_count = 0
        open_ends = 0
        for row in range(self.BOARD_SIZE - 1):
            for col in range(self.BOARD_SIZE - 1):
                cur_pos = board[row][col]

                if cur_pos == self.ID:
                    cons_stone_count += 1

                elif cur_pos == 0:
                    if cons_stone_count > 0:
                        open_ends += 1
                        score += get_set_score(cons_stone_count, open_ends, ai_turn)
                        cons_stone_count = 0
                    open_ends = 1

                elif cons_stone_count > 0:
                    score += get_set_score(cons_stone_count, open_ends, ai_turn)
                    cons_stone_count = 0
                    open_ends = 0

                else:
                    open_ends = 0

            if cons_stone_count > 0:
                score += get_set_score(cons_stone_count, open_ends, ai_turn)
            cons_stone_count = 0
            open_ends = 0
        return score

    def eval_col(self, board, ai_turn):
        board_prime = np.rot90(board)
        score = self.eval_row(board_prime, ai_turn)

        return score

    def eval_diag_tl_br(self, board, ai_turn):
        score = 0
        cons_stone_count = 0
        open_ends = 0
        for row in range(self.BOARD_SIZE - self.X_IN_A_LINE + 1):
            for col in range(self.BOARD_SIZE - self.X_IN_A_LINE + 1):
                for i in range(self.X_IN_A_LINE):
                    cur_pos = board[row+i][col+i]

                    if cur_pos == self.ID:
                        cons_stone_count += 1

                    elif cur_pos == 0:
                        if cons_stone_count > 0:
                            open_ends += 1
                            score += get_set_score(cons_stone_count, open_ends, ai_turn)
                            cons_stone_count = 0
                        open_ends = 1

                    elif cons_stone_count > 0:
                        score += get_set_score(cons_stone_count, open_ends, ai_turn)
                        cons_stone_count = 0
                        open_ends = 0

                    else:
                        open_ends = 0

                if cons_stone_count > 0:
                    score += get_set_score(cons_stone_count, open_ends, ai_turn)
                cons_stone_count = 0
                open_ends = 0

        return score

    def eval_diag_bl_tr(self, board, ai_turn):
        board_prime = np.rot90(board)
        score = self.eval_diag_tl_br(board_prime, ai_turn)
        return score

    def get_score(self, board, ai_turn):
        final_score = self.eval_row(board, ai_turn) + self.eval_col(board, ai_turn) + \
                      self.eval_diag_tl_br(board, ai_turn) + self.eval_diag_bl_tr(board, ai_turn)

        return final_score

    def eval_board(self, board, ai_turn):
        ai_score = self.get_score(board, True)
        opp_score = self.get_score(board, False)

        ai_score = 1 if ai_score == 0 else ai_score
        return ai_score / opp_score

    def gen_possible_moves(self, board):
        possible_moves = set()
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if board[row][col] != 0 : continue
                elif row > 0:
                    if col > 0:
                        if board[row-1][col-1] != 0 or board[row][col-1] != 0:
                            move = (row, col)
                            possible_moves.add(move)
                    elif col < self.BOARD_SIZE - 1:
                        if board[row-1][col+1] != 0 or board[row][col+1] != 0:
                            move = (row, col)
                            possible_moves.add(move)
                    elif board[row-1][col] != 0:
                        move = (row, col)
                        possible_moves.add(move)
                elif row < self.BOARD_SIZE - 1:
                    if col > 0:
                        if board[row+1][col-1] != 0 or board[row][col-1] != 0:
                            move = (row, col)
                            possible_moves.add(move)
                    elif col < self.BOARD_SIZE - 1:
                        if board[row+1][col+1] != 0 or board[row][col+1] != 0:
                            move = (row, col)
                            possible_moves.add(move)
                    elif board[row+1][col] != 0:
                        move = (row, col)
                        possible_moves.add(move)

        return possible_moves

    def search_wining_move(self, board):
        wining_move = []
        possible_moves = self.gen_possible_moves(board)

        for move in possible_moves:
            temp_board = [i for i in board]
            temp_board[move[0]][move[1]] = self.ID
            if self.get_score(temp_board, True) >= WIN_SCORE:
                wining_move = move
                return wining_move

    def minimax(self, board, depth, max_player):
        if depth == 0:
            return self.eval_board(board, max_player)

        possible_moves = self.gen_possible_moves(board)

        if len(possible_moves) == 0:
            return self.eval_board(board, max_player)

        best_move = [0,0,0]

        if max_player:
            best_move[0] = -np.inf
            for move in possible_moves:
                temp_board = [i for i  in board]
                temp_board[move[0]][move[1]] = self.ID
                temp_move = self.minimax(board, depth - 1, False)
                if temp_move[0] > best_move[0]:
                    best_move = temp_move
                    best_move[1] = move[0]
                    best_move[2] = move[1]
        else:
            best_move[0] = np.inf
            best_move[1] = possible_moves[0][0]
            best_move[2] = possible_moves[0][1]
            for move in possible_moves:
                temp_board = [i for i in board]
                temp_board[move[0]][move[1]] = self.ID
                temp_move = self.minimax(board, depth - 1, False)
                if temp_move[0] < best_move[0]:
                    best_move = temp_move
                    best_move[1] = move[0]
                    best_move[2] = move[1]

        return best_move
        
