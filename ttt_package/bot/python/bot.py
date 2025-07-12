#!/usr/bin/env python3
"""
Code Clash Tic Tac Toe Bot Challenge — Python Starter Bot

Welcome to the Code Clash Tic Tac Toe Bot Competition! This is your starter template.
Modify any part of this file to implement your own strategy.

-------------------------------------------
How to package your bot as a single file:
-------------------------------------------
1. Install PyInstaller:
   pip install pyinstaller

2. Build a one-file executable:
   pyinstaller --onefile starter_bot.py

3. Your executable lives in dist/ (e.g., dist/starter_bot.exe)

For rules, move format, and submission details see design_doc.md.
"""
from math import inf
import sys
import json
from evaluate import evaluate_board
from common import *


def get_valid_moves(board: JSONBoard) -> list[Move]:
    """Return list of empty ([row, col]) cells on the board."""
    moves = []
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == "":
                moves.append((i, j))
    return moves


def choose_move(board: JSONBoard, player: Player) -> Move | None:
    """
    Returns a tuple (row, col) from get_valid_moves(board) or None if there are no moves available (tie).
    """
    valid = get_valid_moves(board)
    if not valid:
        return None

    best_eval = -inf
    best_move = None
    for valid_move in valid:
        # Make a hypothetical move
        row, col = valid_move
        board[row][col] = player
        evaluation = alpha_beta_pruning(
            board,
            depth=3,
            maximizing_player=False,
            alpha=float("-inf"),
            beta=float("inf"),
        )
        # Undo the hypothetical move
        board[row][col] = ""

        # flip the evaluation if the player is "O"
        if player == "O":
            evaluation = -evaluation

        if evaluation > best_eval:
            best_eval = evaluation
            best_move = valid_move

    # best_move cannot be None because that would imply that making a move will cause a loss
    return best_move


def alpha_beta_pruning(
        board: JSONBoard,
        depth: int,
        maximizing_player: bool,
        alpha: float = -inf,
        beta: float = inf,
) -> float:
    """
    Minimax algorithm with alpha-beta pruning to evaluate the board position.
    Returns the evaluation score for the current position.
    """
    # Terminal conditions
    if depth == 0:
        return evaluate_board(board, "X" if maximizing_player else "O")

    valid_moves = get_valid_moves(board)
    if not valid_moves:
        return TIE_EVALUATION

    print(
        "Evaluating board at depth",
        depth,
        "for player",
        "X" if maximizing_player else "O",
        end=" ",
        file=sys.stderr,
    )

    value = -inf if maximizing_player else inf
    for row, col in valid_moves:
        # Make move
        board[row][col] = "X"  # Since we are maximizing for "X"
        # Recursive call
        eval_score = alpha_beta_pruning(board, depth - 1, False, alpha, beta)
        # Undo move
        board[row][col] = ""

        if maximizing_player:
            value = max(value, eval_score)

            if value > beta:
                break  # Beta cut-off

            alpha = max(alpha, value)
        else:
            value = min(value, eval_score)

            if value < alpha:
                break  # Alpha cut-off

            beta = min(beta, value)

    print("->", value, file=sys.stderr)
    return value


def main():
    """Main function to run the bot."""
    if len(sys.argv) != 2:
        print("Usage: python starter_bot.py <state.json>", file=sys.stderr)
        sys.exit(1)

    # 1) Load state.json
    try:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            data = json.load(f)
            board = data["board"]
            player = data["player"]
    except Exception as e:  # pylint: disable=broad-except
        print(f"ERROR: Failed to load input: {e}", file=sys.stderr)
        sys.exit(1)

    # 2) Choose move
    try:
        row, col = choose_move(board, player)  # pylint: disable=unpacking-non-sequence
    except Exception as e:  # pylint: disable=broad-except
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # 3) Output result
    print(json.dumps([row, col]))
    sys.exit(0)


if __name__ == "__main__":
    main()
