# 🛠️ Setup & Running Guide — Connect 4 AI Laboratory

This guide provides detailed instructions to set up, configure, run, and evaluate the **Connect 4 Adversarial AI Laboratory** desktop application across **Windows**, **Linux**, and **macOS**.

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

The application relies on standard, lightweight, high-performance libraries:
- **`PyQt6`** ($\ge 6.5.0$): Powers the windowing system, level select screen, and custom `QPainter` 2D graphics canvas.
- **`numpy`** ($\ge 1.24.0$): Provides accelerated matrix operations for board state manipulation.

---

## 🚀 Step-by-Step Installation

### 1. Clone or Download the Repository

```bash
git clone https://github.com/iamabraryeasir/Connect4-AI-Project.git
cd Connect4-AI-Project
```

---

### 2. Create and Activate a Virtual Environment

Isolating dependencies inside a virtual environment prevents package conflicts.

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

With your virtual environment activated:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Verify that all dependencies are properly installed:
```bash
python -c "import PyQt6, numpy; print('PyQt6 and NumPy loaded successfully!')"
```

---

## 🎮 Launching the Application

To launch the desktop application:

```bash
python main.py
```

Upon launching, the application automatically initializes your local player account (`data/profile.json`) with Level 1 unlocked.

---

## 🧭 Navigating the Application

1. **Start Screen**:
   - Displays player evaluation profile, total stars earned, victories, and match timer settings.
   - Choose between **AI Benchmark Mode (Level Progression)** or **Two-Player Pass & Play**.
2. **Level Progression & Evaluation Select**:
   - Displays all 5 evaluation tiers from **Level 1 (Novice Agent)** to **Level 5 (Expert Agent)**.
   - Shows earned stars (★★★), high scores, and unlocked level statuses.
3. **In-Game Evaluation Interface**:
   - Features dynamic turn timers, interactive column target indicators, live search telemetry HUD, and bounded AI hint assistance.

---

## 🔍 Troubleshooting & FAQ

### 1. `ModuleNotFoundError: No module named 'PyQt6'`
- **Fix**: Ensure your virtual environment is active before running `python main.py`. If needed, run `pip install -r requirements.txt`.

### 2. Linux: `qt.qpa.plugin: Could not load the Qt platform plugin "xcb"`
- **Fix**: Install the necessary X11/XCB display packages:
  ```bash
  sudo apt update
  sudo apt install -y libxcb-xinerama0 libxcb-cursor0 libxkbcommon-x11-0 libgl1-mesa-glx
  ```

### 3. Resetting Benchmark & Evaluation Progress
- **Global Keystroke**: Press `Ctrl + Shift + R` anywhere in the application to reset all unlocked levels, stars, and match statistics back to factory defaults.
- **Manual Reset**: Alternatively, delete the `data/profile.json` file. The application will regenerate a clean profile on next startup.

---

## 🧪 Verification & Headless Testing

To test the core Minimax AI engine and profile manager without launching the GUI:

```bash
python -c "from src.ai import minimax; from src.core import game_logic; b = game_logic.create_board(); col, nodes = minimax.get_best_move(b, depth=4, blunder_rate=0.0); print(f'Best col: {col}, Nodes explored: {nodes}')"
```
