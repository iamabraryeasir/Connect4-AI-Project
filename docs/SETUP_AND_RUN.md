# 🛠️ Setup & Running Guide — Connect 4 AI

This guide provides detailed instructions to set up, configure, run, and troubleshoot the **Connect 4 AI** desktop application across **Windows**, **Linux**, and **macOS**.

---

## 📋 System Requirements

| Component | Minimum Specification | Recommended |
| :--- | :--- | :--- |
| **Operating System** | Windows 10/11, macOS 12+, Ubuntu 20.04+ | Latest 64-bit OS |
| **Python** | Python 3.10 | Python 3.11 or 3.12 |
| **RAM** | 2 GB | 4 GB+ |
| **Display** | 1024 × 768 resolution | 1920 × 1080 (Full HD) |

---

## 📦 Dependencies

The application relies on lightweight, high-performance libraries:
- **`PyQt6`** ($\ge 6.5.0$): Powers the GUI, windowing system, and custom `QPainter` 2D graphics.
- **`numpy`** ($\ge 1.24.0$): Provides accelerated matrix operations for board state representations.

---

## 🚀 Step-by-Step Installation

### 1. Clone or Download the Repository

```bash
git clone https://github.com/iamabraryeasir/Connect4-AI-Project.git
cd Connect4-AI-Project
```

---

### 2. Create and Activate a Virtual Environment

Isolating dependencies inside a virtual environment prevents version conflicts with other Python projects.

#### 🪟 Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

> **Note for PowerShell Execution Policy**: If you encounter a `Script Execution is disabled` error, run:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

#### 🪟 Windows (Command Prompt)
```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

#### 🐧 Linux / 🍎 macOS (Bash / Zsh)
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Install Required Packages

With your virtual environment activated, install the required packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

To verify the installation:
```bash
python -c "import PyQt6, numpy; print('PyQt6 and NumPy installed successfully!')"
```

---

## 🎮 Launching the Game

To start the desktop application:

```bash
python main.py
```

---

## 🛠️ Configuration Options

When the game launcher displays:

1. **Game Mode Selection**:
   - `Player vs AI`: Single-player tactical challenge against the Minimax engine.
   - `Player vs Player (PvP)`: Pass-and-play local multiplayer on the same machine.
2. **Match Duration**:
   - `3 Minutes`: Rapid blitz match.
   - `5 Minutes`: Standard tournament game.
   - `10 Minutes`: Extended strategic battle.

Click **START MATCH** to begin!

---

## 🔍 Troubleshooting & FAQ

### 1. `ModuleNotFoundError: No module named 'PyQt6'`
- **Cause**: The virtual environment is either not activated or dependencies were installed to a different Python environment.
- **Fix**: Re-activate your virtual environment and run `pip install -r requirements.txt`.

### 2. Linux: `qt.qpa.plugin: Could not load the Qt platform plugin "xcb"`
- **Cause**: Missing X11/XCB display libraries on Debian/Ubuntu systems.
- **Fix**: Run:
  ```bash
  sudo apt update
  sudo apt install -y libxcb-xinerama0 libxcb-cursor0 libxkbcommon-x11-0 libgl1-mesa-glx
  ```

### 3. High DPI / Display Scaling Issues on Windows
- PyQt6 automatically manages DPI scaling. If UI elements appear too small or oversized, set the Qt scaling environment variable before running:
  ```powershell
  $env:QT_AUTO_SCREEN_SCALE_FACTOR="1"
  python main.py
  ```

---

## 🧪 Verification & Development

To test the core AI and state manager without launching the GUI:

```bash
python -c "from src.ai import minimax; from src.core import game_logic; b = game_logic.create_board(); col, nodes = minimax.get_best_move(b, depth=4); print(f'Best col: {col}, Nodes explored: {nodes}')"
```

