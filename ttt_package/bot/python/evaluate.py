from common import JSONBoard, Player
from generator import Evaluation, Board


def evaluate_board(j_board: JSONBoard, player: Player) -> float:
    eval_obj = Evaluation()
    board = Board(player)
    board.applymoves(j_board)
    return eval_obj.shit2(board.gameboard, 0)
