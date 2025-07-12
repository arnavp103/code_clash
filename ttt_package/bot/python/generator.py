"""
# player true means x
"""
# Generate Board
class Evaluation:
    def __init__(self):
        self.turns = 0

    def shit2(self, gameboard, penalty):
        self.turns += 1
        turn = self.turns // 2
        horizontalwin = 0b1111100000
        verticalwin = 0b1000000000
        lrdiagonalwin = [0b1000000000, 0b0100000000, 0b0010000000, 0b0001000000, 0b0000100000, 0b0000010000,
                         0b0000001000, 0b0000000100, 0b0000000010, 0b0000000001]
        rldiagonalwin = [0b0000000001, 0b0000000010, 0b0000000100, 0b0000001000, 0b0000010000, 0b0000100000,
                         0b0001000000, 0b0010000000, 0b0100000000, 0b1000000000]
        closewins = [0b0111100000, 0b0011110000, 0b0001111000, 0b0000111100, 0b0000011110]
        eval = 0.5 - penalty
        # Check for horizontal win
        hw = horizontalwin
        for i in range(5):
            check = [a & hw for a in gameboard]
            for row in check:
                if row == hw:
                    return float('inf')
                rowcount = bin(row).count('1')
                if (rowcount > 1):
                    eval += (0.1 * rowcount)/(turn//4)
            for z in range(10):
                hw = hw >> 1
        # Check for vertical win
        wincount = 0
        vw = verticalwin
        for i in range(10):
            check = [a & vw for a in gameboard]
            for row in check:
                if row == vw:
                    wincount += 1
                else:
                    if (wincount != 1):
                        eval += (0.1 * wincount)/(turn//4)
                    wincount = 0
                if (wincount == 5):
                    return float('inf') # we have a win
            for z in range(10):
                vw = vw >> 1
        # Check for diagonal win
        # first check top to bottom diagonal moving left to right
        dw1 = lrdiagonalwin
        for i in range(5):
            check = [a & b for a, b in zip(gameboard, dw1)]
            for row in check:
                if row == vw[0]:
                    wincount += 1
                else:
                    if (wincount != 1):
                        eval += (0.1 * wincount)/(turn//4)
                    wincount = 0
                if (wincount == 5):
                    return float('inf') # we have a win
            for z in range(10):
                dw1[z] = dw1[z] >> 1
        # second check right to left
        dw1 = lrdiagonalwin
        for i in range(5):
            check = [a & b for a, b in zip(gameboard, dw1)]
            for row in check:
                if row == vw[0]:
                    wincount += 1
                else:
                    if (wincount != 1):
                        eval += (0.1 * wincount)/(turn//4)
                    wincount = 0
                if (wincount == 5):
                    return float('inf')  # we have a win
            for z in range(10):
                dw1[z] = dw1[z] << 1

        # now we check with a bottom to top diagonal
        # first check moving left to right
        dw1 = rldiagonalwin
        for i in range(5):
            check = [a & b for a, b in zip(gameboard, dw1)]
            for row in check:
                if row == vw[0]:
                    wincount += 1
                else:
                    if (wincount != 1):
                        eval += (0.1 * wincount)/(turn//4)
                    wincount = 0
                if (wincount == 5):
                    return float('inf')  # we have a win
            for z in range(10):
                dw1[z] = dw1[z] >> 1
        # second check right to left
        dw1 = rldiagonalwin
        for i in range(5):
            check = [a & b for a, b in zip(gameboard, dw1)]
            for row in check:
                if row == vw[0]:
                    wincount += 1
                else:
                    if (wincount != 1):
                        eval += (0.1 * wincount)/(turn//4)
                    wincount = 0
                if (wincount == 5):
                    return float('inf')  # we have a win
            for z in range(10):
                dw1[z] = dw1[z] << 1
        return 0