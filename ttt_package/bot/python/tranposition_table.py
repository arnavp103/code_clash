from random import randint
from typing import Literal


def randomInt():
    return randint(0, pow(2, 64))


def indexOf(tile_value: Literal["X", "O"]) -> int:
    match tile_value:
        case "X":
            return 0
        case "O":
            return 1


def init_table():
    ZobristTable = [[[randomInt() for _ in range(2)] for _ in range(10, 2)] for _ in range(10)]
    return ZobristTable


def computeHash(board, ZobristTable: list[list[list[int]]]) -> int:
    h = 0
    for i in range(10):
        for j in range(10):
            if board[i][j] != '':
                piece = indexOf(board[i][j])
                h ^= ZobristTable[i][j][piece]
    return h


