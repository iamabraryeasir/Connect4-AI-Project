from collections.abc import Callable

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QPushButton, QWidget

from src.core import game_logic
from src.profile.profile_manager import ProfileManager
from src.state import game_state
from src.ui import board_renderer


class GameWindow(QWidget):
    def __init__(
        self,
        profile_manager: ProfileManager,
        go_home_callback: Callable[[], None],
        on_next_level: Callable[[int], None] | None = None,
    ):
        super().__init__()
        self.profile_manager = profile_manager
        self.go_home_callback = go_home_callback
        self.on_next_level = on_next_level
        self.state = game_state.create_initial_state()
        self.setMouseTracking(True)

        # Back to Menu / Level Select Button
        self.back_btn = QPushButton("LEVEL SELECT", self)
        self.back_btn.setFixedHeight(36)
        self.back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #1E293B;
                color: #F8FAFC;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 6px 16px;
                font-weight: 700;
                font-size: 12px;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                border: 1px solid #00E5FF;
                color: #00E5FF;
                background-color: #243347;
            }
            QPushButton:pressed {
                background-color: #162030;
            }
        """)
        self.back_btn.clicked.connect(self.go_home_callback)

        # AI Hint Button
        self.hint_btn = QPushButton("USE AI HINT", self)
        self.hint_btn.setFixedHeight(42)
        self.hint_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.hint_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FFD54F, stop:1 #FFB70D);
                color: #0B111E;
                font-size: 13px;
                font-weight: 800;
                letter-spacing: 1px;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FFE082, stop:1 #FFC107);
            }
            QPushButton:pressed {
                background: #E5A800;
            }
        """)
        self.hint_btn.clicked.connect(self.request_hint)

        # Next Level Button (Visible on Campaign Win)
        self.next_level_btn = QPushButton("NEXT LEVEL  ▶", self)
        self.next_level_btn.setFixedHeight(42)
        self.next_level_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_level_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00E5FF, stop:1 #00E676);
                color: #0B111E;
                font-size: 13px;
                font-weight: 900;
                letter-spacing: 1px;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #33ECFF, stop:1 #33E991);
            }
        """)
        self.next_level_btn.clicked.connect(self._handle_next_level)
        self.next_level_btn.hide()

        # Restart Button
        self.restart_btn = QPushButton("RETRY LEVEL", self)
        self.restart_btn.setFixedHeight(42)
        self.restart_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.restart_btn.clicked.connect(self.restart_game)

        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.on_second_tick)

        self._reposition_elements()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._reposition_elements()

    def _reposition_elements(self):
        w = max(self.width(), 900)
        h = max(self.height(), 650)
        layout = board_renderer.calculate_layout(w, h)
        panel_x = layout["panel_x"]
        panel_w = layout["panel_w"]
        margin_top = layout["margin_top"]

        header_y = max(20, margin_top - 50)
        self.back_btn.move(panel_x, header_y)
        self.back_btn.setFixedWidth(panel_w)

        btn_y1 = margin_top + 320
        btn_y2 = margin_top + 372

        self.hint_btn.move(panel_x, btn_y1)
        self.hint_btn.setFixedWidth(panel_w)

        self.next_level_btn.move(panel_x, btn_y1)
        self.next_level_btn.setFixedWidth(panel_w)

        self.restart_btn.move(panel_x, btn_y2)
        self.restart_btn.setFixedWidth(panel_w)

    def start_new_game(
        self,
        mode: str = "campaign",
        level_id: int = 1,
        session_time: int | None = None,
    ):
        self.initial_mode = mode
        self.initial_level_id = level_id
        self.initial_session_time = session_time
        self.state = game_state.create_initial_state(
            mode=mode, level_id=level_id, session_time=session_time
        )
        self.back_btn.setText("LEVEL SELECT" if mode == "campaign" else "QUIT TO MENU")
        self._reposition_elements()
        self.clock_timer.start(1000)
        self.update_ui_state()

    def restart_game(self):
        mode = getattr(self, "initial_mode", "campaign")
        lvl = getattr(self, "initial_level_id", 1)
        sess = getattr(self, "initial_session_time", None)
        self.start_new_game(mode, lvl, sess)

    def _handle_next_level(self):
        current_lvl = self.state.get("level_id", 1)
        if current_lvl < 5 and self.on_next_level:
            self.on_next_level(current_lvl + 1)

    def request_hint(self):
        self.state = game_state.apply_hint(self.state)
        self.update_ui_state()

    def on_second_tick(self):
        old_player = self.state["current_player"]
        self.state = game_state.tick_timers(self.state, self.profile_manager)

        if (
            old_player == 1
            and self.state["current_player"] == 2
            and self.state["mode"] in ("campaign", "pva")
            and not self.state["game_over"]
        ):
            QTimer.singleShot(600, self.run_ai)

        self.update_ui_state()

    def update_ui_state(self):
        is_campaign = self.state.get("mode") == "campaign"
        is_game_over = self.state["game_over"]

        # Hint Button Visibility & Quota
        hints_rem = self.state.get("hints_remaining", 0)
        hints_initial = self.state.get("initial_hints_allowed", 0)

        if is_game_over or self.state["ai_thinking"] or hints_initial == 0:
            self.hint_btn.hide()
        elif not is_game_over and (
            self.state["mode"] == "pvp" or self.state["current_player"] == 1
        ):
            if hints_rem > 0:
                self.hint_btn.setText(f"USE AI HINT  ({hints_rem} LEFT)")
                self.hint_btn.setEnabled(True)
                self.hint_btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FFD54F, stop:1 #FFB70D);
                        color: #0B111E;
                        font-size: 12px;
                        font-weight: 800;
                        letter-spacing: 1px;
                        border: none;
                        border-radius: 10px;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FFE082, stop:1 #FFC107);
                    }
                    QPushButton:pressed {
                        background: #E5A800;
                    }
                """)
                self.hint_btn.show()
            else:
                self.hint_btn.setText("NO HINTS LEFT")
                self.hint_btn.setEnabled(False)
                self.hint_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #1E293B;
                        color: #64748B;
                        font-size: 11px;
                        font-weight: 700;
                        letter-spacing: 1px;
                        border: 1px solid #334155;
                        border-radius: 10px;
                    }
                """)
                self.hint_btn.show()
        else:
            self.hint_btn.hide()

        # Game Over Controls
        if is_game_over:
            won = self.state["winner"] == 1
            lvl_id = self.state.get("level_id", 1)

            if is_campaign and won and lvl_id < 5:
                self.hint_btn.hide()
                self.next_level_btn.show()
                self.restart_btn.setText("RETRY LEVEL")
            else:
                self.next_level_btn.hide()
                self.restart_btn.setText("RETRY LEVEL" if is_campaign else "PLAY AGAIN")

            self.restart_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FFD54F, stop:1 #FF9100);
                    color: #0B111E;
                    font-size: 13px;
                    font-weight: 800;
                    letter-spacing: 1px;
                    border: none;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FFE082, stop:1 #FFA726);
                }
            """)
            self.restart_btn.show()
        else:
            self.next_level_btn.hide()
            self.restart_btn.hide()

        self.update()

    def run_ai(self):
        if not self.state["game_over"]:
            self.state = game_state.process_ai_turn(self.state, self.profile_manager)
            self.update_ui_state()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        board_renderer.draw_game(painter, self.state, self.width(), self.height())

    def mouseMoveEvent(self, event):
        if (
            (self.state["mode"] == "pvp" or self.state["current_player"] == 1)
            and not self.state["game_over"]
            and not self.state["ai_thinking"]
        ):
            col = board_renderer.get_column_from_x(
                event.pos().x(), self.width(), self.height()
            )
            self.state["hover_col"] = col
            self.setCursor(
                Qt.CursorShape.PointingHandCursor
                if col != -1 and game_logic.is_valid_location(self.state["board"], col)
                else Qt.CursorShape.ArrowCursor
            )
        else:
            self.state["hover_col"] = -1
            self.setCursor(Qt.CursorShape.ArrowCursor)
        self.update()

    def mousePressEvent(self, event):
        if (
            (self.state["mode"] == "pvp" or self.state["current_player"] == 1)
            and not self.state["game_over"]
            and not self.state["ai_thinking"]
        ):
            col = self.state["hover_col"]
            if col != -1 and game_logic.is_valid_location(self.state["board"], col):
                self.state = game_state.execute_move(
                    self.state, col, self.profile_manager
                )
                self.setCursor(Qt.CursorShape.ArrowCursor)
                self.update_ui_state()

                if (
                    self.state["mode"] in ("campaign", "pva")
                    and self.state["current_player"] == 2
                    and not self.state["game_over"]
                ):
                    self.state["ai_thinking"] = True
                    QTimer.singleShot(600, self.run_ai)
