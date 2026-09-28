import time
from typing import Any

from src.ai import minimax, win_checker
from src.core import game_logic
from src.levels.level_config import LevelConfig, get_level
from src.profile.profile_manager import ProfileManager


def create_initial_state(
    mode: str = "campaign",
    level_id: int = 1,
    session_time: int | None = None,
) -> dict[str, Any]:
    stage_config: LevelConfig | None = (
        get_level(level_id) if mode == "campaign" else None
    )

    turn_time_val = stage_config.turn_time if stage_config else 15
    hints_val = stage_config.hints_allowed if stage_config else 3
    if session_time is not None:
        sess_time_val = session_time
    elif stage_config is not None:
        sess_time_val = stage_config.session_time
    else:
        sess_time_val = 300

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
        "level_id": level_id,
        "stage_config": stage_config,
        "session_time": sess_time_val,
        "initial_session_time": sess_time_val,
        "turn_time": turn_time_val,
        "initial_turn_time": turn_time_val,
        "consecutive_turns": 1,
        "hint_active": False,
        "hint_col": -1,
        "hints_remaining": hints_val,
        "initial_hints_allowed": hints_val,
        "moves_p1": 0,
        "moves_p2": 0,
        "earned_stars": 0,
        "new_unlock": False,
        "result_recorded": False,
    }


def switch_turns(state: dict[str, Any]) -> dict[str, Any]:
    state["turn_time"] = state.get("initial_turn_time", 15)
    state["hint_active"] = False
    state["hint_col"] = -1
    state["consecutive_turns"] = 1
    state["current_player"] = 2 if state["current_player"] == 1 else 1
    return state


def execute_move(
    state: dict[str, Any],
    col: int,
    profile_manager: ProfileManager | None = None,
) -> dict[str, Any]:
    if state["game_over"] or col == -1:
        return state

    board = state["board"]
    player = state["current_player"]

    if game_logic.is_valid_location(board, col):
        row = game_logic.get_next_open_row(board, col)
        game_logic.drop_piece(board, row, col, player)

        if player == 1:
            state["moves_p1"] += 1
        else:
            state["moves_p2"] += 1

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
            _finalize_match(state, profile_manager)
        elif game_logic.is_board_full(board):
            state["game_over"] = True
            state["winner"] = -1
            _finalize_match(state, profile_manager)
        else:
            state = switch_turns(state)

    return state


def _finalize_match(
    state: dict[str, Any], profile_manager: ProfileManager | None = None
) -> None:
    if state.get("result_recorded") or profile_manager is None:
        return

    state["result_recorded"] = True
    if state["mode"] == "campaign":
        lvl_id = state["level_id"]
        won = state["winner"] == 1
        elapsed = state["initial_session_time"] - max(0, state["session_time"])
        moves = state["moves_p1"]
        res = profile_manager.record_match_result(
            level_id=lvl_id,
            won=won,
            moves_count=moves,
            elapsed_time=elapsed,
            session_time=state["initial_session_time"],
        )
        state["earned_stars"] = res.get("stars_earned", 0)
        state["new_unlock"] = res.get("new_unlock", False)


def apply_hint(state: dict[str, Any]) -> dict[str, Any]:
    if state.get("hints_remaining", 0) <= 0 or state.get("game_over", False):
        return state

    state["hints_remaining"] -= 1
    col, _ = minimax.get_best_move(state["board"], depth=5)
    state["hint_col"] = col
    state["hint_active"] = True
    return state


def tick_timers(
    state: dict[str, Any], profile_manager: ProfileManager | None = None
) -> dict[str, Any]:
    if state["game_over"]:
        return state

    state["session_time"] -= 1
    if state["session_time"] <= 0:
        state["game_over"] = True
        state["winner"] = -1
        _finalize_match(state, profile_manager)
        return state

    is_human_turn = not (
        state["mode"] in ("campaign", "pva") and state["current_player"] == 2
    )

    if is_human_turn and not state["ai_thinking"]:
        state["turn_time"] -= 1
        if state["turn_time"] <= 0:
            state = switch_turns(state)

    return state


def process_ai_turn(
    state: dict[str, Any], profile_manager: ProfileManager | None = None
) -> dict[str, Any]:
    stage: LevelConfig | None = state.get("stage_config")
    depth = stage.depth if stage else 5
    blunder_rate = stage.blunder_rate if stage else 0.0

    start_time = time.perf_counter()
    best_col, ai_nodes_explored = minimax.get_best_move(
        state["board"], depth=depth, blunder_rate=blunder_rate
    )
    end_time = time.perf_counter()

    state["ai_nodes"] = ai_nodes_explored
    state["ai_time"] = (end_time - start_time) * 1000
    state["ai_thinking"] = False

    state = execute_move(state, best_col, profile_manager)

    return state
