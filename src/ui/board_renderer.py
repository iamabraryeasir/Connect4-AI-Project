from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QBrush, QColor, QFont, QLinearGradient, QPen, QRadialGradient

from src.core import game_logic

CELL_SIZE = 85
MARGIN_TOP = 120
MARGIN_LEFT = 30
BOARD_WIDTH = 7 * CELL_SIZE
BOARD_HEIGHT = 6 * CELL_SIZE
PANEL_WIDTH = 280
WINDOW_WIDTH = BOARD_WIDTH + 2 * MARGIN_LEFT + PANEL_WIDTH
WINDOW_HEIGHT = BOARD_HEIGHT + MARGIN_TOP + 30


def get_column_from_x(x):
    if MARGIN_LEFT <= x < MARGIN_LEFT + BOARD_WIDTH:
        return min(int((x - MARGIN_LEFT) // CELL_SIZE), 6)
    return -1


def draw_game(painter, state):
    # 1. Ambient Background Canvas
    bg_gradient = QLinearGradient(0, 0, 0, WINDOW_HEIGHT)
    bg_gradient.setColorAt(0.0, QColor("#0B111E"))
    bg_gradient.setColorAt(1.0, QColor("#111827"))
    painter.fillRect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, bg_gradient)

    glow = QRadialGradient(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, 450)
    glow.setColorAt(0.0, QColor(0, 229, 255, 12))
    glow.setColorAt(1.0, QColor(0, 0, 0, 0))
    painter.setBrush(QBrush(glow))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    # 2. Top Header Status Bar
    if state["game_over"]:
        if state["winner"] == -1:
            text, color = "GAME OVER  •  DRAW / TIMEOUT", QColor("#94A3B8")
        else:
            p_name = (
                "Player 1"
                if state["winner"] == 1
                else ("AI" if state["mode"] == "pva" else "Player 2")
            )
            text, color = (
                f"{p_name.upper()} WINS THE MATCH!",
                QColor("#FF4B4B") if state["winner"] == 1 else QColor("#FFD54F"),
            )
    elif state["ai_thinking"]:
        text, color = "AI IS THINKING...", QColor("#FFD54F")
    else:
        turns_left = (
            f" (Move {3 - state['consecutive_turns']} of 2)"
            if state["consecutive_turns"] > 1
            else ""
        )
        player_name = (
            "Player 1"
            if state["current_player"] == 1
            else ("AI" if state["mode"] == "pva" else "Player 2")
        )
        text = f"CURRENT TURN: {player_name.upper()}{turns_left}"
        color = QColor("#FF4B4B") if state["current_player"] == 1 else QColor("#FFD54F")

    painter.setPen(QPen(color))
    painter.setFont(QFont("Arial", 16, QFont.Weight.Bold))
    painter.drawText(MARGIN_LEFT, 55, text)

    # Indicator Dot
    painter.setBrush(QBrush(color))
    painter.setPen(Qt.PenStyle.NoPen)
    dot_x = MARGIN_LEFT + painter.fontMetrics().horizontalAdvance(text) + 16
    painter.drawEllipse(QPointF(dot_x, 48.0), 7.0, 7.0)

    # 3. Stats Panel (Right Side Cards)
    panel_x = MARGIN_LEFT + BOARD_WIDTH + 30
    panel_w = PANEL_WIDTH - 30

    card_style_pen = QPen(QColor("#334155"), 1)
    card_bg_brush = QBrush(QColor("#1E293B"))

    # Card 1: Timers
    painter.setPen(card_style_pen)
    painter.setBrush(card_bg_brush)
    painter.drawRoundedRect(panel_x, MARGIN_TOP, panel_w, 100, 12.0, 12.0)

    painter.setPen(QColor("#64748B"))
    painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
    painter.drawText(panel_x + 16, MARGIN_TOP + 24, "MATCH TIMERS")

    mins, secs = divmod(state["session_time"], 60)
    time_str = f"{mins:02}:{secs:02}"

    painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))
    painter.setPen(
        QColor("#F8FAFC") if state["session_time"] > 60 else QColor("#FF4B4B")
    )
    painter.drawText(panel_x + 16, MARGIN_TOP + 52, f"Session: {time_str}")

    turn_color = QColor("#FFD54F") if state["turn_time"] <= 5 else QColor("#00E5FF")
    painter.setPen(turn_color)
    painter.drawText(
        panel_x + 16, MARGIN_TOP + 76, f"Turn Clock: {state['turn_time']}s"
    )

    # Card 2: DFS Win Checker Metrics
    y_card2 = MARGIN_TOP + 116
    painter.setPen(card_style_pen)
    painter.setBrush(card_bg_brush)
    painter.drawRoundedRect(panel_x, y_card2, panel_w, 105, 12.0, 12.0)

    painter.setPen(QColor("#64748B"))
    painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
    painter.drawText(panel_x + 16, y_card2 + 24, "DFS (WIN CHECKER)")

    painter.setFont(QFont("Arial", 11))
    painter.setPen(QColor("#00E5FF"))
    painter.drawText(
        panel_x + 16, y_card2 + 52, f"Nodes: {state.get('dfs_nodes', 0):,}"
    )
    painter.drawText(
        panel_x + 16, y_card2 + 78, f"Time: {state.get('dfs_time', 0):.3f} ms"
    )

    # Card 3: Minimax AI Metrics
    y_card3 = y_card2 + 121
    painter.setPen(card_style_pen)
    painter.setBrush(card_bg_brush)
    painter.drawRoundedRect(panel_x, y_card3, panel_w, 105, 12.0, 12.0)

    painter.setPen(QColor("#64748B"))
    painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
    painter.drawText(panel_x + 16, y_card3 + 24, "MINIMAX AI ENGINE")

    painter.setFont(QFont("Arial", 11))
    ai_metric_color = (
        QColor("#00E5FF") if not state.get("ai_thinking") else QColor("#FFD54F")
    )
    painter.setPen(ai_metric_color)
    painter.drawText(panel_x + 16, y_card3 + 52, f"Nodes: {state.get('ai_nodes', 0):,}")
    painter.drawText(
        panel_x + 16, y_card3 + 78, f"Time: {state.get('ai_time', 0):.3f} ms"
    )

    # 4. Board Container
    painter.setBrush(QBrush(QColor("#172030")))
    painter.setPen(QPen(QColor("#334155"), 2))
    painter.drawRoundedRect(
        MARGIN_LEFT, MARGIN_TOP, BOARD_WIDTH, BOARD_HEIGHT, 16.0, 16.0
    )

    # Column Hover Highlight
    if state.get("hint_active") and state["hint_col"] != -1:
        highlight_x = MARGIN_LEFT + state["hint_col"] * CELL_SIZE
        painter.setBrush(QBrush(QColor(255, 213, 79, 45)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(
            highlight_x, MARGIN_TOP, CELL_SIZE, BOARD_HEIGHT, 14.0, 14.0
        )
    elif (
        not state["game_over"] and not state["ai_thinking"] and state["hover_col"] != -1
    ):
        highlight_x = MARGIN_LEFT + state["hover_col"] * CELL_SIZE
        painter.setBrush(QBrush(QColor(0, 229, 255, 25)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(
            highlight_x, MARGIN_TOP, CELL_SIZE, BOARD_HEIGHT, 14.0, 14.0
        )

    # 5. Grid Cells & Discs
    board = state["board"]
    for r in range(6):
        for c in range(7):
            screen_r = 5 - r
            cx = MARGIN_LEFT + c * CELL_SIZE + CELL_SIZE // 2
            cy = MARGIN_TOP + screen_r * CELL_SIZE + CELL_SIZE // 2
            val = board[r][c]

            color = QColor("#0B111E")
            if val == 1:
                color = QColor("#FF4B4B")
            elif val == 2:
                color = QColor("#FFD54F")

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
                QPointF(cx * 1.0, cy * 1.0), CELL_SIZE // 2 - 9.0, CELL_SIZE // 2 - 9.0
            )
            painter.setOpacity(1.0)

    # 6. Winning Connection Line
    if state["game_over"] and state["win_path"]:
        pen = QPen(QColor("#00E5FF"), 10)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        r1, c1, r2, c2 = (
            state["win_path"][0][0],
            state["win_path"][0][1],
            state["win_path"][-1][0],
            state["win_path"][-1][1],
        )
        x1, y1 = (
            MARGIN_LEFT + c1 * CELL_SIZE + CELL_SIZE // 2,
            MARGIN_TOP + (5 - r1) * CELL_SIZE + CELL_SIZE // 2,
        )
        x2, y2 = (
            MARGIN_LEFT + c2 * CELL_SIZE + CELL_SIZE // 2,
            MARGIN_TOP + (5 - r2) * CELL_SIZE + CELL_SIZE // 2,
        )
        painter.drawLine(int(x1), int(y1), int(x2), int(y2))
