from typing import Callable

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
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.profile.profile_manager import ProfileManager


class StartScreen(QWidget):
    def __init__(
        self,
        profile_manager: ProfileManager,
        on_start_campaign: Callable[[], None],
        on_start_pvp: Callable[[int], None],
    ):
        super().__init__()
        self.profile_manager = profile_manager
        self.on_start_campaign = on_start_campaign
        self.on_start_pvp = on_start_pvp
        self.setAutoFillBackground(True)

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(0)
        layout.setContentsMargins(40, 30, 40, 30)

        layout.addStretch(1)

        # Center Container Frame
        container = QFrame()
        container.setObjectName("center_container")
        container.setFixedWidth(440)
        container.setStyleSheet("""
            QFrame#center_container {
                background: transparent;
                border: none;
            }
            QLabel {
                border: none;
                background: transparent;
            }
        """)
        c_layout = QVBoxLayout(container)
        c_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        c_layout.setSpacing(14)
        c_layout.setContentsMargins(0, 0, 0, 0)

        # Header Badge
        badge_container = QHBoxLayout()
        badge_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge = QLabel("AI LABORATORY  •  ADVERSARIAL SEARCH BENCHMARK")
        badge.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 229, 255, 0.08);
                color: #00E5FF;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 1.5px;
                border-radius: 12px;
                padding: 6px 16px;
                border: 1px solid rgba(0, 229, 255, 0.3);
            }
        """)
        badge_container.addWidget(badge)
        c_layout.addLayout(badge_container)

        # Title & Subtitle
        title = QLabel("CONNECT 4")
        title.setFont(QFont("Arial", 32, QFont.Weight.Black))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #FFFFFF; letter-spacing: 4px; margin-top: 2px;")
        c_layout.addWidget(title)

        # Profile Summary Card
        self.profile_card = QFrame()
        self.profile_card.setObjectName("profile_card")
        self.profile_card.setFixedSize(440, 115)
        self.profile_card.setStyleSheet("""
            QFrame#profile_card {
                background-color: #162032;
                border: 1px solid #2A3B53;
                border-radius: 14px;
            }
            QFrame#profile_card QLabel {
                border: none;
                background: transparent;
            }
        """)
        card_layout = QVBoxLayout(self.profile_card)
        card_layout.setContentsMargins(20, 14, 20, 14)
        card_layout.setSpacing(6)

        self.name_label = QLabel()
        self.name_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.name_label.setStyleSheet("color: #00E5FF;")

        self.stats_label = QLabel()
        self.stats_label.setFont(QFont("Arial", 10))
        self.stats_label.setStyleSheet("color: #94A3B8;")

        self.stars_label = QLabel()
        self.stars_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.stars_label.setStyleSheet("color: #FFD54F;")

        card_layout.addWidget(self.name_label)
        card_layout.addWidget(self.stats_label)
        card_layout.addWidget(self.stars_label)

        c_layout.addWidget(self.profile_card)

        # Action Button 1: AI Benchmark Mode
        campaign_btn = QPushButton("▶   START AI BENCHMARK (LEVELS)")
        campaign_btn.setFixedSize(440, 50)
        campaign_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        campaign_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00E5FF, stop:1 #00E676);
                color: #0B111E;
                font-size: 13px;
                font-weight: 900;
                letter-spacing: 1.5px;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #33ECFF, stop:1 #33E991);
            }
            QPushButton:pressed {
                background: #00B0FF;
            }
        """)
        campaign_btn.clicked.connect(self.on_start_campaign)
        c_layout.addWidget(campaign_btn)

        # PvP Duration Dropdown & Label
        pvp_label = QLabel("TWO-PLAYER PASS & PLAY CONFIGURATION")
        pvp_label.setStyleSheet(
            "color: #64748B; font-size: 10px; font-weight: 700; margin-top: 4px;"
        )
        c_layout.addWidget(pvp_label)

        self.time_box = QComboBox()
        self.time_box.addItems(
            ["3 Minutes Match", "5 Minutes Match", "10 Minutes Match"]
        )
        self.time_box.setFixedSize(440, 42)
        self.time_box.setStyleSheet("""
            QComboBox {
                background-color: #1E293B;
                color: #F8FAFC;
                border: 1px solid #334155;
                border-radius: 10px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 600;
            }
            QComboBox:hover {
                border: 1px solid #FF4B4B;
                background-color: #243347;
            }
            QComboBox:focus {
                border: 1px solid #FF4B4B;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 36px;
                border: none;
                background: transparent;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #94A3B8;
                width: 0;
                height: 0;
                margin-right: 12px;
            }
            QComboBox::down-arrow:hover {
                border-top: 6px solid #FF4B4B;
            }
            QAbstractItemView {
                background-color: #1E293B;
                color: #F8FAFC;
                selection-background-color: #FF4B4B;
                selection-color: #FFFFFF;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 6px;
                outline: none;
            }
        """)
        c_layout.addWidget(self.time_box)

        # Action Button 2: PvP Mode
        pvp_btn = QPushButton("👥   TWO-PLAYER PASS & PLAY")
        pvp_btn.setFixedSize(440, 46)
        pvp_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        pvp_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FF4B4B, stop:1 #FF7B00);
                color: #FFFFFF;
                font-size: 13px;
                font-weight: 800;
                letter-spacing: 1px;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FF5C5C, stop:1 #FF8C1A);
            }
            QPushButton:pressed {
                background: #E03E3E;
            }
        """)
        pvp_btn.clicked.connect(self._handle_pvp_click)
        c_layout.addWidget(pvp_btn)

        layout.addWidget(container, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(1)

        self.refresh_profile()

    def _handle_pvp_click(self):
        durations = [180, 300, 600]
        chosen = durations[self.time_box.currentIndex()]
        self.on_start_pvp(chosen)

    def refresh_profile(self):
        prof = self.profile_manager.get_profile()
        pname = prof.get("player_name", "Player 1")
        unlocked = prof.get("highest_unlocked_level", 1)
        career = prof.get("career_stats", {})
        wins = career.get("total_wins", 0)
        losses = career.get("total_losses", 0)
        streak = career.get("win_streak", 0)
        total_stars = career.get("total_stars", 0)

        self.name_label.setText(
            f"👤  {pname.upper()}   •   LEVEL {unlocked}/5 UNLOCKED"
        )
        self.stats_label.setText(
            f"🏆 {wins} Wins   |   💀 {losses} Losses   |   🔥 Streak: {streak}"
        )
        self.stars_label.setText(f"⭐ {total_stars} / 15 Stars Earned")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Ambient Background Gradient
        bg_gradient = QLinearGradient(0, 0, 0, self.height())
        bg_gradient.setColorAt(0.0, QColor("#0B111E"))
        bg_gradient.setColorAt(1.0, QColor("#111827"))
        painter.fillRect(self.rect(), bg_gradient)

        # Soft Cyan Center Glow
        glow = QRadialGradient(
            self.width() / 2,
            self.height() / 2,
            max(self.width(), self.height()) * 0.5,
        )
        glow.setColorAt(0.0, QColor(0, 229, 255, 16))
        glow.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())
