"""
# player true means x
"""
# Generate Board
# gameboard1 = list ()
# for i in range(10):
#     gameboard1.append (["", "", "", "", "" ,"" ,"" ,"" ,"" ,""])
horizontalwin = [0b1111100000, 0b1111100000, 0b1111100000, 0b1111100000, 0b1111100000, 0b1111100000, 0b1111100000, 0b1111100000, 0b1111100000, 0b1111100000]
verticalwin = [0b1000000000, 0b1000000000, 0b1000000000, 0b1000000000, 0b1000000000, 0b1000000000, 0b1000000000, 0b1000000000, 0b1000000000, 0b1000000000]
lrdiagonalwin = [0b1000000000, 0b0100000000, 0b0010000000, 0b0001000000, 0b0000100000, 0b0000010000, 0b0000001000, 0b0000000100, 0b0000000010, 0b0000000001]
rldiagonalwin = [0b0000000001, 0b0000000010, 0b0000000100, 0b0000001000, 0b0000010000, 0b0000100000, 0b0001000000, 0b0010000000, 0b0100000000, 0b1000000000]
# print("{0:b}".format(a))
# print("{0:b}".format(a >> 1))
# print("{0:b}".format(a & (a >> 1)))
def shit2(gameboard, player):
    # Check for horizontal win
    hw = horizontalwin
    for i in range(5):
        check = [a & b for a, b in zip(gameboard, hw)]
        for row in check:
            if row == hw[0]:
                pass # we have a win
        for z in range(10):
            hw[z] = hw[z] >> 1
    # Check for vertical win
    wincount = 0
    vw = verticalwin
    for i in range(10):
        check = [a & b for a, b in zip(gameboard, hw)]
        for row in check:
            if row == vw[0]:
                wincount += 1
            else:
                wincount = 0
            if (wincount == 5):
                pass # we have a win
        for z in range(10):
            vw[z] = vw[z] >> 1
    # Check for diagonal win
    # first check top to bottom diagonal moving left to right
    dw1 = lrdiagonalwin
    for i in range(5):
        check = [a & b for a, b in zip(gameboard, dw1)]
        for row in check:
            if row == vw[0]:
                wincount += 1
            else:
                wincount = 0
            if (wincount == 5):
                pass # we have a win
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
                wincount = 0
            if (wincount == 5):
                pass  # we have a win
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
                wincount = 0
            if (wincount == 5):
                pass  # we have a win
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
                wincount = 0
            if (wincount == 5):
                pass  # we have a win
        for z in range(10):
            dw1[z] = dw1[z] << 1


def shit1(gameboard, player):
    a = 0
    omax = 1
    xmax = 1
    try:
        for row in gameboard:
            for col in row:
                token = gameboard[row][col]
                # check horizontal
                while (a != -1):
                    if (gameboard[row][col + 1] != token):
                        if (token.lower() == "x"):
                            xmax = max(xmax, a)
                        if (token.lower() == "o"):
                            omax = max(omax, a)
                        a = -1
                    else:
                        a = a + 1
                    if (a == 4):
                        raise Exception
                a = 0
                # check diagonal
                while (a != -1):
                    if (gameboard[row + 1][col + 1] != token):
                        if (token.lower() == "x"):
                            xmax = max(xmax, a)
                        if (token.lower() == "o"):
                            omax = max(omax, a)
                        a = -1
                    else:
                        a = a + 1
                    if (a == 4):
                        raise Exception
                # check vertical
                while (a != -1):
                    if (gameboard[row + 1][col] != token):
                        if (token.lower() == "x"):
                            xmax = max(xmax, a)
                        if (token.lower() == "o"):
                            omax = max(omax, a)
                        a = -1
                    else:
                        a = a + 1
                    if (a == 4):
                        raise Exception
        return (xmax -omax )/5 + 0.5
    except:
        if (player):
            return float('inf')
        else:
            return float('-inf')
#
# oyster = [
# ["", "", "", "", "" ,"" ,"" ,"" ,"" ,""],
# ["", "", "", "", "" ,"" ,"" ,"" ,"" ,"o"],
# ["", "", "", "", "" ,"" ,"" ,"x" ,"" ,"x"],
# ["", "", "", "", "" ,"" ,"" ,"" ,"" ,"x"],
# ["", "", "", "", "" ,"" ,"" ,"" ,"" ,"x"],
# ["", "", "", "", "" ,"" ,"" ,"" ,"" ,"o"],
# ["", "", "", "", "" ,"" ,"" ,"" ,"" ,""],
# ["", "", "", "", "" ,"" ,"" ,"" ,"" ,""],
# ["", "", "", "", "" ,"" ,"" ,"" ,"" ,""],
# ["", "", "", "", "" ,"" ,"" ,"" ,"" ,""]
# ]
# print(shit1(oyster, True))
