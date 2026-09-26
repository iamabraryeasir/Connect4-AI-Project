# 🧠 Technical Architecture & AI Engine Specification

This document details the mathematical modeling, algorithmic designs, data structures, state management architecture, and local profile persistence of the **Connect 4 AI Project** with its **Campaign Level Progression System**.

---

## 🏗️ Architectural Topology

The project follows a decoupled layered architecture ensuring clean boundaries between mathematical game state, AI search routines, profile persistence, and graphics rendering:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            Presentation Layer                               │
│  AppController (QStackedWidget)                                             │
│  ├── StartScreen (Profile banner, Mode Selection)                           │
│  ├── LevelSelectScreen (Stage Roadmap, Stars, Boss Cards, Unlocks)          │
│  └── GameWindow (HUD, Clocks, Discs, Win Line, Modal Overlays)              │
│       └── board_renderer (Custom QPainter Graphics Pipeline)                │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Reads State & Paints
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              State Manager                                  │
│                        src.state.game_state                                 │
│  (Central State Dict, Active Level Context, Move Execution, Clock Loops)    │
└──────────────┬───────────────────────┬───────────────────────┬──────────────┘
               │                       │                       │
               ▼                       ▼                       ▼
┌────────────────────────┐ ┌────────────────────────┐ ┌──────────────────────┐
│       AI Engine        │ │   Profile & Levels     │ │     Core Logic       │
│  src.ai.minimax        │ │  src.profile.manager   │ │ src.core.game_logic  │
│  - Configurable Depth  │ │  - profile.json CRUD   │ │ - 6x7 NumPy Matrix   │
│  - Blunder Injection   │ │  - Star Calculation    │ │ - Drop mechanics     │
│  - Alpha-Beta Pruning  │ │  src.levels.config     │ │ - Boundary checks    │
│  - Heuristic Scorer    │ │  - 5-Tier Level Specs  │ │                      │
│  src.ai.win_checker    │ │                        │ │                      │
│  - Directional DFS     │ │                        │ │                      │
└────────────────────────┘ └────────────────────────┘ └──────────────────────┘
```

---

## 🗺️ Campaign Level & AI Difficulty Model

The single-player campaign features a 5-tier progressive difficulty curve designed to ease newcomers in while challenging advanced players at higher stages.

| Level | Boss Codename | Search Depth | Blunder Rate | Turn Clock | AI Hints | Tactical Profile |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Stage 1** | 🟢 **Spark (Novice)** | Depth 1 | 35% random | 20s | 5 Hints | Shallow 1-ply horizon; prone to tactical oversights; generous hints. |
| **Stage 2** | 🔵 **Circuit (Apprentice)** | Depth 2 | 15% random | 15s | 3 Hints | 2-ply search with basic positional awareness; blocks direct 3-in-a-row threats. |
| **Stage 3** | 🟡 **Vector (Tactician)** | Depth 3 | 0% | 15s | 2 Hints | Consistent 3-ply heuristic search; strong central column control. |
| **Stage 4** | 🔴 **Nexus (Grandmaster)** | Depth 4 | 0% | 12s | 1 Hint | Deep 4-ply search with Alpha-Beta pruning; tight hint allowance. |
| **Stage 5** | 🟣 **Omega (God Mode Boss)** | Depth 5 | 0% | 10s Blitz | **Disabled** | Optimal 5-ply Alpha-Beta search; hints completely disabled under severe blitz pressure. |

---

## 💾 Local Profile & Persistence System

### Schema Specification (`data/profile.json`)

User progress is persisted locally without requiring external database dependencies:

```json
{
  "player_name": "Player 1",
  "created_at": "2026-09-26T20:00:00Z",
  "highest_unlocked_level": 1,
  "level_progress": {
    "1": { "completed": true, "stars": 3, "best_time_sec": 38, "wins": 1, "losses": 0 },
    "2": { "completed": false, "stars": 0, "best_time_sec": null, "wins": 0, "losses": 1 },
    "3": { "completed": false, "stars": 0, "best_time_sec": null, "wins": 0, "losses": 0 },
    "4": { "completed": false, "stars": 0, "best_time_sec": null, "wins": 0, "losses": 0 },
    "5": { "completed": false, "stars": 0, "best_time_sec": null, "wins": 0, "losses": 0 }
  },
  "career_stats": {
    "total_matches": 2,
    "total_wins": 1,
    "total_losses": 1,
    "win_streak": 0,
    "best_win_streak": 1,
    "total_stars": 3
  }
}
```

### ⭐ Star Rating Algorithm
Upon defeating a stage's AI boss, the player is awarded between 1 and 3 stars based on their performance efficiency:

$$\text{Stars Awarded} = \begin{cases}
3 & \text{if } \text{Total Player Moves} \le 14 \text{ OR } \frac{\text{Remaining Match Time}}{\text{Initial Session Time}} \ge 0.60 \\
2 & \text{if } 15 \le \text{Total Player Moves} \le 22 \\
1 & \text{if } \text{Total Player Moves} > 22 \text{ (Victory by attrition/timeout)}
\end{cases}$$

---

## 🤖 AI Engine Mechanics

### 1. Minimax with Alpha-Beta Pruning and Blunder Injection

The engine computes the optimal column action via zero-sum game tree evaluation:

$$\text{Minimax}(s, d, \alpha, \beta) = \begin{cases}
\text{Utility}(s) & \text{if } d = 0 \text{ or terminal}(s) \\
\max_{a \in \text{Actions}(s)} \text{Minimax}(\text{Result}(s, a), d-1, \alpha, \beta) & \text{if Maximizing (AI)} \\
\min_{a \in \text{Actions}(s)} \text{Minimax}(\text{Result}(s, a), d-1, \alpha, \beta) & \text{if Minimizing (Player)}
\end{cases}$$

**Blunder Injection**:
For casual and apprentice stages, an $\epsilon$-greedy blunder policy is applied:
$$\text{Action Chosen} = \begin{cases} 
\text{Random Valid Action} & \text{with probability } \epsilon \\
\text{Best Minimax Action} & \text{with probability } 1 - \epsilon 
\end{cases}$$

### 2. Move Ordering Optimization

Alpha-Beta pruning efficiency depends heavily on child traversal order. The engine evaluates columns from the physical center outward:

$$\text{COLUMN\_ORDER} = [3, 2, 4, 1, 5, 0, 6]$$

This maximizes the likelihood of hitting high-utility scores on initial branches, driving up $\alpha$ and pruning up to $80\%$ of downstream permutations.

### 3. Sliding Window Heuristic Function

Non-terminal leaf positions at depth $d=0$ are evaluated across all horizontal, vertical, and diagonal 4-cell windows:

| Window Composition | Heuristic Value | Tactical Significance |
| :--- | :--- | :--- |
| **4 AI Discs** | `+100,000` | Immediate victory |
| **3 AI Discs + 1 Empty** | `+50` | Uncontested winning threat setup |
| **2 AI Discs + 2 Empty** | `+10` | Early-game potential structure |
| **Opponent 3 Discs + 1 Empty** | `-800` | Critical mandatory block |
| **Center Column Control** | `+6` / disc | Geometric board dominance multiplier |

---

## 🔍 Multi-Directional DFS Win Verification

`win_checker.py` performs a targeted directional **Depth-First Search** originating from the newly placed disc coordinates $(r_0, c_0)$:

$$\text{Search Axes} = \Big\{ \big((0, 1), (0, -1)\big), \big((1, 0), (-1, 0)\big), \big((1, 1), (-1, -1)\big), \big((1, -1), (-1, 1)\big) \Big\}$$

For each axis pair $(\vec{d}_1, \vec{d}_2)$:
$$\text{Streak Length} = 1 + \text{count}(\vec{d}_1) + \text{count}(\vec{d}_2)$$
If $\text{Streak Length} \ge 4$, a win is declared and the exact ordered path coordinates are dispatched to the UI for laser line rendering.
