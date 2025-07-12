# from typing import Literal

# Board = list[list[Literal["X", "O", ""]]]


# def evaluate_board(board: Board) -> float:
#     """Basic heuristic: +inf if X wins, -inf if O wins, 0 if draw, between if one side favored."""

#     def count_in_line(line, player):
#         """Count consecutive pieces in a line for a player."""
#         max_count = 0
#         current_count = 0

#         for cell in line:
#             if cell == player:
#                 current_count += 1
#                 max_count = max(max_count, current_count)
#             else:
#                 current_count = 0
#         return max_count

#     def get_score(count):
#         """Convert count to score."""
#         if count >= 5:
#             return float("inf")
#         elif count == 4:
#             return 5
#         elif count == 3:
#             return 2
#         elif count == 2:
#             return 1
#         else:
#             return 0

#     x_score = 0
#     o_score = 0
#     rows = len(board)
#     cols = len(board[0]) if rows > 0 else 0

#     # Check rows
#     for row in board:
#         x_count = count_in_line(row, "X")
#         o_count = count_in_line(row, "O")
#         x_score += get_score(x_count)
#         o_score += get_score(o_count)

#     # Check columns
#     for col in range(cols):
#         column = [board[row][col] for row in range(rows)]
#         x_count = count_in_line(column, "X")
#         o_count = count_in_line(column, "O")
#         x_score += get_score(x_count)
#         o_score += get_score(o_count)

#     # Check diagonals (top-left to bottom-right)
#     for start_row in range(rows):
#         diagonal = []
#         row, col = start_row, 0
#         while row < rows and col < cols:
#             diagonal.append(board[row][col])
#             row += 1
#             col += 1
#         x_count = count_in_line(diagonal, "X")
#         o_count = count_in_line(diagonal, "O")
#         x_score += get_score(x_count)
#         o_score += get_score(o_count)

#     for start_col in range(1, cols):
#         diagonal = []
#         row, col = 0, start_col
#         while row < rows and col < cols:
#             diagonal.append(board[row][col])
#             row += 1
#             col += 1
#         x_count = count_in_line(diagonal, "X")
#         o_count = count_in_line(diagonal, "O")
#         x_score += get_score(x_count)
#         o_score += get_score(o_count)

#     # Check diagonals (top-right to bottom-left)
#     for start_row in range(rows):
#         diagonal = []
#         row, col = start_row, cols - 1
#         while row < rows and col >= 0:
#             diagonal.append(board[row][col])
#             row += 1
#             col -= 1
#         x_count = count_in_line(diagonal, "X")
#         o_count = count_in_line(diagonal, "O")
#         x_score += get_score(x_count)
#         o_score += get_score(o_count)

#     for start_col in range(cols - 2, -1, -1):
#         diagonal = []
#         row, col = 0, start_col
#         while row < rows and col >= 0:
#             diagonal.append(board[row][col])
#             row += 1
#             col -= 1
#         x_count = count_in_line(diagonal, "X")
#         o_count = count_in_line(diagonal, "O")
#         x_score += get_score(x_count)
#         o_score += get_score(o_count)

#     # Check if board is full (draw)
#     is_full = all(cell != "" for row in board for cell in row)

#     # Return difference (positive favors X, negative favors O)
#     if x_score == float("inf") and o_score == float("inf"):
#         return 0  # Both have winning positions
#     elif x_score == float("inf"):
#         return float("inf")
#     elif o_score == float("inf"):
#         return float("-inf")
#     elif is_full:
#         return 0  # Draw - board is full, no winner
#     else:
#         return x_score - o_score

import threading
from typing import Literal

type JSONBoard = list[list[Literal["X", "O", ""]]]
type Move = tuple[int, int]
type Player = Literal["X", "O"]
type BitBoard = list[int]

TIE_EVALUATION: float = 0


def evaluate_board(j_board: JSONBoard, player: Player) -> float:
    eval_obj = Evaluation()
    board = Board(player)
    board.applymoves(j_board)
    return eval_obj.shit2(board.gameboard, 0)


class Board:
    def __init__(self, player: Player):
        self.gameboard: BitBoard = [
            0b0000000000,
            0b0000000000,
            0b0000000000,
            0b0000000000,
            0b0000000000,
            0b0000000000,
            0b0000000000,
            0b0000000000,
            0b0000000000,
            0b0000000000,
        ]
        self.player = player

    def applymoves(self, board: JSONBoard):
        new = 0b1000000000
        for x in range(len(board)):
            for y in range(len(board[x])):
                if board[x][y] == self.player:
                    p = new >> y
                    self.gameboard[x] = self.gameboard[x] | p

    def checkmove(self, board: BitBoard, x, y):
        new = 0b1000000000
        p = new >> x
        if board is None:
            test = self.gameboard.copy()
        else:
            test = board.copy()
        test[y] = test[y] | p
        return test


# Generate Board
class Evaluation:
    def __init__(self):
        self.turns = 1
        self.evallock = threading.Lock()
        self.eval = TIE_EVALUATION

    def print_gameboard(self, gameboard):
        for i in range(10):
            print("{0:b}".format(gameboard[i]))

    def evaluate(self, factor, penalty):
        a = (0.14 * factor) - (penalty + 10) / 100
        if a < 0:
            return 0
        return a

    def check_horiz(self, gameboard, turn, eval):
        hw = 0b1111100000
        for i in range(5):
            check = [a & hw for a in gameboard]
            for row in check:
                if row == hw:
                    self.evallock.acquire(blocking=True, timeout=-1)
                    self.eval += float("inf")
                    self.evallock.release()
                    return 0
                rowcount = bin(row).count("1")
                if rowcount > 1:
                    self.evallock.acquire(blocking=True, timeout=-1)
                    self.eval += self.evaluate(rowcount, turn)
                    self.evallock.release()
            hw = hw >> 1
        return 0

    def check_vert(self, gameboard, turn, eval):
        verticalwin = 0b1000000000
        vw = verticalwin
        for i in range(10):
            wincount = 0
            check = [a & vw for a in gameboard]
            for row in check:
                if row == vw:
                    wincount += 1
                else:
                    if wincount != 1:
                        self.evallock.acquire(blocking=True, timeout=-1)
                        self.eval += self.evaluate(wincount, turn)
                        self.evallock.release()
                    wincount = 0
                if wincount == 5:
                    self.evallock.acquire(blocking=True, timeout=-1)
                    self.eval += float("inf")  # we have a win
                    self.evallock.release()
                    return 0
            vw = vw >> 1
        return 0

    def check_diagonal1(self, gameboard, turn, eval):
        dw1 = [
            0b1000000000,
            0b0100000000,
            0b0010000000,
            0b0001000000,
            0b0000100000,
            0b0000010000,
            0b0000001000,
            0b0000000100,
            0b0000000010,
            0b0000000001,
        ]
        for i in range(5):
            wincount = 0
            check = [a & b for a, b in zip(gameboard, dw1)]
            z = 0
            for row in check:
                if (row == dw1[z]) and (row != 0):
                    wincount += 1
                else:
                    if wincount != 1:
                        self.evallock.acquire(blocking=True, timeout=-1)
                        self.eval += self.evaluate(wincount, turn)
                        self.evallock.release()
                    wincount = 0
                if wincount == 5:
                    self.evallock.acquire(blocking=True, timeout=-1)
                    self.eval += float("inf")  # we have a win
                    self.evallock.release()
                    return 0
                z += 1
            for z in range(10):
                dw1[z] = dw1[z] >> 1
        return 0

    def check_diagonal2(self, gameboard, turn, eval):
        dw1 = [
            0b1000000000,
            0b0100000000,
            0b0010000000,
            0b0001000000,
            0b0000100000,
            0b0000010000,
            0b0000001000,
            0b0000000100,
            0b0000000010,
            0b0000000001,
        ]
        for i in range(5):
            wincount = 0
            check = [a & b for a, b in zip(gameboard, dw1)]
            z = 0
            for row in check:
                if (row == dw1[z]) and (row != 0):
                    wincount += 1
                else:
                    if wincount != 1:
                        self.evallock.acquire(blocking=True, timeout=-1)
                        self.eval += self.evaluate(wincount, turn)
                        self.evallock.release()
                    wincount = 0
                if wincount == 5:
                    self.evallock.acquire(blocking=True, timeout=-1)
                    self.eval += float("inf")  # we have a win
                    self.evallock.release()
                    return 0
                z += 1
            for z in range(10):
                dw1[z] = dw1[z] << 1
        return 0

    def check_diagonal3(self, gameboard, turn, eval):
        dw1 = [
            0b0000000001,
            0b0000000010,
            0b0000000100,
            0b0000001000,
            0b0000010000,
            0b0000100000,
            0b0001000000,
            0b0010000000,
            0b0100000000,
            0b1000000000,
        ]
        for i in range(5):
            wincount = 0
            check = [a & b for a, b in zip(gameboard, dw1)]
            z = 0
            for row in check:
                if (row == dw1[z]) and (row != 0):
                    wincount += 1
                else:
                    if wincount != 1:
                        self.evallock.acquire(blocking=True, timeout=-1)
                        self.eval += self.evaluate(wincount, turn)
                        self.evallock.release()
                    wincount = 0
                if wincount == 5:
                    self.evallock.acquire(blocking=True, timeout=-1)
                    self.eval += float("inf")  # we have a win
                    self.evallock.release()
                    return 0
                z += 1
            for z in range(10):
                dw1[z] = dw1[z] >> 1
        return 0

    def check_diagonal4(self, gameboard, turn, eval):
        dw1 = [
            0b0000000001,
            0b0000000010,
            0b0000000100,
            0b0000001000,
            0b0000010000,
            0b0000100000,
            0b0001000000,
            0b0010000000,
            0b0100000000,
            0b1000000000,
        ]
        for i in range(5):
            wincount = 0
            check = [a & b for a, b in zip(gameboard, dw1)]
            z = 0
            for row in check:
                if (row == dw1[z]) and (row != 0):
                    wincount += 1
                else:
                    if wincount != 1:
                        self.evallock.acquire(blocking=True, timeout=-1)
                        self.eval += self.evaluate(wincount, turn)
                        self.evallock.release()
                    wincount = 0
                if wincount == 5:
                    self.evallock.acquire(blocking=True, timeout=-1)
                    self.eval += float("inf")  # we have a win
                    self.evallock.release()
                    return 0
                z += 1
            for z in range(10):
                dw1[z] = dw1[z] << 1
        return 0

    def shit2(self, gameboard: BitBoard, penalty):
        self.turns += 1
        turn = self.turns // 2

        rldiagonalwin = [
            0b0000000001,
            0b0000000010,
            0b0000000100,
            0b0000001000,
            0b0000010000,
            0b0000100000,
            0b0001000000,
            0b0010000000,
            0b0100000000,
            0b1000000000,
        ]
        closewins = [
            0b0111100000,
            0b0011110000,
            0b0001111000,
            0b0000111100,
            0b0000011110,
        ]
        self.eval = 0
        threads = []
        t = threading.Thread(target=self.check_horiz, args=(gameboard, turn, self.eval))
        threads.append(t)
        t = threading.Thread(target=self.check_vert, args=(gameboard, turn, self.eval))
        threads.append(t)
        t = threading.Thread(
            target=self.check_diagonal1, args=(gameboard, turn, self.eval)
        )
        threads.append(t)
        t = threading.Thread(
            target=self.check_diagonal2, args=(gameboard, turn, self.eval)
        )
        threads.append(t)
        t = threading.Thread(
            target=self.check_diagonal3, args=(gameboard, turn, self.eval)
        )
        threads.append(t)
        t = threading.Thread(
            target=self.check_diagonal4, args=(gameboard, turn, self.eval)
        )
        threads.append(t)
        # Start each thread
        for t in threads:
            t.start()

        # Wait for all threads to finish
        for t in threads:
            t.join()

        return self.eval
        # t = threading.Thread(target=self.check_horiz, args=(gameboard, turn, eval))
        # threads.append(t)
        # t = threading.Thread(target=self.check_horiz, args=(gameboard, turn, eval))
        # threads.append(t)
        # Check for horizontal win

        # Check for vertical win

        # Check for diagonal win
        # first check top to bottom diagonal moving left to right

        # second check right to left

        # now we check with a bottom to top diagonal
        # first check moving left to right

        # second check right to left


b = Evaluation()
# [0b0000000000, 0b0000000000, 0b0000000000, 0b0000000000, 0b0000000000, 0b0000000000,
#                          0b0000000000, 0b0000000000, 0b0000000000, 0b0000000000]
g = [
    0b0000000000,
    0b0000000000,
    0b0010000000,
    0b0001000000,
    0b0000100000,
    0b0000000000,
    0b0000001000,
    0b0000000000,
    0b0000000000,
    0b0000000000,
]
print(b.shit2(g, 0))
