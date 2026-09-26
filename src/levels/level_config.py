from dataclasses import dataclass
from typing import Dict, Optional


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


LEVELS: Dict[int, LevelConfig] = {
    1: LevelConfig(
        id=1,
        name="Stage 1",
        boss_name="Spark",
        title="Novice Bot",
        depth=1,
        blunder_rate=0.35,
        turn_time=20,
        session_time=300,
        hints_allowed=5,
        accent_color="#00E676",  # Neon Green
        description="Shallow 1-ply horizon with frequent tactical oversights. An easy entry point.",
    ),
    2: LevelConfig(
        id=2,
        name="Stage 2",
        boss_name="Circuit",
        title="Apprentice",
        depth=2,
        blunder_rate=0.15,
        turn_time=15,
        session_time=300,
        hints_allowed=3,
        accent_color="#00E5FF",  # Neon Cyan
        description="2-ply search with basic positional awareness. Blocks direct 3-in-a-row threats.",
    ),
    3: LevelConfig(
        id=3,
        name="Stage 3",
        boss_name="Vector",
        title="Tactician",
        depth=3,
        blunder_rate=0.0,
        turn_time=15,
        session_time=300,
        hints_allowed=2,
        accent_color="#FFD54F",  # Gold / Amber
        description="Consistent 3-ply heuristic search with aggressive center column dominance.",
    ),
    4: LevelConfig(
        id=4,
        name="Stage 4",
        boss_name="Nexus",
        title="Grandmaster",
        depth=4,
        blunder_rate=0.0,
        turn_time=12,
        session_time=300,
        hints_allowed=1,
        accent_color="#FF4B4B",  # Neon Red
        description="Deep 4-ply Alpha-Beta pruning engine that engineers multi-pronged fork attacks.",
    ),
    5: LevelConfig(
        id=5,
        name="Stage 5",
        boss_name="Omega",
        title="God Mode Boss",
        depth=5,
        blunder_rate=0.0,
        turn_time=10,
        session_time=180,
        hints_allowed=0,  # Hints completely disabled on Boss Level!
        accent_color="#D500F9",  # Neon Purple
        description="Uncompromising 5-ply Alpha-Beta search with hints disabled under 10s blitz pressure.",
    ),
}


def get_level(level_id: int) -> Optional[LevelConfig]:
    return LEVELS.get(level_id)


def get_all_levels() -> Dict[int, LevelConfig]:
    return LEVELS


def get_total_levels() -> int:
    return len(LEVELS)
