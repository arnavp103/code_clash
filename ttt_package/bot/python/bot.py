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

import time
import sys
import json
from enum import Enum
from typing import Literal
import evaluate

Board = list[list[Literal["X", "O", ""]]]


class TTFlag(Enum):
    EXACT = 0
    LOWER_BOUND = 1  # Alpha cutoff
    UPPER_BOUND = 2  # Beta cutoff


class TTEntry:
    def __init__(self, depth, value, flag, best_move=None):
        self.depth = depth
        self.value = value
        self.flag = flag
        self.best_move = best_move


class TranspositionTable:
    def __init__(self, size_mb=256):
        # Fixed size hash table to control memory
        self.size = (size_mb * 1024 * 1024) // 32
        self.table = {}

    def store(self, board_hash, depth, value, flag, best_move=None):
        # Always replace for simplicity (could use depth-preferred replacement)
        self.table[board_hash % self.size] = TTEntry(depth, value, flag, best_move)

    def probe(self, board_hash):
        return self.table.get(board_hash % self.size)


class MinimaxBot:
    def __init__(self, eval_function, time_limit=4.8):
        self.evaluate = eval_function
        self.time_limit = time_limit
        self.tt = TranspositionTable()
        self.nodes_searched = 0
        self.time_up = False
        self.start_time = 0
        self.zobrist_table = {}
        self.player = "X"
        self.initialize_zobrist()

    def get_move(self, board):
        self.start_time = time.time()
        self.time_up = False
        best_move = None

        # Get all legal moves
        legal_moves = get_valid_moves(board)
        if len(legal_moves) == 1:
            return legal_moves[0]

        # Iterative deepening
        for depth in range(1, 100):
            self.nodes_searched = 0

            try:
                # Search with current depth
                value, move = self.minimax_root(board, depth)

                # Only update best move if search completed
                if move is not None:
                    best_move = move
                    print(
                        f"Depth {depth}: best_move={move}, value={value:.3f}, nodes={self.nodes_searched}"
                    )

                # Check if we have time for another iteration
                elapsed = time.time() - self.start_time
                if elapsed > self.time_limit * 0.4:  # If 40% time used
                    # Estimate time for next iteration (exponential growth)
                    if self.nodes_searched > 0:
                        time_per_node = elapsed / self.nodes_searched
                        estimated_next = time_per_node * (
                            self.nodes_searched * 3
                        )  # Branching factor estimate
                        if elapsed + estimated_next > self.time_limit * 0.9:
                            break

            except TimeoutError:
                break

        return best_move

    def minimax_root(self, board, depth):
        best_move = None
        best_value = -float("inf")
        alpha = -float("inf")
        beta = float("inf")

        moves = get_valid_moves(board)
        board_hash = self.hash_board(board)
        tt_entry = self.tt.probe(board_hash)

        if tt_entry and tt_entry.best_move and tt_entry.best_move in moves:
            # Put TT move first
            moves.remove(tt_entry.best_move)
            moves.insert(0, tt_entry.best_move)

        # Try each move
        for move in moves:
            child_board = self.make_move(board, move)

            value = -self.alphabeta(child_board, depth - 1, -beta, -alpha, False)

            if value > best_value:
                best_value = value
                best_move = move

            alpha = max(alpha, value)

        # Store in TT
        self.tt.store(board_hash, depth, best_value, TTFlag.EXACT, best_move)

        return best_value, best_move

    def alphabeta(self, board, depth, alpha, beta, maximizing_player):
        # Time check (every N nodes to reduce overhead)
        self.nodes_searched += 1
        if self.nodes_searched % 1000 == 0:
            if time.time() - self.start_time > self.time_limit:
                self.time_up = True
                raise TimeoutError()

        # Transposition table lookup
        board_hash = self.hash_board(board)
        tt_entry = self.tt.probe(board_hash)

        if tt_entry and tt_entry.depth >= depth:
            if tt_entry.flag == TTFlag.EXACT:
                return tt_entry.value
            elif tt_entry.flag == TTFlag.LOWER_BOUND:
                alpha = max(alpha, tt_entry.value)
            elif tt_entry.flag == TTFlag.UPPER_BOUND:
                beta = min(beta, tt_entry.value)

            if alpha >= beta:
                return tt_entry.value

        # Terminal node or depth 0
        if depth == 0 or self.is_game_over(board):
            value = self.evaluate(board)
            self.tt.store(board_hash, 0, value, TTFlag.EXACT)
            return value

        # todo: implement better move ordering
        moves = get_valid_moves(board)

        if maximizing_player:
            value = -float("inf")
            best_move = None
            flag = TTFlag.UPPER_BOUND  # Assume fail-low

            for move in moves:
                child_board = self.make_move(board, move)
                child_value = self.alphabeta(child_board, depth - 1, alpha, beta, False)

                if child_value > value:
                    value = child_value
                    best_move = move

                if value > alpha:
                    alpha = value
                    flag = TTFlag.EXACT  # Found exact value

                if alpha >= beta:
                    flag = TTFlag.LOWER_BOUND
                    break

            self.tt.store(board_hash, depth, value, flag, best_move)
            return value

        else:
            value = float("inf")
            best_move = None
            flag = TTFlag.LOWER_BOUND  # Assume fail-high

            for move in moves:
                child_board = self.make_move(board, move)
                child_value = self.alphabeta(child_board, depth - 1, alpha, beta, True)

                if child_value < value:
                    value = child_value
                    best_move = move

                if value < beta:
                    beta = value
                    flag = TTFlag.EXACT

                if alpha >= beta:
                    flag = TTFlag.UPPER_BOUND  # Fail-low
                    break

            self.tt.store(board_hash, depth, value, flag, best_move)
            return value

    def initialize_zobrist(self):
        # Initialize random numbers for each piece/position
        self.zobrist_table = {}
        import random

        random.seed(42)  # Reproducible

        for row in range(11):
            for col in range(11):
                self.zobrist_table[(row, col, "X")] = random.getrandbits(64)
                self.zobrist_table[(row, col, "O")] = random.getrandbits(64)

    def hash_board(self, board):
        h = 0
        for row in range(len(board)):
            for col in range(len(board[0]) if board else 0):
                piece = board[row][col]
                if (
                    piece != "."
                    and piece != ""
                    and (row, col, piece) in self.zobrist_table
                ):
                    h ^= self.zobrist_table[(row, col, piece)]
        return h

    def is_game_over(self, board):
        return len(get_valid_moves(board)) == 0

    def make_move(self, board, move):
        """write to state.json"""
        row, col = move
        new_board = [list(r) for r in board]
        new_board[row][col] = self.player
        return new_board


def get_valid_moves(board: Board) -> list[tuple[int, int]]:
    """Return list of empty ([row, col]) cells on the board."""
    moves = []
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == "":
                moves.append((i, j))
    return moves


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
        def eval_wrapper(board):
            return evaluate.evaluate_board(board, player)
        
        bot = MinimaxBot(eval_wrapper)
        bot.player = player
        move = bot.get_move(board)
        if move is None:
            # Fallback: return first available move
            valid_moves = get_valid_moves(board)
            if valid_moves:
                move = valid_moves[0]
            else:
                raise ValueError("No valid moves available")
        row, col = move
    except Exception as e:  # pylint: disable=broad-except
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # 3) Output result
    print(json.dumps([row, col]))
    sys.exit(0)


if __name__ == "__main__":
    main()
