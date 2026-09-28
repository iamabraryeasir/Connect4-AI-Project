import json
from pathlib import Path
from typing import Any


def get_default_profile() -> dict[str, Any]:
    return {
        "player_name": "Player 1",
        "highest_unlocked_level": 1,
        "level_progress": {
            str(lvl): {
                "completed": False,
                "stars": 0,
                "best_time_sec": None,
                "wins": 0,
                "losses": 0,
            }
            for lvl in range(1, 6)
        },
        "career_stats": {
            "total_matches": 0,
            "total_wins": 0,
            "total_losses": 0,
            "win_streak": 0,
            "best_win_streak": 0,
            "total_stars": 0,
        },
    }


class ProfileManager:
    def __init__(self, file_path: str | Path | None = None):
        if file_path is None:
            self.file_path = (
                Path(__file__).resolve().parent.parent.parent / "data" / "profile.json"
            )
        else:
            self.file_path = Path(file_path)

        self.data_dir = self.file_path.parent
        self._profile: dict[str, Any] = self.load_profile()

    def load_profile(self) -> dict[str, Any]:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            default_data = get_default_profile()
            self.save_profile(default_data)
            return default_data

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except (json.JSONDecodeError, OSError, KeyError, TypeError):
            default_data = get_default_profile()
            self.save_profile(default_data)
            return default_data

    def save_profile(self, profile_data: dict[str, Any] | None = None) -> None:
        if profile_data is not None:
            self._profile = profile_data

        self.data_dir.mkdir(parents=True, exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self._profile, f, indent=2)

    def get_profile(self) -> dict[str, Any]:
        return self._profile

    def is_level_unlocked(self, level_id: int) -> bool:
        return level_id <= self._profile.get("highest_unlocked_level", 1)

    def get_level_stars(self, level_id: int) -> int:
        lvl_key = str(level_id)
        return self._profile.get("level_progress", {}).get(lvl_key, {}).get("stars", 0)

    @staticmethod
    def calculate_stars(moves_count: int, elapsed_time: int, session_time: int) -> int:
        if moves_count <= 14 or (
            session_time > 0 and elapsed_time <= 0.40 * session_time
        ):
            return 3
        elif moves_count <= 22:
            return 2
        return 1

    def record_match_result(
        self,
        level_id: int,
        won: bool,
        moves_count: int = 0,
        elapsed_time: int = 0,
        session_time: int = 300,
    ) -> dict[str, Any]:
        lvl_key = str(level_id)
        progress = self._profile.setdefault("level_progress", {})
        lvl_stat = progress.setdefault(
            lvl_key,
            {
                "completed": False,
                "stars": 0,
                "best_time_sec": None,
                "wins": 0,
                "losses": 0,
            },
        )
        career = self._profile.setdefault("career_stats", {})

        career["total_matches"] = career.get("total_matches", 0) + 1
        stars_earned = 0
        new_unlock = False

        if won:
            career["total_wins"] = career.get("total_wins", 0) + 1
            streak = career.get("win_streak", 0) + 1
            career["win_streak"] = streak
            if streak > career.get("best_win_streak", 0):
                career["best_win_streak"] = streak

            lvl_stat["wins"] = lvl_stat.get("wins", 0) + 1
            lvl_stat["completed"] = True

            stars_earned = self.calculate_stars(moves_count, elapsed_time, session_time)
            if stars_earned > lvl_stat.get("stars", 0):
                lvl_stat["stars"] = stars_earned

            # Update best time
            old_best = lvl_stat.get("best_time_sec")
            if old_best is None or (elapsed_time > 0 and elapsed_time < old_best):
                lvl_stat["best_time_sec"] = elapsed_time

            # Unlock next level
            current_unlocked = self._profile.get("highest_unlocked_level", 1)
            if level_id == current_unlocked and level_id < 5:
                self._profile["highest_unlocked_level"] = level_id + 1
                new_unlock = True
        else:
            career["total_losses"] = career.get("total_losses", 0) + 1
            career["win_streak"] = 0
            lvl_stat["losses"] = lvl_stat.get("losses", 0) + 1

        # Recalculate total stars across all levels
        total_stars = sum(lvl.get("stars", 0) for lvl in progress.values())
        career["total_stars"] = total_stars

        self.save_profile()

        return {
            "won": won,
            "stars_earned": stars_earned,
            "new_unlock": new_unlock,
            "highest_unlocked_level": self._profile.get("highest_unlocked_level", 1),
        }

    def reset_profile(self) -> dict[str, Any]:
        self._profile = get_default_profile()
        self.save_profile()
        return self._profile
