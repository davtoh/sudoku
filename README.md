# Sudoku Game

A modern, object-oriented Sudoku game built with Python and Pygame. Designed for responsive gameplay across mobile phones (e.g. Android with Pydroid 3 or QPython), tablets, and desktop computers.

---

## Key Features

- **Adaptive Responsive Layout (`LayoutManager`)**:
  - Automatically calculates optimal board and keypad geometries to fit any screen size or aspect ratio.
  - **Portrait Mode**: Positions the keypad **below (down)** the board for comfortable one-handed mobile play.
  - **Landscape Mode**: Positions the keypad to the **right** of the board for widescreen and desktop layouts.
  - Live window resizing and screen rotation support (`pygame.VIDEORESIZE`).
- **Object-Oriented Modular Architecture**:
  - Clean separation of concerns between core models (`Cell`, `Board`, `SudokuGenerator`), UI presentation (`BoardView`, `KeypadView`, `Button`), and scene lifecycle management.
- **Rich Gameplay Features**:
  - **4 Difficulty Levels**: Easy (49 clues), Medium (39 clues), Hard (31 clues), and Expert (25 clues).
  - **Pencil Marks / Notes Mode**: Toggle notes to draft candidate numbers in a mini 3x3 subgrid within each cell.
  - **Conflict Highlighting**: Instantly detects duplicate numbers in rows, columns, and 3x3 blocks.
  - **Undo History**: Revert moves and note changes with full state preservation.
  - **Dual Input Support**: Play via touch/mouse or physical keyboard shortcuts.
  - **Theme Support**: Includes both Light and Dark themes.

---

## Project Structure

```
sudoku/
├── sudoku.py                     # Runnable entry point (supports CLI flags)
├── requirements.txt              # Dependencies (pygame, numpy, etc.)
├── README.md                     # Documentation
├── src/
│   ├── __init__.py
│   ├── app.py                   # SudokuApp game runner & scene orchestrator
│   ├── config.py                # Themes, difficulty settings, and layout placement enums
│   ├── core/
│   │   ├── __init__.py
│   │   ├── cell.py              # Cell model (values, given state, notes, validity)
│   │   ├── board.py             # Board model (grid operations, undo stack, win check)
│   │   └── generator.py         # Sudoku puzzle generator and solver
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── layout.py            # Responsive LayoutManager (bottom vs right placement)
│   │   ├── components.py        # UI widgets (Button, Card, FontCache)
│   │   ├── board_view.py        # 9x9 grid, selection, notes, and conflict rendering
│   │   └── keypad_view.py       # Adaptive numeric keypad and action buttons
│   └── scenes/
│       ├── __init__.py
│       ├── base_scene.py        # Abstract Scene lifecycle interface
│       ├── menu_scene.py        # Difficulty selection and configuration menu
│       └── game_scene.py        # Gameplay scene with toolbar, timer, and victory dialog
└── tests/
    ├── test_generator.py        # Generator and solver tests
    ├── test_board.py            # Board and cell domain logic tests
    └── test_layout.py           # LayoutManager geometry and placement tests
```

---

## How to Run

### 1. Setup Environment
```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Launch Game
```bash
python sudoku.py
```

### 3. CLI Options
You can customize the layout, window size, or starting difficulty directly from the command line:

```bash
# Force keypad to the right (landscape mode)
python sudoku.py --layout right

# Force keypad below the board (portrait mode)
python sudoku.py --layout bottom

# Launch with dark theme
python sudoku.py --theme dark

# Launch with custom window size
python sudoku.py --width 800 --height 600

# Directly launch hard difficulty
python sudoku.py --difficulty hard
```

---

## Controls

### Mouse / Touch
- **Tap any cell** to select.
- **Tap keypad numbers (1-9)** to enter digit or note.
- **Tap Notes button** to toggle pencil marks mode.
- **Tap Erase button** to clear selected cell.
- **Tap Undo button** to undo last action.
- **Tap Layout button (⇄ Layout)** to switch keypad between Bottom and Right on the fly.

### Keyboard Shortcuts
| Key | Action |
|---|---|
| `1` - `9` | Place number (or note if Notes mode is active) |
| `Backspace` / `Delete` / `0` | Erase cell value and notes |
| `N` | Toggle pencil notes mode |
| `U` or `Ctrl+Z` / `Cmd+Z` | Undo last move |
| `Arrow Keys` / `WASD` | Navigate selection across the grid |
| `R` | Restart current puzzle |
| `Escape` | Return to Main Menu |

---

## Running Tests

Execute all automated unit tests:
```bash
python -m unittest discover tests/
```
