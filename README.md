# 🔴 CONNECT 4 — Tactical Cyberpunk AI Arena

<div align="center">

```
  ██████╗ ██████╗ ███╗   ██╗███╗   ██╗███████╗ ██████╗████████╗    ██╗  ██╗
 ██╔════╝██╔═══██╗████╗  ██║████╗  ██║██╔════╝██╔════╝╚══██╔══╝    ██║  ██║
 ██║     ██║   ██║██╔██╗ ██║██╔██╗ ██║█████╗  ██║        ██║       ███████║
 ██║     ██║   ██║██║╚██╗██║██║╚██╗██║██╔══╝  ██║        ██║       ╚════██║
 ╚██████╗╚██████╔╝██║ ╚████║██║ ╚████║███████╗╚██████╗   ██║            ██║
  ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝ ╚═════╝   ╚═╝            ╚═╝
```

**An electrifying, desktop Connect 4 duel powered by an adversarial Minimax AI engine and a sleek PyQt6 dark-mode interface.**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://pypi.org/project/PyQt6/)
[![NumPy](https://img.shields.io/badge/Matrix-NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue?style=for-the-badge)](https://www.python.org/)

[🎮 Quick Start](#-quick-start) • [🕹️ Game Modes](#-game-modes) • [⚡ Game Mechanics](#-game-mechanics) • [🧠 The AI Challenger](#-the-ai-challenger) • [📖 Documentation](#-documentation-hub)

</div>

---

## 🌟 The Experience

Welcome to **Connect 4 AI Arena** — a reimagined classic strategy game brought into a futuristic visual arena. Whether you're challenging a friend in a local pass-and-play clash or testing your wits against a high-speed **Depth-5 Minimax AI Mastermind**, every move demands tactical foresight, spatial dominance, and speed under the pressure of the blitz clock.

---

## 🕹️ Game Modes

### 🤖 1. Player vs AI (PvA) — *The Singularity Challenge*
Step into the ring against an optimized **Minimax AI** equipped with **Alpha-Beta Pruning** and center-outward tactical move ordering. 
- AI searches up to **5 moves ahead**, evaluating thousands of board states in fractions of a second.
- Can you spot the traps and conquer the machine?

### 👥 2. Player vs Player (PvP) — *Local Pass-and-Play*
Settle scores locally on the same screen. Full turn timers, session countdowns, and real-time win verification make it the ultimate tabletop digital experience.

---

## ⚡ Game Mechanics & Tactical HUD

<div align="center">

| Feature | Description |
| :--- | :--- |
| ⏱️ **Blitz Turn Clock** | A dynamic **15-second per-turn countdown** forces rapid tactical decision-making. Run out of time, and the turn automatically flips to your rival! |
| ⏳ **Match Session Timers** | Choose your pace: **3 Minutes**, **5 Minutes**, or **10 Minutes** total match durations. |
| 💡 **Tactical AI Hint** | Stuck on a move? Hit **`USE AI HINT`** to consult the engine and highlight the mathematically optimal column. |
| 📊 **Live Telemetry HUD** | A cyber-styled side panel tracks **nodes evaluated** and **computation latency (ms)** in real-time for both Minimax decisions and DFS win checks. |
| ⚡ **Laser Win Stroke** | When four discs align, a glowing cyan laser beam strikes across the winning line to celebrate victory! |
| 🔄 **Instant Rematch** | Win, lose, or draw — hit **`PLAY AGAIN`** for an instant reset without leaving the action. |

</div>

---

## 🎮 How to Play & Controls

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

- **Aim**: Move your mouse across the grid. The hovered column lights up with a subtle cyan targeting highlight.
- **Drop**: **Left-Click** on any valid column to drop your piece into the lowest available slot.
- **AI Turn**: Watch the AI think as the status bar and telemetry HUD update in real-time.
- **Hints**: Click **`USE AI HINT`** during your turn for tactical assistance.
- **Menu**: Hit **`QUIT TO MENU`** anytime to reconfigure match rules or swap game modes.

---

## 🧠 The AI Challenger

The AI is built using classical adversarial game theory, optimized for aggressive real-time tactical play:

- 🌳 **Depth-5 Minimax Tree**: Simulates future move sequences up to 5 plies deep.
- ✂️ **Alpha-Beta Cutoffs**: Aggressively prunes unpromising branches ($\alpha \ge \beta$) to cut down calculation time.
- 🎯 **Center-Outward Move Ordering**: Explores column priorities `[3, 2, 4, 1, 5, 0, 6]` to trigger instant cutoffs.
- 📐 **Sliding Window Heuristic**: Evaluates all horizontal, vertical, and diagonal 4-cell windows to value offensive trios (`+50`), defensive emergency blocks (`-800`), and center dominance (`+6`).
- ⚡ **Directional DFS Win Engine**: Employs targeted recursive Depth-First Search around the last dropped piece for instant sub-millisecond win detection.

---

## 🎨 Visual Design & Aesthetics

- **Dark Glassmorphism**: Clean `#0B111E` background paired with slate panels (`#1E293B`) and cyan accents (`#00E5FF`).
- **Ambient Radial Lighting**: Soft glowing canvas center creating depth and focus.
- **Hardware-Accelerated QPainter Canvas**: Smooth 60 FPS drawing pipeline with zero UI lag.
- **Crisp High-DPI Discs**: Saturated Crimson (`#FF4B4B`) vs Solar Gold (`#FFD54F`).

---

## 🚀 Quick Start

Launch into battle in 3 simple steps:

```bash
# 1. Clone the repository
git clone https://github.com/iamabraryeasir/Connect4-AI-Project.git
cd Connect4-AI-Project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the game!
python main.py
```

> 📖 **Need detailed setup instructions for Windows, Linux, or macOS?**  
> Check the comprehensive **[Setup & Running Guide](docs/SETUP_AND_RUN.md)**.

---

## 📖 Documentation Hub

Explore the dedicated documentation guides:

| Document | Purpose |
| :--- | :--- |
| 🛠️ **[Setup & Running Guide](docs/SETUP_AND_RUN.md)** | Step-by-step installation, virtual environment setup, platform-specific troubleshooting, and verification. |
| 🧠 **[Architecture & AI Engine](docs/ARCHITECTURE_AND_AI.md)** | In-depth algorithmic breakdowns, Minimax mathematics, heuristic scoring tables, and DFS proofs. |

---

## 🛠️ Built With

- **[Python 3.10+](https://www.python.org/)** — Core programming language.
- **[PyQt6](https://pypi.org/project/PyQt6/)** — Cross-platform GUI framework & custom `QPainter` 2D graphics engine.
- **[NumPy](https://numpy.org/)** — High-speed matrix manipulation for grid calculations.

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for details.
