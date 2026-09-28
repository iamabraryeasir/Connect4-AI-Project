from typing import Any

from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QBrush, QColor, QFont, QLinearGradient, QPen, QRadialGradient

from src.core import game_logic
from src.levels.level_config import LevelConfig


def calculate_layout(width: int, height: int) -> dict[str, int]:
    margin_top = max(80, min(130, int(height * 0.15)))
    avail_h = height - margin_top - 35
    avail_w = width - 60

    panel_w = max(240, min(300, int(width * 0.25)))
    gap = 24

    cell_h = int(avail_h / 6.0)
    cell_w = int((avail_w - panel_w - gap) / 7.0)

    cell_size = max(55, min(105, min(cell_h, cell_w)))

    board_w = 7 * cell_size
    board_h = 6 * cell_size

    total_w = board_w + gap + panel_w
    margin_left = max(20, (width - total_w) // 2)
    panel_x = margin_left + board_w + gap

    return {
        "cell_size": cell_size,
        "margin_top": margin_top,
        "margin_left": margin_left,
        "board_w": board_w,
        "board_h": board_h,
        "panel_w": panel_w,
        "panel_x": panel_x,
        "gap": gap,
    }


def get_column_from_x(x: int, width: int, height: int) -> int:
    layout = calculate_layout(width, height)
    ml = layout["margin_left"]
    cs = layout["cell_size"]
    bw = layout["board_w"]
    if ml <= x < ml + bw:
        return min(int((x - ml) // cs), 6)
    return -1


def draw_game(painter, state: dict[str, Any], width: int, height: int):
    layout = calculate_layout(width, height)
    cell_size = layout["cell_size"]
    margin_top = layout["margin_top"]
    margin_left = layout["margin_left"]
    board_w = layout["board_w"]
    board_h = layout["board_h"]
    panel_w = layout["panel_w"]
    panel_x = layout["panel_x"]

    stage_cfg: LevelConfig | None = state.get("stage_config")
    is_campaign = state.get("mode") == "campaign"
    boss_name = stage_cfg.boss_name.upper() if stage_cfg else "AI"
    boss_color_hex = stage_cfg.accent_color if stage_cfg else "#FFD54F"
    boss_color = QColor(boss_color_hex)

    # 1. Ambient Background Canvas
    bg_gradient = QLinearGradient(0, 0, 0, height)
    bg_gradient.setColorAt(0.0, QColor("#0B111E"))
    bg_gradient.setColorAt(1.0, QColor("#111827"))
    painter.fillRect(0, 0, width, height, bg_gradient)

    glow = QRadialGradient(width / 2, height / 2, max(width, height) * 0.55)
    glow.setColorAt(0.0, QColor(0, 229, 255, 14))
    glow.setColorAt(1.0, QColor(0, 0, 0, 0))
    painter.setBrush(QBrush(glow))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRect(0, 0, width, height)

    # 2. Top Header Status Bar
    header_y = max(35, margin_top - 45)
    if state["game_over"]:
        if state["winner"] == -1:
            text = "GAME OVER  •  DRAW / TIMEOUT"
            color = QColor("#94A3B8")
        elif state["winner"] == 1:
            if is_campaign:
                stars = state.get("earned_stars", 1)
                star_str = "★" * stars + "☆" * (3 - stars)
                lvl_id = state.get("level_id", 1)
                text = f"LEVEL {lvl_id} COMPLETED  [{star_str}]"
            else:
                text = "PLAYER 1 WINS THE MATCH!"
            color = QColor("#00E676") if is_campaign else QColor("#FF4B4B")
        else:
            opp_name = boss_name if is_campaign else "PLAYER 2"
            text = f"{opp_name} WINS THE MATCH!"
            color = boss_color
    elif state["ai_thinking"]:
        text = f"{boss_name} IS THINKING..."
        color = boss_color
    else:
        if state["current_player"] == 1:
            player_label = "PLAYER 1"
            color = QColor("#FF4B4B")
        else:
            player_label = boss_name if is_campaign else "PLAYER 2"
            color = boss_color

        text = f"CURRENT TURN: {player_label}"

    painter.setPen(QPen(color))
    painter.setFont(QFont("Arial", 16, QFont.Weight.Bold))
    painter.drawText(margin_left, header_y, text)

    # Indicator Dot
    painter.setBrush(QBrush(color))
    painter.setPen(Qt.PenStyle.NoPen)
    dot_x = margin_left + painter.fontMetrics().horizontalAdvance(text) + 16
    painter.drawEllipse(QPointF(dot_x, header_y - 7.0), 6.5, 6.5)

    # 3. Stats Panel (Right Side Cards)
    card_style_pen = QPen(QColor("#334155"), 1)
    card_bg_brush = QBrush(QColor("#1E293B"))

    # Card 1: Timers
    card1_h = 92
    painter.setPen(card_style_pen)
    painter.setBrush(card_bg_brush)
    painter.drawRoundedRect(panel_x, margin_top, panel_w, card1_h, 12.0, 12.0)

    painter.setPen(QColor("#64748B"))
    painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
    painter.drawText(panel_x + 16, margin_top + 22, "MATCH TIMERS")

    mins, secs = divmod(max(0, state["session_time"]), 60)
    time_str = f"{mins:02}:{secs:02}"

    painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))
    painter.setPen(
        QColor("#F8FAFC") if state["session_time"] > 60 else QColor("#FF4B4B")
    )
    painter.drawText(panel_x + 16, margin_top + 48, f"Session: {time_str}")

    turn_color = QColor("#FFD54F") if state["turn_time"] <= 5 else QColor("#00E5FF")
    painter.setPen(turn_color)
    painter.drawText(
        panel_x + 16, margin_top + 72, f"Turn Clock: {state['turn_time']}s"
    )

    # Card 2: DFS Win Checker Metrics
    y_card2 = margin_top + card1_h + 12
    card2_h = 92
    painter.setPen(card_style_pen)
    painter.setBrush(card_bg_brush)
    painter.drawRoundedRect(panel_x, y_card2, panel_w, card2_h, 12.0, 12.0)

    painter.setPen(QColor("#64748B"))
    painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
    painter.drawText(panel_x + 16, y_card2 + 22, "DFS (WIN CHECKER)")

    painter.setFont(QFont("Arial", 11))
    painter.setPen(QColor("#00E5FF"))
    painter.drawText(
        panel_x + 16, y_card2 + 48, f"Nodes: {state.get('dfs_nodes', 0):,}"
    )
    painter.drawText(
        panel_x + 16, y_card2 + 72, f"Time: {state.get('dfs_time', 0):.3f} ms"
    )

    # Card 3: Minimax AI Metrics
    y_card3 = y_card2 + card2_h + 12
    card3_h = 92
    painter.setPen(card_style_pen)
    painter.setBrush(card_bg_brush)
    painter.drawRoundedRect(panel_x, y_card3, panel_w, card3_h, 12.0, 12.0)

    painter.setPen(QColor("#64748B"))
    painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
    ai_header = f"AI AGENT: {boss_name}" if is_campaign else "MINIMAX AI ENGINE"
    painter.drawText(panel_x + 16, y_card3 + 22, ai_header)

    painter.setFont(QFont("Arial", 11))
    ai_metric_color = QColor("#00E5FF") if not state.get("ai_thinking") else boss_color
    painter.setPen(ai_metric_color)
    painter.drawText(panel_x + 16, y_card3 + 48, f"Nodes: {state.get('ai_nodes', 0):,}")
    painter.drawText(
        panel_x + 16, y_card3 + 72, f"Time: {state.get('ai_time', 0):.3f} ms"
    )

    # 4. Board Container
    painter.setBrush(QBrush(QColor("#172030")))
    painter.setPen(QPen(QColor("#334155"), 2))
    painter.drawRoundedRect(margin_left, margin_top, board_w, board_h, 16.0, 16.0)

    # Column Hover Highlight
    if state.get("hint_active") and state["hint_col"] != -1:
        highlight_x = margin_left + state["hint_col"] * cell_size
        painter.setBrush(QBrush(QColor(255, 213, 79, 45)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(highlight_x, margin_top, cell_size, board_h, 14.0, 14.0)
    elif (
        not state["game_over"] and not state["ai_thinking"] and state["hover_col"] != -1
    ):
        highlight_x = margin_left + state["hover_col"] * cell_size
        painter.setBrush(QBrush(QColor(0, 229, 255, 25)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(highlight_x, margin_top, cell_size, board_h, 14.0, 14.0)

    # 5. Grid Cells & Discs
    board = state["board"]
    disc_radius = cell_size // 2 - max(6, int(cell_size * 0.1))
    for r in range(6):
        for c in range(7):
            screen_r = 5 - r
            cx = margin_left + c * cell_size + cell_size // 2
            cy = margin_top + screen_r * cell_size + cell_size // 2
            val = board[r][c]

            color = QColor("#0B111E")
            if val == 1:
                color = QColor("#FF4B4B")
            elif val == 2:
                color = boss_color if is_campaign else QColor("#FFD54F")

            if (
                state["game_over"]
                and state["win_path"]
                and val != 0
                and (r, c) not in state["win_path"]
            ):
                painter.setOpacity(0.35)

            painter.setBrush(QBrush(color))
            painter.setPen(
                QPen(QColor("#1E293B") if val == 0 else QColor("#0B111E"), 2)
            )
            painter.drawEllipse(
                QPointF(cx * 1.0, cy * 1.0), disc_radius * 1.0, disc_radius * 1.0
            )
            painter.setOpacity(1.0)

    # 6. Winning Connection Line
    if state["game_over"] and state["win_path"]:
        pen = QPen(QColor("#00E5FF"), max(6, int(cell_size * 0.12)))
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        r1, c1, r2, c2 = (
            state["win_path"][0][0],
            state["win_path"][0][1],
            state["win_path"][-1][0],
            state["win_path"][-1][1],
        )
        x1, y1 = (
            margin_left + c1 * cell_size + cell_size // 2,
            margin_top + (5 - r1) * cell_size + cell_size // 2,
        )
        x2, y2 = (
            margin_left + c2 * cell_size + cell_size // 2,
            margin_top + (5 - r2) * cell_size + cell_size // 2,
        )
        painter.drawLine(int(x1), int(y1), int(x2), int(y2))
