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
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.levels.level_config import LEVELS, LevelConfig
from src.profile.profile_manager import ProfileManager


class StageCard(QFrame):
    def __init__(
        self,
        config: LevelConfig,
        is_unlocked: bool,
        stars: int,
        on_select: Callable[[int], None],
    ):
        super().__init__()
        self.config = config
        self.is_unlocked = is_unlocked
        self.stars = stars
        self.on_select = on_select

        self.setObjectName(f"stage_card_{config.id}")
        self.setFixedSize(175, 320)
        self.setCursor(
            Qt.CursorShape.PointingHandCursor
            if is_unlocked
            else Qt.CursorShape.ForbiddenCursor
        )
        self._setup_card()

    def _setup_card(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 18, 14, 18)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Stage Number Pill
        stage_pill = QLabel(f"STAGE 0{self.config.id}")
        stage_pill.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        stage_pill.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stage_pill.setStyleSheet(f"""
            QLabel {{
                color: {self.config.accent_color if self.is_unlocked else "#64748B"};
                letter-spacing: 1.5px;
                border: none;
                background: transparent;
            }}
        """)
        layout.addWidget(stage_pill)

        # Boss Name
        boss_lbl = QLabel(self.config.boss_name)
        boss_lbl.setFont(QFont("Arial", 18, QFont.Weight.Black))
        boss_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        boss_lbl.setStyleSheet(f"""
            QLabel {{
                color: {"#FFFFFF" if self.is_unlocked else "#64748B"};
                letter-spacing: 1px;
                border: none;
                background: transparent;
            }}
        """)
        layout.addWidget(boss_lbl)

        # Title / Role
        title_lbl = QLabel(self.config.title)
        title_lbl.setFont(QFont("Arial", 10))
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_lbl.setStyleSheet(
            "QLabel { color: #94A3B8; border: none; background: transparent; }"
        )
        layout.addWidget(title_lbl)

        # Subtle Separator
        sep = QFrame()
        sep.setObjectName("sep")
        sep.setFixedHeight(1)
        sep.setStyleSheet("QFrame#sep { background-color: #2A3B53; border: none; }")
        layout.addWidget(sep)

        # Depth, Clock & Hint Badge
        hint_str = (
            f"{self.config.hints_allowed} Hints"
            if self.config.hints_allowed > 0
            else "No Hints"
        )
        info_lbl = QLabel(
            f"Depth {self.config.depth}  •  {self.config.turn_time}s  •  {hint_str}"
        )
        info_lbl.setFont(QFont("Arial", 8, QFont.Weight.Bold))
        info_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_lbl.setStyleSheet(
            "QLabel { color: #CBD5E1; border: none; background: transparent; }"
        )
        layout.addWidget(info_lbl)

        # Star Rating or Lock Status
        if self.is_unlocked:
            star_str = "★" * self.stars + "☆" * (3 - self.stars)
            status_lbl = QLabel(star_str)
            status_lbl.setFont(QFont("Arial", 16, QFont.Weight.Bold))
            status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            status_lbl.setStyleSheet(
                "QLabel { color: #FFD54F; letter-spacing: 2px; border: none; background: transparent; }"
            )
        else:
            status_lbl = QLabel("🔒 LOCKED")
            status_lbl.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            status_lbl.setStyleSheet(
                "QLabel { color: #64748B; letter-spacing: 1px; border: none; background: transparent; }"
            )
        layout.addWidget(status_lbl)

        # Battle Action Button
        btn = QPushButton("BATTLE" if self.is_unlocked else "LOCKED")
        btn.setFixedHeight(38)
        btn.setEnabled(self.is_unlocked)
        btn.setCursor(
            Qt.CursorShape.PointingHandCursor
            if self.is_unlocked
            else Qt.CursorShape.ForbiddenCursor
        )

        if self.is_unlocked:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {self.config.accent_color}, stop:1 #FFFFFF);
                    color: #0B111E;
                    font-size: 12px;
                    font-weight: 900;
                    letter-spacing: 1.5px;
                    border: none;
                    border-radius: 9px;
                }}
                QPushButton:hover {{
                    background: #FFFFFF;
                }}
            """)
            btn.clicked.connect(lambda: self.on_select(self.config.id))
        else:
            btn.setStyleSheet("""
                QPushButton {{
                    background-color: #1E293B;
                    color: #475569;
                    font-size: 11px;
                    font-weight: 800;
                    letter-spacing: 1px;
                    border: 1px solid #2A3B53;
                    border-radius: 9px;
                }}
            """)
        layout.addWidget(btn)

        # Scoped Card Border styling (Never cascades borders to labels)
        card_id = f"stage_card_{self.config.id}"
        border_color = self.config.accent_color if self.is_unlocked else "#2A3B53"
        bg_color = "#162032" if self.is_unlocked else "#0F172A"

        self.setStyleSheet(f"""
            QFrame#{card_id} {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 16px;
            }}
            QFrame#{card_id} QLabel {{
                border: none;
                background: transparent;
            }}
        """)

    def mousePressEvent(self, event):
        if self.is_unlocked:
            self.on_select(self.config.id)


class LevelSelectScreen(QWidget):
    def __init__(
        self,
        profile_manager: ProfileManager,
        on_select_level: Callable[[int], None],
        on_back: Callable[[], None],
    ):
        super().__init__()
        self.profile_manager = profile_manager
        self.on_select_level = on_select_level
        self.on_back = on_back
        self.setAutoFillBackground(True)

        self._build_ui()

    def _build_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(30, 20, 30, 20)

        self.main_layout.addStretch(1)

        # Header Title Box
        title_box = QVBoxLayout()
        title_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_box.setSpacing(6)

        header = QLabel("AI CAMPAIGN ROADMAP")
        header.setFont(QFont("Arial", 26, QFont.Weight.Black))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet(
            "color: #FFFFFF; letter-spacing: 3px; border: none; background: transparent;"
        )

        self.subtitle = QLabel("Select an unlocked AI entity to challenge")
        self.subtitle.setFont(QFont("Arial", 12))
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setStyleSheet(
            "color: #94A3B8; border: none; background: transparent;"
        )

        title_box.addWidget(header)
        title_box.addWidget(self.subtitle)
        self.main_layout.addLayout(title_box)

        self.main_layout.addSpacing(22)

        # Cards Container Layout (Centered horizontally)
        self.cards_layout = QHBoxLayout()
        self.cards_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cards_layout.setSpacing(16)
        self.main_layout.addLayout(self.cards_layout)

        self.main_layout.addSpacing(26)

        # Back Button
        back_btn = QPushButton("←   BACK TO MAIN MENU")
        back_btn.setFixedSize(260, 44)
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #1E293B;
                color: #CBD5E1;
                font-size: 12px;
                font-weight: 800;
                letter-spacing: 1.5px;
                border: 1px solid #334155;
                border-radius: 10px;
            }
            QPushButton:hover {
                border: 1px solid #00E5FF;
                color: #00E5FF;
                background-color: #243347;
            }
        """)
        back_btn.clicked.connect(self.on_back)
        self.main_layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addStretch(1)

        self.refresh_levels()

    def refresh_levels(self):
        while self.cards_layout.count():
            child = self.cards_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        prof = self.profile_manager.get_profile()
        highest_unlocked = prof.get("highest_unlocked_level", 1)
        progress = prof.get("level_progress", {})

        total_stars = prof.get("career_stats", {}).get("total_stars", 0)
        self.subtitle.setText(
            f"Stage Progress: {highest_unlocked}/5 Unlocked   •   ⭐ {total_stars} / 15 Stars Earned"
        )

        for lvl_id in range(1, 6):
            cfg = LEVELS[lvl_id]
            is_unlocked = lvl_id <= highest_unlocked
            stars = progress.get(str(lvl_id), {}).get("stars", 0)
            card = StageCard(
                config=cfg,
                is_unlocked=is_unlocked,
                stars=stars,
                on_select=self.on_select_level,
            )
            self.cards_layout.addWidget(card)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        bg_gradient = QLinearGradient(0, 0, 0, self.height())
        bg_gradient.setColorAt(0.0, QColor("#0B111E"))
        bg_gradient.setColorAt(1.0, QColor("#111827"))
        painter.fillRect(self.rect(), bg_gradient)

        glow = QRadialGradient(
            self.width() / 2, self.height() / 2, max(self.width(), self.height()) * 0.55
        )
        glow.setColorAt(0.0, QColor(0, 229, 255, 14))
        glow.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())
