# 🔴 CONNECT 4 — Advanced AI Engine & Interactive GUI

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://pypi.org/project/PyQt6/)
[![NumPy](https://img.shields.io/badge/Matrix-NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

An industry-standard, desktop Connect 4 application featuring a **Minimax AI Engine with Alpha-Beta Pruning**, **Depth-First Search (DFS)** win validation, **Holographic Ghost Piece trajectory projection**, and a custom **PyQt6 dark-mode interface** with real-time performance telemetry.

---

## 🌟 Key Features

- 🤖 **Minimax AI Engine (Depth 5 Search)**
    - Powered by Alpha-Beta pruning with custom heuristic evaluation.
    - Implements **Center-Outward Move Ordering** (`[3, 2, 4, 1, 5, 0, 6]`) to maximize pruning efficiency and cut down node evaluation trees.
- 🔮 **Holographic Ghost Pieces (Principal Variation Line)**
    - Projects the AI's predicted sequence of future moves on the board in real-time.
    - Translucent red dashed rings depict expected human counter-moves, while yellow dashed rings show planned AI follow-ups.
- ⚡ **DFS Win Checker & Real-Time Telemetry**
    - Optimized Depth-First Search win condition evaluation.
    - Live side panel displaying computation metrics (Nodes explored, search latency in ms) for both Minimax and DFS routines.
- 🎨 **Futuristic UI / UX Design System**
    - Built with PyQt6 featuring ambient canvas lighting, smooth radial gradients, hover indicators, and glassmorphism styling.
- ⏱️ **Match & Turn Clock Controllers**
    - Configurable match session timers (1, 3, 5 mins, or infinite) with per-turn countdown clocks.
- 💡 **AI Hint System & Instant Rematch**
    - Tactical "USE AI HINT" button to assist human players.
    - Dynamic **PLAY AGAIN** restart trigger that appears seamlessly upon game completion.

---

## 🏗️ Project Architecture

```
connect4_project/
├── main.py                    # Application entry point
├── requirements.txt           # Dependency specifications
├── README.md                  # Project documentation
└── src/
    ├── ai/
    │   ├── minimax.py         # Minimax algorithm, Alpha-Beta pruning & Move Ordering
    │   └── win_checker.py     # DFS directional win checking algorithm
    ├── core/
    │   └── game_logic.py      # Grid matrix state, drop mechanics, location validation
    ├── state/
    │   └── game_state.py      # Immutable-style state manager & turn flow controller
    └── ui/
        ├── app_controller.py  # Navigation, main window & launcher screen
        ├── board_renderer.py # High-performance QPainter 2D graphics engine
        └── game_window.py    # Game view manager & UI event handling
```

---

## 🧠 AI Engine & Algorithm Mechanics

### 1. Minimax with Alpha-Beta Pruning & Move Ordering

The AI evaluates game trees using the Minimax theorem. To achieve optimal performance at **Depth 5**, moves are evaluated using center-outward column ordering:

$$\text{COLUMN\\_ORDER} = [3, 2, 4, 1, 5, 0, 6]$$

Evaluating column 3 (the center column) first maximizes the probability of finding high-value utility scores early, triggering aggressive **Alpha-Beta cutoffs** ($\alpha \ge \beta$) and pruning unnecessary branches.

### 2. Heuristic Scoring Function

Positions are evaluated across all 4-slot sliding windows (Horizontal, Vertical, Diagonals) and center column control:

| Window Pattern / Condition      | Score Weight   | Tactical Objective           |
| :------------------------------ | :------------- | :--------------------------- |
| **4 Pieces in a Row**           | `+100,000`     | Immediate Victory            |
| **Opponent 3 Pieces + 1 Empty** | `-800`         | Critical Mandatory Block     |
| **3 Pieces + 1 Empty**          | `+50`          | High-Priority Attack Setup   |
| **2 Pieces + 2 Empty**          | `+10`          | Early Game Position Building |
| **Center Column Control**       | `+6` per piece | Dominating the board center  |

### 3. Holographic Ghost Pieces (Principal Variation)

The AI returns its **Principal Variation (PV)**—the optimal path sequence assuming rational play from both sides. The renderer projects this path onto the board:

- **Red Dashed Ring** ($\text{Opacity } 0.35$): Anticipated Human move.
- **Yellow Dashed Ring** ($\text{Opacity } 0.35$): Planned AI counter-move.

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** installed on your system.

### Installation

1. **Clone the Repository**

    ```bash
    https://github.com/iamabraryeasir/Connect4-AI-Project.git
    cd Connect4-AI-Project
    ```

2. **Create a Virtual Environment**
    - **Windows:**
        ```powershell
        python -m venv .venv
        .\.venv\Scripts\activate
        ```
    - **Linux / macOS:**
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Launch the Game**
    ```bash
    python main.py
    ```

---

## 🕹️ Game Modes & Controls

- **Player vs AI (PvA)**: Battle against the Depth-5 Minimax AI engine.
- **Player vs Player (PvP)**: Pass-and-play local multiplayer mode.
- **AI Hint**: Click `USE AI HINT` during your turn to highlight the recommended column.
- **Play Again**: Click `PLAY AGAIN` on the right side panel after game completion to instantly restart a match.

---

## 🛠️ Built With

- **[Python](https://www.python.org/)** — Core programming language.
- **[PyQt6](https://pypi.org/project/PyQt6/)** — Cross-platform GUI framework and QPainter graphics pipeline.
- **[NumPy](https://numpy.org/)** — High-performance 2D matrix manipulation for game board representations.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.
