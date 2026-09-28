from dataclasses import dataclass


@dataclass(frozen=True)
class LevelConfig:
    id: int
    name: str
    boss_name: str
    title: str
    depth: int
    blunder_rate: float
    turn_time: int
    session_time: int
    hints_allowed: int
    accent_color: str
    description: str


LEVELS: dict[int, LevelConfig] = {
    1: LevelConfig(
        id=1,
        name="Level 1",
        boss_name="Novice Agent",
        title="1-Ply Evaluation",
        depth=1,
        blunder_rate=0.35,
        turn_time=20,
        session_time=300,
        hints_allowed=5,
        accent_color="#00E676",  # Emerald Green
        description="Baseline heuristic evaluator assessing immediate 1-ply board transitions with intentional stochastic variance.",
    ),
    2: LevelConfig(
        id=2,
        name="Level 2",
        boss_name="Apprentice Agent",
        title="2-Ply Minimax",
        depth=2,
        blunder_rate=0.15,
        turn_time=15,
        session_time=300,
        hints_allowed=3,
        accent_color="#00E5FF",  # Cyan
        description="2-ply search evaluating immediate opponent replies and preventing direct 3-in-a-row formations.",
    ),
    3: LevelConfig(
        id=3,
        name="Level 3",
        boss_name="Tactical Agent",
        title="3-Ply Alpha-Beta",
        depth=3,
        blunder_rate=0.0,
        turn_time=15,
        session_time=300,
        hints_allowed=2,
        accent_color="#FFD54F",  # Amber
        description="3-ply deterministic search incorporating center column dominance and directional window scoring.",
    ),
    4: LevelConfig(
        id=4,
        name="Level 4",
        boss_name="Advanced Agent",
        title="4-Ply Alpha-Beta",
        depth=4,
        blunder_rate=0.0,
        turn_time=12,
        session_time=300,
        hints_allowed=1,
        accent_color="#FF7043",  # Coral / Orange
        description="Deep 4-ply minimax with aggressive alpha-beta pruning and multi-step tactical positioning.",
    ),
    5: LevelConfig(
        id=5,
        name="Level 5",
        boss_name="Expert Agent",
        title="5-Ply Optimal Engine",
        depth=5,
        blunder_rate=0.0,
        turn_time=10,
        session_time=180,
        hints_allowed=0,  # Hints disabled on Expert Level
        accent_color="#BA68C8",  # Purple
        description="Optimal 5-ply search evaluating tens of thousands of board states under strict blitz clock constraints.",
    ),
}


def get_level(level_id: int) -> LevelConfig | None:
    return LEVELS.get(level_id)


def get_all_levels() -> dict[int, LevelConfig]:
    return LEVELS


def get_total_levels() -> int:
    return len(LEVELS)
