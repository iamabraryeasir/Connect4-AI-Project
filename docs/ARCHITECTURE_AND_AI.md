# 🧠 Technical Architecture & AI Engine Specification

This document details the mathematical modeling, algorithmic designs, data structures, and state management architecture of the **Connect 4 AI Project**.

---

## 🏗️ Architectural Topology

The project follows a decoupled layered architecture ensuring clean boundaries between mathematical game state, AI search routines, and graphics rendering:

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                       │
│      AppController (QStackedWidget) ──► GameWindow          │
│                      │                                      │
│                      ▼                                      │
│             board_renderer (QPainter)                       │
└──────────────────────────────┬──────────────────────────────┘
                               │ Reads State & Paints
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                      State Manager                          │
│               src.state.game_state                          │
│     (Immutable-style Dict, Clocks, Bonus Turns, Dispatch)   │
└──────────────┬──────────────────────────────┬───────────────┘
               │                              │
               ▼                              ▼
┌──────────────────────────────┐ ┌────────────────────────────┐
│         AI Engine            │ │        Core Logic          │
│   src.ai.minimax             │ │    src.core.game_logic     │
│   - Alpha-Beta Pruning       │ │    - 6x7 NumPy Matrix      │
│   - Move Ordering [3,2,4...] │ │    - Drop mechanics        │
│   - Heuristic Window Scorer  │ │    - Grid boundary checks  │
│   src.ai.win_checker         │ │                            │
│   - Directional DFS          │ │                            │
└──────────────────────────────┘ └────────────────────────────┘
```

---

## 🤖 1. Minimax Algorithm with Alpha-Beta Pruning

The AI models Connect 4 as a two-player, zero-sum game of perfect information.

### Mathematical Formulation

Let $s$ be the board state, $d$ be the remaining depth limit ($d = 5$), and $\text{Actions}(s)$ be the set of valid column choices:

$$\text{Minimax}(s, d, \alpha, \beta) = \begin{cases}
\text{Utility}(s) & \text{if } d = 0 \text{ or terminal}(s) \\
\max_{a \in \text{Actions}(s)} \text{Minimax}(\text{Result}(s, a), d-1, \alpha, \beta) & \text{if Maximizing (AI)} \\
\min_{a \in \text{Actions}(s)} \text{Minimax}(\text{Result}(s, a), d-1, \alpha, \beta) & \text{if Minimizing (Player)}
\end{cases}$$

### Alpha-Beta Pruning Cutoff Criteria
- **$\alpha$**: Lower bound on the utility guaranteed to the Maximizer.
- **$\beta$**: Upper bound on the utility guaranteed to the Minimizer.
- Whenever $\alpha \ge \beta$ at any node, exploring subsequent siblings cannot influence the root decision, triggering an immediate **branch cutoff**.

---

## ⚡ 2. Center-Outward Move Ordering

Because alpha-beta efficiency is heavily dependent on branch traversal order, columns are visited starting from the center outward:

$$\text{COLUMN\_ORDER} = [3, 2, 4, 1, 5, 0, 6]$$

**Rationale**: Center columns offer the greatest number of winning 4-cell combinations across horizontal and diagonal vectors. By evaluating the central column first, high utility scores are discovered rapidly, driving up $\alpha$ early and pruning up to $80\%$ of subtrees compared to random ordering.

---

## 🎯 3. Sliding Window Heuristic Function

When depth $d = 0$ is reached on a non-terminal leaf node, the board is evaluated using a 4-cell sliding window across all rows, columns, and diagonal lines:

| Window Composition | Heuristic Value | Tactical Significance |
| :--- | :--- | :--- |
| **4 AI Discs** | `+100,000` | Immediate victory |
| **3 AI Discs + 1 Empty** | `+50` | Uncontested winning threat setup |
| **2 AI Discs + 2 Empty** | `+10` | Early-game potential building |
| **Opponent 3 Discs + 1 Empty** | `-800` | Critical defensive block required |
| **Center Column Control** | `+6` / disc | Geometric board dominance multiplier |

---

## 🔍 4. Multi-Directional DFS Win Verification

Rather than performing a costly brute-force scan of all 42 board cells after each turn, `win_checker.py` performs a targeted directional **Depth-First Search** originating strictly from the coordinates of the last dropped piece $(r_0, c_0)$:

$$\text{Search Axes} = \Big\{ \big((0, 1), (0, -1)\big), \big((1, 0), (-1, 0)\big), \big((1, 1), (-1, -1)\big), \big((1, -1), (-1, 1)\big) \Big\}$$

For each axis pair $(\vec{d}_1, \vec{d}_2)$:
1. `dfs_directional` recursively counts identical consecutive discs along direction $\vec{d}_1$.
2. `dfs_directional` recursively counts identical consecutive discs along opposite direction $\vec{d}_2$.
3. Total contiguous line length:
   $$\text{Length} = 1 + \text{count}(\vec{d}_1) + \text{count}(\vec{d}_2)$$
4. If $\text{Length} \ge 4$, the function returns `True` alongside the exact ordered coordinates of the winning four-in-a-row.

