# 🔴 CONNECT 4 — Adversarial AI Laboratory & Interactive Benchmark

<div align="center">

```
  ██████╗ ██████╗ ███╗   ██╗███╗   ██╗███████╗ ██████╗████████╗    ██╗  ██╗
 ██╔════╝██╔═══██╗████╗  ██║████╗  ██║██╔════╝██╔════╝╚══██╔══╝    ██║  ██║
 ██║     ██║   ██║██╔██╗ ██║██╔██╗ ██║█████╗  ██║        ██║       ███████║
 ██║     ██║   ██║██║╚██╗██║██║╚██╗██║██╔══╝  ██║        ██║       ╚════██║
 ╚██████╗╚██████╔╝██║ ╚████║██║ ╚████║███████╗╚██████╗   ██║            ██║
  ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝ ╚═════╝   ╚═╝            ╚═╝
```

**An academic-grade adversarial AI research and benchmarking platform for Connect 4, integrating a 5-tier Minimax engine with Alpha-Beta pruning, directional DFS win validation, performance telemetry, and a responsive PyQt6 evaluation interface.**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://pypi.org/project/PyQt6/)
[![NumPy](https://img.shields.io/badge/Matrix-NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue?style=for-the-badge)](https://www.python.org/)

[⚡ Quick Start](#-quick-start) • [🗺️ 5-Tier AI Benchmark](#-the-5-tier-ai-evaluation-benchmark) • [📊 Evaluation Metrics](#-evaluation-metrics--telemetry-hud) • [🧠 AI Architecture](#-ai-engine--algorithm-mechanics) • [📖 Documentation](#-documentation-hub)

</div>

---

## 🔬 Project Overview

**Connect 4 AI Laboratory** is an interactive desktop benchmark developed to demonstrate classical adversarial search algorithms, heuristic evaluation models, and multi-directional graph search within game theory. 

The system implements a parameterized **Minimax algorithm with Alpha-Beta Pruning** across 5 progressive evaluation tiers, varying search depths from 1-ply heuristic approximations to a 5-ply optimal decision engine. A live telemetry dashboard exposes real-time search latencies and explored state spaces for educational analysis and benchmarking.

---

## 🗺️ The 5-Tier AI Evaluation Benchmark

The single-player mode evaluates human-agent gameplay across 5 distinct algorithmic configurations:

<div align="center">

```
 [LEVEL 1]              [LEVEL 2]              [LEVEL 3]              [LEVEL 4]              [LEVEL 5]
  🟢 Novice Agent  ──►  🔵 Apprentice     ──►  🟡 Tactical Agent ──►  🔴 Advanced Agent ──► 🟣 Expert Agent
  1-Ply Heuristic       2-Ply Minimax          3-Ply Alpha-Beta       4-Ply Alpha-Beta       5-Ply Optimal Engine
  35% Stochastic        15% Stochastic         Deterministic          Deterministic          Deterministic
```

</div>

| Level | Agent Designation | Search Depth | Stochastic Rate | Turn Limit | Hint Quota | Algorithmic Profile |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **1** | 🟢 **Novice Agent** | Depth 1 | 35% random | 20s | 5 Hints | Baseline 1-ply evaluator assessing immediate board transitions with intentional variance. |
| **2** | 🔵 **Apprentice Agent** | Depth 2 | 15% random | 15s | 3 Hints | 2-ply lookahead evaluating direct opponent responses and blocking obvious 3-in-a-row threats. |
| **3** | 🟡 **Tactical Agent** | Depth 3 | 0% | 15s | 2 Hints | Deterministic 3-ply search with center column dominance and directional window heuristics. |
| **4** | 🔴 **Advanced Agent** | Depth 4 | 0% | 12s | 1 Hint | Deep 4-ply minimax with aggressive alpha-beta cutoffs and multi-step positioning. |
| **5** | 🟣 **Expert Agent** | Depth 5 | 0% | 10s Blitz | **Disabled** | Optimal 5-ply Alpha-Beta search exploring thousands of board states under strict time limits. |

---

## 💾 Profile Persistence & Performance Metrics

- 👤 **Local Profile Persistence**: Automatically records evaluation histories, win/loss ratios, current streaks, and unlocked tiers to `data/profile.json`.
- ⭐ **3-Star Performance Rating**:
  - **⭐⭐⭐ 3 Stars**: Optimal victory in $\le 14$ turns or finishing with $\ge 60\%$ of total session time remaining.
  - **⭐⭐ 2 Stars**: Standard victory in $15 - 22$ turns.
  - **⭐ 1 Star**: Victory by prolonged attrition or timeout.
- 🔓 **Level Progression**: Success against an AI tier unlocks the subsequent evaluation tier on the interactive level selection interface.
- 🔑 **Reset Shortcut**: Global shortcut (<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>R</kbd>) to reset profile benchmarks back to Level 1.

---

## 📊 Evaluation Metrics & Telemetry HUD

<div align="center">

| Component | Technical Description |
| :--- | :--- |
| ⏱️ **Turn Clock Controller** | Per-turn countdown timer enforcing real-time decision-making bounds. Turn automatically transitions on expiration. |
| ⏳ **Match Session Timers** | Configurable match durations: **3 Minutes**, **5 Minutes**, or **10 Minutes**. |
| 💡 **Advisory Hint Engine** | Calls the Minimax evaluator at runtime to highlight the mathematically optimal column choice based on current heuristic weights. |
| 📊 **Real-Time Search Telemetry** | Dedicated side panels display exact **node exploration counts** and **computation latency (ms)** for both Minimax moves and DFS win checks. |
| ⚡ **Directional Win Indicator** | Dynamic cyan connection vector rendering the precise 4-in-a-row coordinates upon terminal win states. |

</div>

---

## 🎮 Evaluation Interface & User Controls

```
             Hover to Target Column ──► [ ▼ ]
                                       [   ] [   ] [   ] [   ] [   ] [   ] [   ]
                                       [   ] [   ] [   ] [   ] [   ] [   ] [   ]
                                       [   ] [   ] [ 🔴] [ 🟡] [   ] [   ] [   ]
                                       [   ] [ 🔴] [ 🟡] [ 🔴] [   ] [   ] [   ]
                                       [ 🟡] [ 🔴] [ 🔴] [ 🟡] [   ] [   ] [   ]
                                       [ 🔴] [ 🟡] [ 🟡] [ 🔴] [ 🟡] [   ] [   ]
                                         0     1     2     3     4     5     6
```

- **Targeting**: Hover cursor across columns to see the column highlight indicator.
- **Move Execution**: **Left-Click** to drop a disc into the lowest available row of the target column.
- **AI Hints**: Click **`USE AI HINT`** during your turn to query the advisory heuristic engine.
- **Level Navigation**: Click **`LEVEL SELECT`** to navigate to the benchmark roadmap or choose another tier.

---

## 🧠 AI Engine & Algorithm Mechanics

### 1. Minimax Algorithm with Alpha-Beta Pruning
The adversarial decision engine evaluates zero-sum game trees up to depth $d$:

$$\text{Minimax}(s, d, \alpha, \beta) = \begin{cases}
\text{Utility}(s) & \text{if } d = 0 \text{ or terminal}(s) \\
\max_{a \in \text{Actions}(s)} \text{Minimax}(\text{Result}(s, a), d-1, \alpha, \beta) & \text{if Maximizing (AI)} \\
\min_{a \in \text{Actions}(s)} \text{Minimax}(\text{Result}(s, a), d-1, \alpha, \beta) & \text{if Minimizing (Human)}
\end{cases}$$

Branches are pruned when $\alpha \ge \beta$, cutting branch evaluation counts by up to $80\%$.

### 2. Center-Outward Column Ordering
Columns are visited in order $\text{COLUMN\_ORDER} = [3, 2, 4, 1, 5, 0, 6]$ to discover high-utility central lines early and maximize early alpha-beta cutoffs.

### 3. Heuristic Evaluation Weights
Non-terminal leaf positions are scored using a 4-slot sliding window algorithm:

| Evaluation Pattern | Assigned Weight | Strategic Purpose |
| :--- | :---: | :--- |
| **4 AI Discs** | `+100,000` | Terminal win condition |
| **Opponent 3 Discs + 1 Empty** | `-800` | Immediate mandatory block |
| **AI 3 Discs + 1 Empty** | `+50` | High-priority offensive setup |
| **AI 2 Discs + 2 Empty** | `+10` | Early-game formation building |
| **Center Column Control** | `+6` / disc | Central geometric dominance multiplier |

---

## ⚡ Quick Start

Launch the evaluation platform in 3 steps:

```bash
# 1. Clone the repository
git clone https://github.com/iamabraryeasir/Connect4-AI-Project.git
cd Connect4-AI-Project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the application
python main.py
```

> 📖 **Looking for OS-specific installation and troubleshooting steps?**  
> Refer to the **[Setup & Running Guide](docs/SETUP_AND_RUN.md)**.

---

## 📖 Documentation Hub

| Document | Description |
| :--- | :--- |
| 🛠️ **[Setup & Running Guide](docs/SETUP_AND_RUN.md)** | Step-by-step virtual environment setup, package dependencies, platform troubleshooting, and headless tests. |
| 🧠 **[Architecture & AI Specifications](docs/ARCHITECTURE_AND_AI.md)** | Full technical documentation of Minimax formulations, sliding window heuristics, DFS directional vectors, and profile schemas. |

---

## 🛠️ Built With

- **[Python 3.10+](https://www.python.org/)** — Core implementation language.
- **[PyQt6](https://pypi.org/project/PyQt6/)** — Cross-platform GUI framework and responsive `QPainter` 2D graphics canvas.
- **[NumPy](https://numpy.org/)** — High-performance multidimensional array matrix operations.

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for details.
