import random

import numpy as np

from src.ai import win_checker
from src.core import game_logic

ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0

# Preferred column exploration order for optimal Alpha-Beta pruning cutoffs (center-outward)
COLUMN_ORDER = [3, 2, 4, 1, 5, 0, 6]


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 100000
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 50
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 10

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 800

    return score


def score_position(board, piece):
    score = 0
    # Prioritize center column control (Multiplier increased to 6 for strong center dominance)
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 6

    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c : c + 4]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r : r + 4]
            score += evaluate_window(window, piece)

    # Score Positive Diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score Negative Diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board, last_row=None, last_col=None, last_piece=None):
    if last_row is not None and last_piece is not None:
        win, _, _ = win_checker.check_win(board, last_piece, last_row, last_col)
        if win:
            return True, last_piece
    else:
        win_p1, _, _ = win_checker.check_win_full(board, PLAYER_PIECE)
        win_p2, _, _ = win_checker.check_win_full(board, AI_PIECE)
        if win_p1:
            return True, PLAYER_PIECE
        if win_p2:
            return True, AI_PIECE

    if len(get_valid_locations(board)) == 0:
        return True, 0
    return False, None


def get_valid_locations(board):
    # Order columns from center outward [3, 2, 4, 1, 5, 0, 6] for maximum Alpha-Beta pruning efficiency
    valid_locations = []
    for col in COLUMN_ORDER:
        if game_logic.is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def minimax(
    board,
    depth,
    alpha,
    beta,
    maximizingPlayer,
    nodes_count,
    last_row=None,
    last_col=None,
    last_piece=None,
):
    nodes_count[0] += 1
    valid_locations = get_valid_locations(board)

    is_terminal, winning_piece = is_terminal_node(board, last_row, last_col, last_piece)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_piece == AI_PIECE:
                return (None, 10000000000000 + depth, [])
            elif winning_piece == PLAYER_PIECE:
                return (None, -10000000000000 - depth, [])
            else:
                return (None, 0, [])
        else:
            return (None, score_position(board, AI_PIECE), [])

    if maximizingPlayer:
        value = -np.inf
        best_col = random.choice(valid_locations)
        best_pv = []
        for col in valid_locations:
            row = game_logic.get_next_open_row(board, col)
            b_copy = board.copy()
            game_logic.drop_piece(b_copy, row, col, AI_PIECE)

            _, new_score, child_pv = minimax(
                b_copy, depth - 1, alpha, beta, False, nodes_count, row, col, AI_PIECE
            )

            if new_score > value:
                value = new_score
                best_col = col
                best_pv = [col] + child_pv
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value, best_pv

    else:
        value = np.inf
        best_col = random.choice(valid_locations)
        best_pv = []
        for col in valid_locations:
            row = game_logic.get_next_open_row(board, col)
            b_copy = board.copy()
            game_logic.drop_piece(b_copy, row, col, PLAYER_PIECE)

            _, new_score, child_pv = minimax(
                b_copy,
                depth - 1,
                alpha,
                beta,
                True,
                nodes_count,
                row,
                col,
                PLAYER_PIECE,
            )

            if new_score < value:
                value = new_score
                best_col = col
                best_pv = [col] + child_pv
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value, best_pv


def get_best_move(board, depth=5):
    nodes_count = [0]
    col, _, pv_list = minimax(board, depth, -np.inf, np.inf, True, nodes_count)
    predicted_path = pv_list[1:] if len(pv_list) > 1 else []
    return col, nodes_count[0], predicted_path
