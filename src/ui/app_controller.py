from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import QStackedWidget, QVBoxLayout, QWidget

from src.profile.profile_manager import ProfileManager
from src.ui.game_window import GameWindow
from src.ui.level_select_window import LevelSelectScreen
from src.ui.start_screen import StartScreen


class AppController(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(
            "Connect 4 — Adversarial AI Laboratory & Evaluation Benchmark"
        )
        self.setMinimumSize(980, 680)
        self.resize(1080, 740)

        self.profile_manager = ProfileManager()

        # Root layout for full responsiveness
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.stacked_widget = QStackedWidget(self)
        root_layout.addWidget(self.stacked_widget)

        # Screens
        self.start_screen = StartScreen(
            profile_manager=self.profile_manager,
            on_start_campaign=self.show_level_select,
            on_start_pvp=self.launch_pvp,
        )
        self.level_select_screen = LevelSelectScreen(
            profile_manager=self.profile_manager,
            on_select_level=self.launch_campaign_level,
            on_back=self.show_main_menu,
        )
        self.game_screen = GameWindow(
            profile_manager=self.profile_manager,
            go_home_callback=self.on_game_back,
            on_next_level=self.launch_campaign_level,
        )

        self.stacked_widget.addWidget(self.start_screen)  # Index 0
        self.stacked_widget.addWidget(self.level_select_screen)  # Index 1
        self.stacked_widget.addWidget(self.game_screen)  # Index 2

        # Secret Reset Progress Keystroke (Ctrl + Shift + R)
        self.reset_shortcut = QShortcut(QKeySequence("Ctrl+Shift+R"), self)
        self.reset_shortcut.activated.connect(self.secret_reset_progress)

    def secret_reset_progress(self):
        """Hidden developer/player shortcut to completely reset game progress."""
        self.profile_manager.reset_profile()
        self.start_screen.refresh_profile()
        self.level_select_screen.refresh_levels()

        current_idx = self.stacked_widget.currentIndex()
        if current_idx == 2:
            self.game_screen.clock_timer.stop()
            self.show_main_menu()

    def show_main_menu(self):
        self.game_screen.clock_timer.stop()
        self.start_screen.refresh_profile()
        self.stacked_widget.setCurrentIndex(0)

    def show_level_select(self):
        self.game_screen.clock_timer.stop()
        self.level_select_screen.refresh_levels()
        self.stacked_widget.setCurrentIndex(1)

    def launch_campaign_level(self, level_id: int):
        self.game_screen.start_new_game(mode="campaign", level_id=level_id)
        self.stacked_widget.setCurrentIndex(2)

    def launch_pvp(self, session_time: int):
        self.game_screen.start_new_game(
            mode="pvp", level_id=1, session_time=session_time
        )
        self.stacked_widget.setCurrentIndex(2)

    def on_game_back(self):
        self.game_screen.clock_timer.stop()
        if getattr(self.game_screen, "initial_mode", "campaign") == "campaign":
            self.show_level_select()
        else:
            self.show_main_menu()
