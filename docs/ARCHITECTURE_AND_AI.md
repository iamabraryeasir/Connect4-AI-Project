# 🧠 Technical Architecture & AI Engine Specification

This document details the mathematical modeling, algorithmic designs, data structures, state management architecture, and local profile persistence of the **Connect 4 Adversarial AI Laboratory**.

---

## 🏗️ Architectural Topology

The project follows a decoupled layered architecture ensuring clean boundaries between mathematical game state, AI search routines, profile persistence, and graphics rendering:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            Presentation Layer                               │
│  AppController (QStackedWidget)                                             │
│  ├── StartScreen (Profile banner, Mode Selection)                           │
│  ├── LevelSelectScreen (Benchmark Roadmap, Stars, Agent Cards, Unlocks)     │
│  └── GameWindow (HUD, Clocks, Discs, Win Vector, Dynamic Overlays)          │
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
│  - Parameterized Depth │ │  - profile.json CRUD   │ │ - 6x7 NumPy Matrix   │
│  - Stochastic Variance │ │  - Star Calculation    │ │ - Drop mechanics     │
│  - Alpha-Beta Pruning  │ │  src.levels.config     │ │ - Boundary checks    │
│  - Heuristic Scorer    │ │  - 5-Tier Agent Specs  │ │                      │
│  src.ai.win_checker    │ │                        │ │                      │
│  - Directional DFS     │ │                        │ │                      │
└────────────────────────┘ └────────────────────────┘ └──────────────────────┘
```

---

## 🗺️ 5-Tier AI Difficulty & Evaluation Model

The benchmark features a 5-tier progressive difficulty curve designed to evaluate heuristic search performance from baseline approximations to deep lookahead.

| Level | Agent Designation | Search Depth | Stochastic Rate | Turn Clock | AI Hints | Algorithmic Profile |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Level 1** | 🟢 **Novice Agent** | Depth 1 | 35% random | 20s | 5 Hints | Baseline 1-ply heuristic evaluation with intentional stochastic variance. |
| **Level 2** | 🔵 **Apprentice Agent** | Depth 2 | 15% random | 15s | 3 Hints | 2-ply lookahead evaluating direct opponent responses and blocking obvious lines. |
| **Level 3** | 🟡 **Tactical Agent** | Depth 3 | 0% | 15s | 2 Hints | Deterministic 3-ply heuristic search incorporating center column dominance. |
| **Level 4** | 🔴 **Advanced Agent** | Depth 4 | 0% | 12s | 1 Hint | Deep 4-ply minimax with aggressive alpha-beta pruning and multi-step positioning. |
| **Level 5** | 🟣 **Expert Agent** | Depth 5 | 0% | 10s Blitz | **Disabled** | Optimal 5-ply Alpha-Beta search exploring thousands of board states under strict time limits. |

---

## 💾 Local Profile & Persistence System

### Schema Specification (`data/profile.json`)

User progress and evaluation records are persisted locally in lightweight JSON format:

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

### ⭐ Performance Star Rating Algorithm
Upon defeating an AI tier, the player receives a performance score between 1 and 3 stars:

$$\text{Stars Awarded} = \begin{cases}
3 & \text{if } \text{Total Moves} \le 14 \text{ OR } \frac{\text{Remaining Match Time}}{\text{Initial Session Time}} \ge 0.60 \\
2 & \text{if } 15 \le \text{Total Moves} \le 22 \\
1 & \text{if } \text{Total Moves} > 22 \text{ (Victory by prolonged play or timeout)}
\end{cases}$$

---

## 🤖 AI Engine Mechanics

### 1. Minimax Algorithm with Alpha-Beta Pruning

The AI models Connect 4 as a two-player, zero-sum game of perfect information:

$$\text{Minimax}(s, d, \alpha, \beta) = \begin{cases}
\text{Utility}(s) & \text{if } d = 0 \text{ or terminal}(s) \\
\max_{a \in \text{Actions}(s)} \text{Minimax}(\text{Result}(s, a), d-1, \alpha, \beta) & \text{if Maximizing (AI)} \\
\min_{a \in \text{Actions}(s)} \text{Minimax}(\text{Result}(s, a), d-1, \alpha, \beta) & \text{if Minimizing (Player)}
\end{cases}$$

**Alpha-Beta Pruning**:
- $\alpha$: Lower bound on utility guaranteed to the Maximizer.
- $\beta$: Upper bound on utility guaranteed to the Minimizer.
- Whenever $\alpha \ge \beta$ at any node, exploring remaining siblings cannot alter the root decision, triggering an immediate cutoff.

**Stochastic Variance Injection**:
For baseline and introductory tiers, an $\epsilon$-greedy policy injects variability:
$$\text{Action Chosen} = \begin{cases} 
\text{Random Legal Action} & \text{with probability } \epsilon \\
\text{Optimal Minimax Action} & \text{with probability } 1 - \epsilon 
\end{cases}$$

### 2. Move Ordering Optimization

Child branches are explored starting from the physical center outward:

$$\text{COLUMN\_ORDER} = [3, 2, 4, 1, 5, 0, 6]$$

Evaluating column 3 first yields high utility scores early, allowing alpha-beta pruning to cut off up to $80\%$ of downstream tree permutations.

### 3. Sliding Window Heuristic Function

Leaf evaluations at depth $d=0$ score the grid using a 4-cell sliding window across horizontal, vertical, and diagonal lines:

| Window Composition | Heuristic Weight | Strategic Objective |
| :--- | :---: | :--- |
| **4 AI Discs** | `+100,000` | Terminal victory |
| **Opponent 3 Discs + 1 Empty** | `-800` | Critical defensive block required |
| **AI 3 Discs + 1 Empty** | `+50` | High-priority offensive setup |
| **AI 2 Discs + 2 Empty** | `+10` | Early-game structural building |
| **Center Column Control** | `+6` / disc | Board center dominance multiplier |

---

## 🔍 Multi-Directional DFS Win Verification

`win_checker.py` executes a targeted directional **Depth-First Search** originating from the coordinates of the newly placed disc $(r_0, c_0)$:

$$\text{Search Axes} = \Big\{ \big((0, 1), (0, -1)\big), \big((1, 0), (-1, 0)\big), \big((1, 1), (-1, -1)\big), \big((1, -1), (-1, 1)\big) \Big\}$$

For each axis pair $(\vec{d}_1, \vec{d}_2)$:
$$\text{Streak Length} = 1 + \text{count}(\vec{d}_1) + \text{count}(\vec{d}_2)$$
If $\text{Streak Length} \ge 4$, a win state is returned with the exact ordered path coordinates for UI rendering.
