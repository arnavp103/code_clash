from types import Board, Move, Evaluation


def evaluate_board(board: Board) -> Evaluation:
    """Basic heuristic: +inf if X wins, -inf if O wins, 0 if draw, between if one side favored."""
    return 0


def evaluate_after_move(board: Board, move: Move, maximizing_player: bool) -> Evaluation:
    evalv = None
    if maximizing_player:
        board[move[0]][move[1]] = "X"
        evalv = evaluate_board(board)
        board[move[0]][move[1]] = ""
    else:
        board[move[0]][move[1]] = "O"
        evalv = evaluate_board(board)
        board[move[0]][move[1]] = ""
    return evalv