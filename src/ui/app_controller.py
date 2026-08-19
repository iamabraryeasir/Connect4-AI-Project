from PyQt6.QtCore import Qt
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QLinearGradient,
    QPainter,
    QRadialGradient,
)
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.ui import board_renderer
from src.ui.game_window import GameWindow


class StartScreen(QWidget):
    def __init__(self, start_game_callback):
        super().__init__()
        self.setAutoFillBackground(True)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(16)
        layout.setContentsMargins(50, 50, 50, 50)

        # Header Badge
        badge_container = QHBoxLayout()
        badge_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge = QLabel("AI ENGINE  •  MINIMAX & DFS")
        badge.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 229, 255, 0.1);
                color: #00E5FF;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 1px;
                border-radius: 12px;
                padding: 5px 14px;
                border: 1px solid rgba(0, 229, 255, 0.2);
            }
        """)
        badge_container.addWidget(badge)

        # Title & Subtitle
        title = QLabel("CONNECT 4")
        title.setFont(QFont("Arial", 32, QFont.Weight.Black))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #FFFFFF; letter-spacing: 2px;")

        subtitle = QLabel("Select your game configuration to begin")
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #94A3B8; margin-bottom: 10px;")

        # Common QComboBox Styling
        combo_style = """
            QComboBox {
                background-color: #1E293B;
                color: #F8FAFC;
                border: 1px solid #334155;
                border-radius: 10px;
                padding: 10px 16px;
                font-size: 14px;
                font-weight: 600;
            }
            QComboBox:hover {
                border: 1px solid #00E5FF;
                background-color: #243347;
            }
            QComboBox:focus {
                border: 1px solid #00E5FF;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #94A3B8;
                margin-right: 12px;
            }
            QAbstractItemView {
                background-color: #1E293B;
                color: #F8FAFC;
                selection-background-color: #2563EB;
                selection-color: #FFFFFF;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 6px;
                outline: none;
            }
        """

        # Form Field: Game Mode
        mode_label = QLabel("GAME MODE")
        mode_label.setFixedWidth(380)
        mode_label.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 700;")
        self.mode_box = QComboBox()
        self.mode_box.addItems(["Player vs AI", "Player vs Player (PvP)"])
        self.mode_box.setFixedSize(380, 44)
        self.mode_box.setStyleSheet(combo_style)

        # Form Field: Match Duration
        time_label = QLabel("MATCH DURATION")
        time_label.setFixedWidth(380)
        time_label.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 700;")
        self.time_box = QComboBox()
        self.time_box.addItems(["3 Minutes", "5 Minutes", "10 Minutes"])
        self.time_box.setFixedSize(380, 44)
        self.time_box.setStyleSheet(combo_style)

        # Start Button CTA
        start_btn = QPushButton("START MATCH")
        start_btn.setFixedSize(380, 50)
        start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        start_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FF4B4B, stop:1 #FF7B00);
                color: #FFFFFF;
                font-size: 15px;
                font-weight: 800;
                letter-spacing: 1px;
                border: none;
                border-radius: 12px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FF5C5C, stop:1 #FF8C1A);
            }
            QPushButton:pressed {
                background: #E03E3E;
            }
        """)

        start_btn.clicked.connect(
            lambda: start_game_callback(
                "pva" if self.mode_box.currentIndex() == 0 else "pvp",
                [180, 300, 600][self.time_box.currentIndex()],
            )
        )

        layout.addLayout(badge_container)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(mode_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.mode_box, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(time_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.time_box, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(start_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Flat Ambient Gradient Background
        bg_gradient = QLinearGradient(0, 0, 0, self.height())
        bg_gradient.setColorAt(0.0, QColor("#0B111E"))
        bg_gradient.setColorAt(1.0, QColor("#111827"))
        painter.fillRect(self.rect(), bg_gradient)

        # Soft Ambient Center Glow
        glow = QRadialGradient(self.width() / 2, self.height() / 2, 400)
        glow.setColorAt(0.0, QColor(0, 229, 255, 15))
        glow.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())


class AppController(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connect 4 - AI Lab Project")
        self.setFixedSize(board_renderer.WINDOW_WIDTH, board_renderer.WINDOW_HEIGHT)

        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setFixedSize(
            board_renderer.WINDOW_WIDTH, board_renderer.WINDOW_HEIGHT
        )

        self.start_screen = StartScreen(self.launch_game)
        self.game_screen = GameWindow(self.show_menu)

        self.stacked_widget.addWidget(self.start_screen)
        self.stacked_widget.addWidget(self.game_screen)

    def launch_game(self, mode, session_time):
        self.game_screen.start_new_game(mode, session_time)
        self.stacked_widget.setCurrentIndex(1)

    def show_menu(self):
        self.game_screen.clock_timer.stop()
        self.stacked_widget.setCurrentIndex(0)
