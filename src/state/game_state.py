import time

from src.ai import minimax, win_checker
from src.core import game_logic


def create_initial_state(mode="pva", session_time=300):
    return {
        "board": game_logic.create_board(),
        "current_player": 1,
        "game_over": False,
        "winner": 0,
        "win_path": [],
        "hover_col": -1,
        "dfs_nodes": 0,
        "dfs_time": 0.0,
        "dfs_explored": set(),
        "ai_nodes": 0,
        "ai_time": 0.0,
        "ai_thinking": False,
        "mode": mode,
        "session_time": session_time,
        "turn_time": 15,
        "consecutive_turns": 1,
        "next_player_bonus_turns": 0,
        "hint_active": False,
        "hint_col": -1,
    }


def switch_turns(state):
    state["consecutive_turns"] -= 1
    state["turn_time"] = 15
    state["hint_active"] = False

    if state["consecutive_turns"] > 0:
        return state

    state["current_player"] = 2 if state["current_player"] == 1 else 1

    if state["next_player_bonus_turns"] > 0:
        state["consecutive_turns"] = state["next_player_bonus_turns"]
        state["next_player_bonus_turns"] = 0
    else:
        state["consecutive_turns"] = 1

    return state


def execute_move(state, col):
    if state["game_over"] or col == -1:
        return state

    board = state["board"]
    player = state["current_player"]

    if game_logic.is_valid_location(board, col):
        row = game_logic.get_next_open_row(board, col)
        game_logic.drop_piece(board, row, col, player)

        start_time = time.perf_counter()
        is_win, path, explored_set = win_checker.check_win(
            board, player, last_row=row, last_col=col
        )
        end_time = time.perf_counter()

        state["dfs_explored"] = explored_set
        state["dfs_nodes"] = len(explored_set)
        state["dfs_time"] = (end_time - start_time) * 1000

        if is_win:
            state["game_over"] = True
            state["winner"] = player
            state["win_path"] = path
        elif game_logic.is_board_full(board):
            state["game_over"] = True
            state["winner"] = -1
        else:
            state = switch_turns(state)

    return state


def apply_hint(state):
    col, _ = minimax.get_best_move(state["board"], depth=5)
    state["hint_col"] = col
    state["hint_active"] = True
    state["next_player_bonus_turns"] = 2
    return state


def tick_timers(state):
    if state["game_over"]:
        return state

    state["session_time"] -= 1
    if state["session_time"] <= 0:
        state["game_over"] = True
        state["winner"] = -1
        return state

    is_human_turn = not (state["mode"] == "pva" and state["current_player"] == 2)

    if is_human_turn and not state["ai_thinking"]:
        state["turn_time"] -= 1
        if state["turn_time"] <= 0:
            state = switch_turns(state)

    return state


def process_ai_turn(state):
    start_time = time.perf_counter()
    best_col, ai_nodes_explored = minimax.get_best_move(state["board"], depth=5)
    end_time = time.perf_counter()

    state["ai_nodes"] = ai_nodes_explored
    state["ai_time"] = (end_time - start_time) * 1000
    state["ai_thinking"] = False

    state = execute_move(state, best_col)

    return state
