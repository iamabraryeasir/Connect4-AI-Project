# 🔴 CONNECT 4 — Advanced AI Engine & Desktop GUI

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://pypi.org/project/PyQt6/)
[![NumPy](https://img.shields.io/badge/Matrix-NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue?style=for-the-badge)](https://www.python.org/)

An academic-grade, modular desktop implementation of **Connect 4** built with **Python 3**, **PyQt6**, and **NumPy**. The project integrates an adversarial **Minimax AI Engine with Alpha-Beta Pruning**, **Center-Outward Move Ordering**, **Depth-First Search (DFS) directional win verification**, and a high-performance **QPainter 2D graphics pipeline** featuring real-time algorithm performance telemetry.

---

## 📑 Table of Contents

- [Key Features](#-key-features)
- [Project Architecture](#-project-architecture)
- [Module Breakdown](#-module-breakdown)
- [AI Engine & Algorithm Mechanics](#-ai-engine--algorithm-mechanics)
  - [1. Minimax with Alpha-Beta Pruning](#1-minimax-with-alpha-beta-pruning)
  - [2. Move Ordering Optimization](#2-move-ordering-optimization)
  - [3. Heuristic Evaluation Function](#3-heuristic-evaluation-function)
  - [4. DFS Directional Win Detection](#4-dfs-directional-win-detection)
- [Game Modes & State Rules](#-game-modes--state-rules)
- [Installation & Getting Started](#-installation--getting-started)
- [Controls & User Guide](#-controls--user-guide)
- [Tech Stack](#-tech-stack)
- [License](#-license)

---

## 🌟 Key Features

- 🤖 **Adversarial Minimax AI Engine (Depth 5 Search)**
  - Recursive minimax search tree evaluation enhanced with **Alpha-Beta Cutoffs** ($\alpha \ge \beta$).
  - Evaluates tens of thousands of board states in sub-second latency with tactical heuristic weights.

- ⚡ **Center-Outward Move Ordering**
  - Prioritizes searching high-potential central columns (`[3, 2, 4, 1, 5, 0, 6]`) first to maximize early alpha-beta branch pruning.

- 🔍 **DFS Directional Win Validation**
  - Explores linear and diagonal axes recursively from the last played piece to identify four-in-a-row alignments with exact coordinate tracking.

- 📊 **Live Performance Telemetry Cards**
  - Real-time side panel displaying nodes evaluated and execution duration (in milliseconds) for both the Minimax search and the DFS win validator.

- ⏱️ **Match & Turn Clock Management**
  - Configurable match session clocks (3, 5, or 10 minutes) alongside a dynamic 15-second per-turn countdown.

- 💡 **Tactical AI Hint System**
  - Built-in hint advisor analyzing the current grid position and highlighting the mathematically optimal column.

- 🎨 **Futuristic PyQt6 UI / UX**
  - Custom dark glassmorphism theme, ambient radial background glow, smooth column hover highlights, and dynamic winning stroke lines.

---

## 🏗️ Project Architecture

The codebase enforces strict separation of concerns across logic, state, algorithms, and rendering:

```
connect4_project/
├── main.py                     # Application entry point & Qt event loop bootstrap
├── requirements.txt            # Project dependencies
├── README.md                   # Complete project documentation
└── src/
    ├── ai/
    │   ├── __init__.py
    │   ├── minimax.py          # Minimax algorithm, Alpha-Beta pruning & Heuristic scoring
    │   └── win_checker.py      # Multi-directional DFS win condition checker
    ├── core/
    │   ├── __init__.py
    │   └── game_logic.py       # NumPy matrix operations, piece drops & grid validation
    ├── state/
    │   ├── __init__.py
    │   └── game_state.py       # Central state manager, turn engine & clock tick loops
    └── ui/
        ├── __init__.py
        ├── app_controller.py   # QStackedWidget navigation & launcher start screen
        ├── board_renderer.py  # 2D QPainter graphics engine & telemetry card renderer
        └── game_window.py     # Game canvas event handlers, timers & user actions
```

---

## 🧩 Module Breakdown

### 1. Core Logic (`src/core/game_logic.py`)
- **Grid Representation**: Maintains a $6 \times 7$ 2D NumPy array with row indices $0$ (bottom) to $5$ (top).
- `create_board()`: Initializes a zero-filled NumPy matrix.
- `drop_piece(board, row, col, piece)`: Places the active player's disc into the designated cell.
- `is_valid_location(board, col)`: Validates whether a given column has available space.
- `get_next_open_row(board, col)`: Finds the lowest unoccupied row index in a target column.
- `is_board_full(board)`: Detects stalemate scenarios where no legal moves remain.

### 2. AI Engine (`src/ai/minimax.py` & `src/ai/win_checker.py`)
- **`minimax.py`**: Executes recursive minimax search with alpha-beta bounds, center-weighted column permutations, and positional evaluation.
- **`win_checker.py`**: Multi-directional Depth-First Search traversing the 4 primary axes (Horizontal, Vertical, Positive Diagonal, Negative Diagonal) starting from the last played piece coordinates.

### 3. State Engine (`src/state/game_state.py`)
- Centralized immutable-style state dictionary containing:
  - Board matrix, current turn, game over status, and winner identifier.
  - Performance telemetry metrics (`dfs_nodes`, `dfs_time`, `ai_nodes`, `ai_time`).
  - Session clock, per-turn timers, consecutive turns tracker, and hint flags.
- Dispatches move actions, handles turn transitions, applies hint rewards/penalties, and coordinates AI execution.

### 4. User Interface & Rendering (`src/ui/`)
- **`app_controller.py`**: Hosts `AppController` (`QStackedWidget`) managing transitions between the start screen (`StartScreen`) and the active game view (`GameWindow`).
- **`board_renderer.py`**: Pure `QPainter` drawing pipeline handling the ambient background gradient, disc slots, hover overlays, win-line indicators, and telemetry stat panels.
- **`game_window.py`**: Receives mouse events, manages Qt clocks (`QTimer`), coordinates AI response single-shots, and handles instant rematch actions.

---

## 🧠 AI Engine & Algorithm Mechanics

### 1. Minimax with Alpha-Beta Pruning

The AI models Connect 4 as a two-player, zero-sum game of perfect information. The minimax value of state $s$ at depth $d$ is determined by:

$$\text{Minimax}(s, d) = \begin{cases} 
\text{Utility}(s) & \text{if } d = 0 \text{ or terminal}(s) \\
\max_{a \in \text{Actions}(s)} \text{Minimax}(\text{Result}(s, a), d-1) & \text{if Maximizing (AI)} \\
\min_{a \in \text{Actions}(s)} \text{Minimax}(\text{Result}(s, a), d-1) & \text{if Minimizing (Player)}
\end{cases}$$

**Alpha-Beta Cutoffs**:
- $\alpha$: Highest score guaranteed to the maximizing player so far.
- $\beta$: Lowest score guaranteed to the minimizing player so far.
- If $\alpha \ge \beta$, the current branch is pruned immediately without evaluating remaining siblings.

```
                  [Max Node] (α = -inf, β = +inf)
                  /         \
                 /           \
     [Min Node]               [Min Node] (Pruned when α >= β)
      /      \
  Leaf(5)   Leaf(3)
```

### 2. Move Ordering Optimization

Alpha-Beta pruning efficiency depends heavily on the order in which child nodes are visited. Connect 4 dynamics favor central column control; therefore, child states are explored from the center outward:

$$\text{COLUMN\_ORDER} = [3, 2, 4, 1, 5, 0, 6]$$

Starting search exploration at column $3$ (the physical center) yields higher evaluation scores earlier, allowing the algorithm to maximize cutoffs and prune significantly larger sub-trees.

### 3. Heuristic Evaluation Function

When reaching maximum search depth ($d = 5$) on non-terminal states, the engine scores the board using a 4-slot sliding window algorithm across all horizontal, vertical, and diagonal lines:

| Window Pattern / Condition | Score Value | Tactical Rationale |
| :--- | :--- | :--- |
| **4 AI Pieces** | `+100,000` | Terminal / immediate AI victory |
| **Opponent 3 Pieces + 1 Empty** | `-800` | High-threat defense: mandatory block |
| **AI 3 Pieces + 1 Empty** | `+50` | High-priority offensive setup |
| **AI 2 Pieces + 2 Empty** | `+10` | Early-game potential structure building |
| **Center Column Control** | `+6` / piece | Board center dominance multiplier |

---

### 4. DFS Directional Win Detection

Rather than scanning the entire $6 \times 7$ grid after each move, `win_checker.py` performs a targeted directional Depth-First Search centered at the coordinates of the newly placed piece `(last_row, last_col)`:

$$\text{Axes} = \{ \text{Horizontal: } (0, \pm 1), \text{Vertical: } (\pm 1, 0), \text{Diag } /: (\pm 1, \pm 1), \text{Diag } \backslash: (\pm 1, \mp 1) \}$$

For each axis, DFS explores both positive and negative directions recursively:
$$\text{Total Streak} = 1 + \text{count}(\vec{d}_1) + \text{count}(\vec{d}_2)$$
If $\text{Total Streak} \ge 4$, a victory is declared and the complete ordered streak path is passed to `board_renderer.py` to draw the winning connection line.

---

## 🎮 Game Modes & State Rules

1. **Player vs AI (PvA)**
   - Battle against the Depth-5 Minimax AI engine.
   - The AI takes calculated turns with realistic reaction delays.
2. **Player vs Player (PvP)**
   - Local pass-and-play two-player mode on the same device.
3. **AI Tactical Hint (`USE AI HINT`)**
   - Human players can request a move suggestion during their turn.
   - Highlights the optimal column calculated by the AI engine.
4. **Time Controls**
   - **Match Duration**: Configurable to 3, 5, or 10 minutes.
   - **Turn Clock**: 15 seconds per move. If time expires, the turn automatically flips to the opponent.
5. **Instant Rematch**
   - Upon victory, defeat, or timeout, a `PLAY AGAIN` button appears on the side panel to reset the board instantly.

---

## 🚀 Installation & Getting Started

### Prerequisites

- **Python 3.10+**
- **pip** package manager

### 1. Clone the Repository

```bash
git clone https://github.com/iamabraryeasir/Connect4-AI-Project.git
cd Connect4-AI-Project
```

### 2. Set Up Virtual Environment

- **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\activate
  ```
- **Linux / macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the Game

```bash
python main.py
```

---

## 🕹️ Controls & User Guide

- **Mouse Hover**: Move cursor across columns to see the column highlight indicator.
- **Left Click**: Drop a disc into the hovered column.
- **QUIT TO MENU**: Return to the launcher screen to reconfigure match settings.
- **USE AI HINT**: Consult the Minimax engine for tactical recommendation.
- **PLAY AGAIN / RESTART GAME**: Reset the board with existing configuration.

---

## 🛠️ Tech Stack

- **[Python 3.10+](https://www.python.org/)** — Core language.
- **[PyQt6](https://pypi.org/project/PyQt6/)** — Cross-platform GUI framework and 2D hardware-accelerated canvas renderer.
- **[NumPy](https://numpy.org/)** — High-performance multidimensional array manipulation for matrix states.

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.
