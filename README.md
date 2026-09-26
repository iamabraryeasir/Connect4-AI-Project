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

**An electrifying desktop Connect 4 campaign featuring a 5-Stage AI Boss Gauntlet, local player account persistence, star-rating unlocks, and a sleek PyQt6 dark-mode interface.**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://pypi.org/project/PyQt6/)
[![NumPy](https://img.shields.io/badge/Matrix-NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue?style=for-the-badge)](https://www.python.org/)

[🎮 Quick Start](#-quick-start) • [🗺️ The 5-Stage Campaign](#-the-5-stage-campaign) • [💾 Profile & Star Progression](#-profile--star-progression) • [⚡ Tactical HUD](#-tactical-hud--game-mechanics) • [📖 Documentation](#-documentation-hub)

</div>

---

## 🌟 The Experience

Welcome to **Connect 4 AI Arena** — where classic four-in-a-row strategy meets a progressive single-player campaign. Rise through a gauntlet of 5 distinct AI entities, each possessing unique search depths, mistake probabilities, and blitz turn restrictions. Build your local career profile, unlock higher stages, earn up to **3 Stars (★★★)** per victory, and face the unbeatable **Omega AI Boss**!

---

## 🗺️ The 5-Stage Campaign

Battle through an escalating hierarchy of AI adversaries:

<div align="center">

```
 [STAGE 1]           [STAGE 2]           [STAGE 3]           [STAGE 4]           [STAGE 5]
  🟢 SPARK    ──►     🔵 CIRCUIT   ──►     🟡 VECTOR   ──►     🔴 NEXUS    ──►     🟣 OMEGA
  (Novice)          (Apprentice)         (Tactician)        (Grandmaster)        (God Mode Boss)
  Depth 1             Depth 2             Depth 3             Depth 4             Depth 5
  35% Blunder         15% Blunder         0% Blunder          0% Blunder          Blitz Pressure
```

</div>

| Stage | AI Boss | Difficulty | Turn Clock | AI Hints | Tactical Profile |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **1** | 🟢 **Spark** | Novice | 20s | 5 Hints | Shallow 1-ply search; prone to tactical oversights; generous hint assistance. |
| **2** | 🔵 **Circuit** | Apprentice | 15s | 3 Hints | 2-ply search with basic positional awareness; blocks immediate 3-in-a-row lines. |
| **3** | 🟡 **Vector** | Tactician | 15s | 2 Hints | 3-ply heuristic search with aggressive center control; zero blunders. |
| **4** | 🔴 **Nexus** | Grandmaster | 12s | 1 Hint | 4-ply Alpha-Beta search; sets up multi-pronged fork attacks. |
| **5** | 🟣 **Omega** | God Mode Boss | 10s Blitz | **Disabled** | 5-ply Alpha-Beta search under 10s blitz time limits; zero hints allowed! |

---

## 💾 Profile & Star Progression

- 👤 **Local Player Account**: Automatically persists player name, total wins/losses, win streaks, and unlocked stages to `data/profile.json`.
- ⭐ **3-Star Rating System**:
  - **⭐⭐⭐ 3 Stars**: Decisive victory in $\le 14$ turns or finishing with $\ge 60\%$ match time remaining.
  - **⭐⭐ 2 Stars**: Tactical victory in $15 - 22$ turns.
  - **⭐ 1 Star**: Grinding victory by attrition or clock timeout.
- 🔓 **Stage Unlocks**: Defeating an AI boss unlocks the next stage on the interactive Level Select roadmap.

---

## ⚡ Tactical HUD & Game Mechanics

<div align="center">

| Feature | Description |
| :--- | :--- |
| ⏱️ **Blitz Turn Clock** | Per-turn countdown timer forces rapid decision-making. If time expires, the turn passes to your opponent! |
| ⏳ **Match Session Timers** | Configurable overall match durations: **3 Minutes**, **5 Minutes**, or **10 Minutes**. |
| 💡 **Tactical AI Hint** | Hit **`USE AI HINT`** during your turn to highlight the mathematically optimal column. |
| 📊 **Real-Time Telemetry HUD** | Cyber-styled side cards display live node counts and computation latency (ms) for Minimax decisions and DFS checks. |
| ⚡ **Laser Win Stroke** | When four discs connect, a glowing cyan beam strikes across the winning line. |
| 🔄 **Instant Rematch** | Hit **`PLAY AGAIN`** to immediately retry a stage or challenge your previous star record. |

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

- **Aim**: Move your cursor across the columns to highlight the target slot.
- **Drop**: **Left-Click** to drop your disc into the lowest open row.
- **Hints**: Click **`USE AI HINT`** for tactical assistance.
- **Stage Navigation**: Return to the **Level Select Screen** anytime to view your stars or select a new challenge.

---

## 🎨 Visual Design & Aesthetics

- **Dark Glassmorphism**: Slate panels (`#1E293B`) against deep navy (`#0B111E`) with vibrant neon accents.
- **Hardware-Accelerated QPainter Canvas**: Smooth 60 FPS drawing pipeline with zero lag.
- **Interactive Level Map**: Visual stage cards displaying boss codenames, star badges, and lock/unlock indicators.

---

## 🚀 Quick Start

Launch into the campaign in 3 simple steps:

```bash
# 1. Clone the repository
git clone https://github.com/iamabraryeasir/Connect4-AI-Project.git
cd Connect4-AI-Project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the game
python main.py
```

> 📖 **Need detailed setup instructions for Windows, Linux, or macOS?**  
> Read the complete **[Setup & Running Guide](docs/SETUP_AND_RUN.md)**.

---

## 📖 Documentation Hub

| Document | Purpose |
| :--- | :--- |
| 🛠️ **[Setup & Running Guide](docs/SETUP_AND_RUN.md)** | Step-by-step installation, virtual environment management, platform troubleshooting, and headless tests. |
| 🧠 **[Architecture & AI Engine](docs/ARCHITECTURE_AND_AI.md)** | In-depth technical specifications, Minimax Alpha-Beta mathematics, sliding window heuristics, and DFS proofs. |

---

## 🛠️ Built With

- **[Python 3.10+](https://www.python.org/)** — Core language.
- **[PyQt6](https://pypi.org/project/PyQt6/)** — Desktop GUI framework & custom `QPainter` 2D graphics engine.
- **[NumPy](https://numpy.org/)** — Accelerated matrix operations for grid representation.

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for details.
