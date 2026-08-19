from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QPushButton, QWidget

from src.core import game_logic
from src.state import game_state
from src.ui import board_renderer


class GameWindow(QWidget):
    def __init__(self, go_home_callback):
        super().__init__()
        self.go_home_callback = go_home_callback
        self.state = game_state.create_initial_state()
        self.setMouseTracking(True)

        # Menu Button
        btn = QPushButton("QUIT TO MENU", self)
        btn.move(board_renderer.BOARD_WIDTH + board_renderer.MARGIN_LEFT + 30, 35)
        btn.setFixedHeight(36)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
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
        btn.clicked.connect(self.go_home_callback)

        # AI Hint Button
        self.hint_btn = QPushButton("USE AI HINT", self)
        self.hint_btn.move(
            board_renderer.BOARD_WIDTH + board_renderer.MARGIN_LEFT + 30,
            board_renderer.MARGIN_TOP + 360,
        )
        self.hint_btn.setFixedSize(board_renderer.PANEL_WIDTH - 30, 44)
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

        # Restart Button
        self.restart_btn = QPushButton("RESTART GAME", self)
        self.restart_btn.move(
            board_renderer.BOARD_WIDTH + board_renderer.MARGIN_LEFT + 30,
            board_renderer.MARGIN_TOP + 412,
        )
        self.restart_btn.setFixedSize(board_renderer.PANEL_WIDTH - 30, 44)
        self.restart_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.restart_btn.clicked.connect(self.restart_game)

        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.on_second_tick)

    def start_new_game(self, mode, session_time):
        self.initial_mode = mode
        self.initial_session_time = session_time
        self.state = game_state.create_initial_state(mode, session_time)
        self.clock_timer.start(1000)
        self.update_ui_state()

    def restart_game(self):
        mode = getattr(self, "initial_mode", self.state.get("mode", "pva"))
        session_time = getattr(self, "initial_session_time", 300)
        self.start_new_game(mode, session_time)

    def request_hint(self):
        self.state = game_state.apply_hint(self.state)
        self.update_ui_state()

    def on_second_tick(self):
        old_player = self.state["current_player"]
        self.state = game_state.tick_timers(self.state)

        if (
            old_player == 1
            and self.state["current_player"] == 2
            and self.state["mode"] == "pva"
            and not self.state["game_over"]
        ):
            QTimer.singleShot(800, self.run_ai)

        self.update_ui_state()

    def update_ui_state(self):
        if (
            self.state["mode"] == "pva"
            or self.state["consecutive_turns"] > 1
            or self.state["ai_thinking"]
            or self.state["game_over"]
        ):
            self.hint_btn.hide()
        else:
            self.hint_btn.show()

        if self.state["game_over"]:
            self.restart_btn.setText("PLAY AGAIN")
            self.restart_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00E5FF, stop:1 #00E676);
                    color: #0B111E;
                    font-size: 14px;
                    font-weight: 900;
                    letter-spacing: 1.5px;
                    border: none;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #33ECFF, stop:1 #33E991);
                }
                QPushButton:pressed {
                    background: #00B0FF;
                }
            """)
            self.restart_btn.show()
        else:
            self.restart_btn.hide()
        self.update()

    def run_ai(self):
        self.state = game_state.process_ai_turn(self.state)
        self.update_ui_state()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        board_renderer.draw_game(painter, self.state)

    def mouseMoveEvent(self, event):
        if (
            (self.state["mode"] == "pvp" or self.state["current_player"] == 1)
            and not self.state["game_over"]
            and not self.state["ai_thinking"]
        ):
            col = board_renderer.get_column_from_x(event.pos().x())
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
                self.state = game_state.execute_move(self.state, col)
                self.setCursor(Qt.CursorShape.ArrowCursor)
                self.update_ui_state()

                if (
                    self.state["mode"] == "pva"
                    and self.state["current_player"] == 2
                    and not self.state["game_over"]
                ):
                    self.state["ai_thinking"] = True
                    QTimer.singleShot(800, self.run_ai)
