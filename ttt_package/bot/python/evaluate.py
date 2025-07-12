from typing import Literal

Board = list[list[Literal["X", "O", ""]]]


def evaluate_board(board: Board) -> float:
    """Basic heuristic: +inf if X wins, -inf if O wins, 0 if draw, between if one side favored."""

    def count_in_line(line, player):
        """Count consecutive pieces in a line for a player."""
        max_count = 0
        current_count = 0

        for cell in line:
            if cell == player:
                current_count += 1
                max_count = max(max_count, current_count)
            else:
                current_count = 0
        return max_count

    def get_score(count):
        """Convert count to score."""
        if count >= 5:
            return float("inf")
        elif count == 4:
            return 5
        elif count == 3:
            return 2
        elif count == 2:
            return 1
        else:
            return 0

    x_score = 0
    o_score = 0
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Check rows
    for row in board:
        x_count = count_in_line(row, "X")
        o_count = count_in_line(row, "O")
        x_score += get_score(x_count)
        o_score += get_score(o_count)

    # Check columns
    for col in range(cols):
        column = [board[row][col] for row in range(rows)]
        x_count = count_in_line(column, "X")
        o_count = count_in_line(column, "O")
        x_score += get_score(x_count)
        o_score += get_score(o_count)

    # Check diagonals (top-left to bottom-right)
    for start_row in range(rows):
        diagonal = []
        row, col = start_row, 0
        while row < rows and col < cols:
            diagonal.append(board[row][col])
            row += 1
            col += 1
        x_count = count_in_line(diagonal, "X")
        o_count = count_in_line(diagonal, "O")
        x_score += get_score(x_count)
        o_score += get_score(o_count)

    for start_col in range(1, cols):
        diagonal = []
        row, col = 0, start_col
        while row < rows and col < cols:
            diagonal.append(board[row][col])
            row += 1
            col += 1
        x_count = count_in_line(diagonal, "X")
        o_count = count_in_line(diagonal, "O")
        x_score += get_score(x_count)
        o_score += get_score(o_count)

    # Check diagonals (top-right to bottom-left)
    for start_row in range(rows):
        diagonal = []
        row, col = start_row, cols - 1
        while row < rows and col >= 0:
            diagonal.append(board[row][col])
            row += 1
            col -= 1
        x_count = count_in_line(diagonal, "X")
        o_count = count_in_line(diagonal, "O")
        x_score += get_score(x_count)
        o_score += get_score(o_count)

    for start_col in range(cols - 2, -1, -1):
        diagonal = []
        row, col = 0, start_col
        while row < rows and col >= 0:
            diagonal.append(board[row][col])
            row += 1
            col -= 1
        x_count = count_in_line(diagonal, "X")
        o_count = count_in_line(diagonal, "O")
        x_score += get_score(x_count)
        o_score += get_score(o_count)

    # Check if board is full (draw)
    is_full = all(cell != "" for row in board for cell in row)

    # Return difference (positive favors X, negative favors O)
    if x_score == float("inf") and o_score == float("inf"):
        return 0  # Both have winning positions
    elif x_score == float("inf"):
        return float("inf")
    elif o_score == float("inf"):
        return float("-inf")
    elif is_full:
        return 0  # Draw - board is full, no winner
    else:
        return x_score - o_score
