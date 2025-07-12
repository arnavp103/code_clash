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

import sys
import json
from typing import Literal
from types import Board, Move, EvaluatedMove
from evaluate import evaluate_board
from GameTree import GameTree

tree = GameTree(None, None, None)


def get_valid_moves(board: Board) -> list[Move]:
    """Return list of empty ([row, col]) cells on the board."""
    moves = []
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == "":
                moves.append((i, j))
    return moves


def choose_move(board: Board, player: Literal["X"] | Literal["O"]) -> Move:
    """
    Should return a tuple (row, col) from get_valid_moves(board).
    """

    evaluation, move = alpha_beta_pruning(
        board,
        tree,
        depth=3,
        maximizing_player=True if player == "X" else False,
        alpha=float("-inf"),
        beta=float("inf"),
    )

    return move


def alpha_beta_pruning(
        board: Board,
        gtree: GameTree,
        depth: int,
        maximizing_player: bool,
        alpha: float = float("-inf"),
        beta: float = float("inf"),
) -> EvaluatedMove:
    """
    Minimax algorithm with alpha-beta pruning to evaluate the board position.
    """
    # Terminal conditions
    if depth == 0:
        return evaluate_board(board), gtree.move_from_parent

    valid_moves = get_valid_moves(board)
    if not valid_moves:
        raise ValueError("No valid moves available")

    print(
        "Evaluating board at depth",
        depth,
        "for player",
        "X" if maximizing_player else "O",
        end=" ",
    )

    value = float("-inf")
    best_move: Move | None = None
    for move in valid_moves:
        row, col = move
        # Make move
        board[row][col] = "X"  # Since we are maximizing for "X"
        gtree.add_child(move, None)
        # Recursive call
        eval_score, _ = alpha_beta_pruning(board, gtree.children[move], depth - 1, False, alpha, beta)
        # Undo move
        board[row][col] = ""
        gtree.children[move].evalv = eval_score

        if maximizing_player:
            if value < eval_score:
                best_move = move
            if value > beta:
                gtree.pruned = True
                break  # Beta cut-off
            alpha = max(alpha, value)
        else:
            if value > eval_score:
                best_move = move
            if value < alpha:
                gtree.pruned = True
                break  # Alpha cut-off

            beta = min(beta, value)
    print("->", value)
    return value, best_move


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
