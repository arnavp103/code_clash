# Generate Board
gameboard = list ()
for i in range(10):
    gameboard.append (["", "", "", "", "" ,"" ,"" ,"" ,"" ,""])

# player true means x
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


