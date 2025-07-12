import threading
"""
# player true means x
"""
class Board:
    def __init__(self, xplayer):
        self.gameboard = [0b0000000000, 0b0000000000, 0b0000000000, 0b0000000000, 0b0000000000, 0b0000000000,
                         0b0000000000, 0b0000000000, 0b0000000000, 0b0000000000]
        if xplayer:
            self.player = "X"
        else:
            self.player = "O"

    def applymoves(self, board):
        new = 0b1000000000
        for x in range(len(board)):
            for y in range(len(board[x])):
                if board[x][y] == self.player:
                    p = new >> y
                    self.gameboard[x] = self.gameboard[x] | p

    def checkmove(self, board, x, y):
        new = 0b1000000000
        p = new >> x
        if (board is None):
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
        self.eval = 0

    def print_gameboard(self, gameboard):
        for i in range (10):
            print ("{0:b}".format(gameboard[i]))

    def evaluate(self, factor, penalty):
        a = (0.14 * factor) - (penalty + 10) / 100
        if (a < 0):
            return 0
        return a

    def check_horiz(self, gameboard, turn, eval):
        hw = 0b1111100000
        for i in range(5):
            check = [a & hw for a in gameboard]
            for row in check:
                if row == hw:
                    self.evallock.acquire(blocking=True, timeout=-1)
                    self.eval += float('inf')
                    self.evallock.release()
                rowcount = bin(row).count('1')
                if (rowcount > 1):
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
                    if (wincount != 1):
                        self.evallock.acquire(blocking=True, timeout=-1)
                        self.eval += self.evaluate(wincount, turn)
                        self.evallock.release()
                    wincount = 0
                if (wincount == 5):
                    self.evallock.acquire(blocking=True, timeout=-1)
                    self.eval += float('inf')  # we have a win
                    self.evallock.release()
            vw = vw >> 1
        return 0

    def check_diagonal1(self, gameboard, turn, eval):
        dw1 = [0b1000000000, 0b0100000000, 0b0010000000, 0b0001000000, 0b0000100000, 0b0000010000,
                         0b0000001000, 0b0000000100, 0b0000000010, 0b0000000001]
        for i in range(5):
            wincount = 0
            check = [a & b for a, b in zip(gameboard, dw1)]
            z = 0
            for row in check:
                if (row == dw1[z]) and (row != 0):
                    wincount += 1
                else:
                    if (wincount != 1):
                        self.evallock.acquire(blocking=True, timeout=-1)
                        self.eval += self.evaluate(wincount, turn)
                        self.evallock.release()
                    wincount = 0
                if (wincount == 5):
                    self.evallock.acquire(blocking=True, timeout=-1)
                    self.eval += float('inf')  # we have a win
                    self.evallock.release()
                z += 1
            for z in range(10):
                dw1[z] = dw1[z] >> 1
        return 0

    def check_diagonal2(self, gameboard, turn, eval):
        dw1 = [0b1000000000, 0b0100000000, 0b0010000000, 0b0001000000, 0b0000100000, 0b0000010000,
                         0b0000001000, 0b0000000100, 0b0000000010, 0b0000000001]
        for i in range(5):
            wincount = 0
            check = [a & b for a, b in zip(gameboard, dw1)]
            z = 0
            for row in check:
                if (row == dw1[z]) and (row != 0):
                    wincount += 1
                else:
                    if (wincount != 1):
                        self.evallock.acquire(blocking=True, timeout=-1)
                        self.eval += self.evaluate(wincount, turn)
                        self.evallock.release()
                    wincount = 0
                if (wincount == 5):
                    self.evallock.acquire(blocking=True, timeout=-1)
                    self.eval += float('inf')  # we have a win
                    self.evallock.release()
                z += 1
            for z in range(10):
                dw1[z] = dw1[z] << 1
        return 0

    def check_diagonal3(self, gameboard, turn, eval):
        dw1 = [0b0000000001, 0b0000000010, 0b0000000100, 0b0000001000, 0b0000010000, 0b0000100000,
               0b0001000000, 0b0010000000, 0b0100000000, 0b1000000000]
        for i in range(5):
            wincount = 0
            check = [a & b for a, b in zip(gameboard, dw1)]
            z = 0
            for row in check:
                if (row == dw1[z]) and (row != 0):
                    wincount += 1
                else:
                    if (wincount != 1):
                        self.evallock.acquire(blocking=True, timeout=-1)
                        self.eval += self.evaluate(wincount, turn)
                        self.evallock.release()
                    wincount = 0
                if (wincount == 5):
                    self.evallock.acquire(blocking=True, timeout=-1)
                    self.eval += float('inf')  # we have a win
                    self.evallock.release()
                z += 1
            for z in range(10):
                dw1[z] = dw1[z] >> 1
        return 0
    def check_diagonal4(self, gameboard, turn, eval):
        dw1 = [0b0000000001, 0b0000000010, 0b0000000100, 0b0000001000, 0b0000010000, 0b0000100000,
               0b0001000000, 0b0010000000, 0b0100000000, 0b1000000000]
        for i in range(5):
            wincount = 0
            check = [a & b for a, b in zip(gameboard, dw1)]
            z = 0
            for row in check:
                if (row == dw1[z]) and (row != 0):
                    wincount += 1
                else:
                    if (wincount != 1):
                        self.evallock.acquire(blocking=True, timeout=-1)
                        self.eval += self.evaluate(wincount, turn)
                        self.evallock.release()
                    wincount = 0
                if (wincount == 5):
                    self.evallock.acquire(blocking=True, timeout=-1)
                    self.eval += float('inf')  # we have a win
                    self.evallock.release()
                z += 1
            for z in range(10):
                dw1[z] = dw1[z] << 1
        return 0

    def shit2(self, gameboard, penalty):
        self.turns += 1
        turn = self.turns // 2


        rldiagonalwin = [0b0000000001, 0b0000000010, 0b0000000100, 0b0000001000, 0b0000010000, 0b0000100000,
                         0b0001000000, 0b0010000000, 0b0100000000, 0b1000000000]
        closewins = [0b0111100000, 0b0011110000, 0b0001111000, 0b0000111100, 0b0000011110]
        self.eval = 0
        threads = []
        t = threading.Thread(target=self.check_horiz, args=(gameboard, turn, self.eval))
        threads.append(t)
        t = threading.Thread(target=self.check_vert, args=(gameboard, turn, self.eval))
        threads.append(t)
        t = threading.Thread(target=self.check_diagonal1, args=(gameboard, turn, self.eval))
        threads.append(t)
        t = threading.Thread(target=self.check_diagonal2, args=(gameboard, turn, self.eval))
        threads.append(t)
        t = threading.Thread(target=self.check_diagonal3, args=(gameboard, turn, self.eval))
        threads.append(t)
        t = threading.Thread(target=self.check_diagonal4, args=(gameboard, turn, self.eval))
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
g  = [0b0000000000, 0b0000000000, 0b0010000000, 0b0001000000, 0b0000100000, 0b0000000000,
                         0b0000001000, 0b0000000000, 0b0000000000, 0b0000000000]
print(b.shit2(g, 0))