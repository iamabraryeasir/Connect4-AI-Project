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
                return (None, 10000000000000 + depth)
            elif winning_piece == PLAYER_PIECE:
                return (None, -10000000000000 - depth)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI_PIECE))

    if maximizingPlayer:
        value = -np.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = game_logic.get_next_open_row(board, col)
            b_copy = board.copy()
            game_logic.drop_piece(b_copy, row, col, AI_PIECE)

            _, new_score = minimax(
                b_copy, depth - 1, alpha, beta, False, nodes_count, row, col, AI_PIECE
            )

            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value

    else:
        value = np.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = game_logic.get_next_open_row(board, col)
            b_copy = board.copy()
            game_logic.drop_piece(b_copy, row, col, PLAYER_PIECE)

            _, new_score = minimax(
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
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value


def get_best_move(board, depth=5, blunder_rate=0.0, diagnostics=False):
    valid_locations = get_valid_locations(board)
    if not valid_locations:
        return 0, 0

    is_blunder = blunder_rate > 0.0 and random.random() < blunder_rate
    if is_blunder and not diagnostics:
        return random.choice(valid_locations), 1

    if diagnostics:
        nodes_count = [0]
        candidate_scores = {}
        candidate_heuristics = {}
        best_col = None
        best_score = -np.inf

        for candidate_col in valid_locations:
            row = game_logic.get_next_open_row(board, candidate_col)
            candidate_board = board.copy()
            game_logic.drop_piece(candidate_board, row, candidate_col, AI_PIECE)
            candidate_heuristics[candidate_col] = score_position(
                candidate_board, AI_PIECE
            )

            _, candidate_score = minimax(
                candidate_board,
                depth - 1,
                -np.inf,
                np.inf,
                False,
                nodes_count,
                row,
                candidate_col,
                AI_PIECE,
            )
            candidate_scores[candidate_col] = int(candidate_score)
            if candidate_score > best_score:
                best_score = candidate_score
                best_col = candidate_col

        chosen_col = random.choice(valid_locations) if is_blunder else best_col
        chosen_score = candidate_scores[chosen_col]

        print(f"\n--- Minimax Evaluation (Depth: {depth}) ---")
        for candidate_col in sorted(valid_locations):
            heuristic_score = candidate_heuristics[candidate_col]
            center_count = sum(
                int(piece) == AI_PIECE for piece in board[:, COLUMN_COUNT // 2]
            )
            center_score = center_count * 6
            # The candidate heuristic includes the newly placed piece's center bonus.
            if candidate_col == COLUMN_COUNT // 2:
                center_score += 6
            pattern_score = heuristic_score - center_score
            marker = " -> BEST" if candidate_col == best_col else ""
            if is_blunder and candidate_col == chosen_col:
                marker = " -> CHOSEN (BLUNDER)"
            print(
                f"  Column {candidate_col}: score = "
                f"{candidate_scores[candidate_col]:+d} (minimax) | "
                f"heuristic = {center_score:+d}(center) + "
                f"{pattern_score:+d}(patterns) = {heuristic_score:+d}{marker}"
            )
        print(f"Chosen move: Column {chosen_col} (score: {chosen_score})")
        print(f"Nodes explored: {nodes_count[0]}")
        print("-------------------------------------------")
        return chosen_col, nodes_count[0]

    nodes_count = [0]
    col, _ = minimax(board, depth, -np.inf, np.inf, True, nodes_count)
    if col is None or col not in valid_locations:
        col = random.choice(valid_locations)
    return col, nodes_count[0]
