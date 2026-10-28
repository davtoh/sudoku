# Sudoku Flutter

A modern, accessible, and responsive Sudoku game built with Flutter. Migrated and enhanced from the original Python (Pygame) implementation, featuring Material 3 theming, full desktop & web keyboard navigation, screen reader accessibility (AX), haptic feedback, background puzzle generation, and local persistence.

---

## Features

- **Adaptive Responsive Layout (`AdaptiveSudokuLayout`)**:
  - **Portrait Mode**: Board on top, keypad below within comfortable thumb reach.
  - **Landscape Mode**: Side-by-side view (Board on left, Controls and Keypad on right).
  - **Desktop & Large Displays**: Centered layout with constrained maximum width to preserve optimal geometry.
  - **Keypad Placement Control**: Choose between Auto (Adaptive), Bottom, or Side keypad placement in settings.
- **Accessibility & Experience (AX)**:
  - **Screen Reader Support**: Complete semantic labels on every cell (e.g., *"Row 3, Column 5: 7, given"*, *"Empty cell, notes: 1, 4"*).
  - **Haptic Feedback**: Tactile feedback on mobile devices for cell taps, pencil notes, errors, and game completion.
  - **Full Hardware Keyboard Controls**: Seamless navigation and input on macOS, Windows, Linux, Web, and iPads with external keyboards.
- **4 Beautiful Themes (Material 3 `ThemeExtension`)**:
  - **Light Theme**: Crisp slate and royal blue palette.
  - **Dark Theme**: Deep charcoal and soft indigo for low-light gameplay.
  - **Warm Sepia**: Book paper tone designed for night reading comfort.
  - **OLED Pitch Black**: Pure `#000000` with high-contrast accents for AMOLED battery savings.
- **Rich Gameplay Mechanics**:
  - **4 Difficulty Levels**: Easy (49 clues), Medium (39 clues), Hard (31 clues), and Expert (25 clues).
  - **Remaining Count Badges**: Keypad digits show remaining numbers needed (1–9) and turn into checkmarks when complete.
  - **Auto-Clear Peer Notes**: Automatically removes placed digits from pencil candidate notes in the same row, column, and 3x3 box.
  - **Auto-Fill All Candidates**: One-tap tool to fill all valid pencil marks for advanced deduction.
  - **Intelligent Hint System**: Reveals next logical cell solution when requested.
  - **Undo & Redo**: Full bidirectional move and note history stack.
  - **Anti-Cheat Pause Blur**: Frosted-glass backdrop filter obscures the board while paused to preserve fair timing.
  - **Local Persistence & Stats**: Automatically saves active game state and tracks best times and total wins per difficulty via `shared_preferences`.
  - **Smooth Performance**: Backtracking puzzle generation runs in a background Dart isolate (`compute()`), keeping the UI at 60/120 FPS.

---

## Project Structure

```text
sudoku_flutter/
├── lib/
│   ├── main.dart                                # Application entry point
│   ├── core/
│   │   ├── theme/
│   │   │   ├── app_theme.dart                   # Light, Dark, Sepia, OLED themes & SudokuThemeColors
│   │   │   └── theme_view_model.dart            # Theme state management & persistence
│   │   └── utils/
│   │       └── haptic_util.dart                 # Cross-platform haptic feedback helper
│   ├── data/
│   │   └── storage/
│   │       └── game_storage.dart                # Local persistence (active game, stats, settings)
│   ├── domain/
│   │   ├── models/
│   │   │   ├── cell.dart                        # Cell model (value, solution, notes, accessibility)
│   │   │   ├── board.dart                       # 9x9 grid, undo/redo, conflict validation
│   │   │   ├── move_record.dart                 # Move history representation
│   │   │   └── difficulty.dart                  # Difficulty levels and clue counts
│   │   └── services/
│   │       └── sudoku_generator.dart            # Backtracking solver, generator & candidate calculator
│   └── ui/
│       ├── features/
│       │   ├── game/
│       │   │   ├── game_screen.dart             # Game screen coordinator
│       │   │   ├── view_models/
│       │   │   │   └── game_view_model.dart     # Game state, timer, move orchestration
│       │   │   └── widgets/
│       │   │       ├── cell_widget.dart         # Cell rendering with notes & highlights
│       │   │       ├── sudoku_board_widget.dart # 9x9 board with 3x3 subgrids & pause blur
│       │   │       ├── adaptive_keypad_widget.dart # 1-9 keypad with badges & actions
│       │   │       ├── game_header_widget.dart  # Header toolbar, timer, restart, settings
│       │   │       ├── victory_dialog.dart      # Game completion dialog with stats
│       │   │       └── keyboard_listener_wrapper.dart # Keyboard shortcut listener
│       │   ├── menu/
│       │   │   └── menu_screen.dart             # Difficulty selection, resume, stats
│       │   └── settings/
│       │       └── settings_screen.dart         # Theme, layout, and helper preferences
│       └── responsive/
│           └── adaptive_sudoku_layout.dart      # Breakpoint-driven layout switcher
└── test/
    ├── sudoku_core_test.dart                    # Domain logic & generator unit tests
    └── widget_test.dart                         # Widget smoke tests
```

---

## Getting Started

### Prerequisites

- [Flutter SDK](https://docs.flutter.dev/get-started/install) (3.13+ or higher)
- macOS, Windows, Linux, iOS/Android toolchains, or Google Chrome for web.

### Installation

1. Navigate to the `sudoku_flutter` directory:
   ```bash
   cd sudoku_flutter
   ```

2. Fetch all dependencies:
   ```bash
   flutter pub get
   ```

---

## Running the Application

### Automatic Device Selection
```bash
flutter run
```

### Run on Specific Targets

- **macOS Desktop**:
  ```bash
  flutter run -d macos
  ```
- **Web (Chrome)**:
  ```bash
  flutter run -d chrome
  ```
- **Android**:
  ```bash
  flutter run -d android
  ```
- **iOS Simulator / Device**:
  ```bash
  flutter run -d ios
  ```
- **Windows Desktop**:
  ```bash
  flutter run -d windows
  ```
- **Linux Desktop**:
  ```bash
  flutter run -d linux
  ```

---

## Running Tests & Static Analysis

### 1. Static Analysis
Run Flutter's analyzer to verify there are zero errors or lint warnings:
```bash
flutter analyze
```

### 2. Unit and Widget Tests
Execute the full test suite:
```bash
flutter test
```

### Test Coverage Highlights:
- **`Cell Model Tests`**: Value changes, notes toggle, clear operations, and immutability of given clues.
- **`SudokuGenerator Tests`**: Full 9x9 board validity (rows, columns, and 3x3 blocks having unique 1–9 digits) and puzzle generation uniqueness (`countSolutions == 1`).
- **`Board Domain Tests`**: Input handling, conflict validation for duplicate digits, full bidirectional undo/redo, and win detection.
- **`Widget Smoke Tests`**: `SudokuApp` initialization, menu rendering, and difficulty options.

---

## Controls

### Mouse / Touch
- **Tap Cell**: Select a cell.
- **Keypad 1–9**: Place a number into the selected cell (or toggle candidate note in Notes mode).
- **Notes Button**: Toggle pencil marks mode on/off.
- **Erase**: Clear user value or notes from the selected cell.
- **Undo / Redo**: Step backward or forward through move history.
- **Hint**: Reveal the solution for the selected or next unresolved cell.
- **Auto**: Automatically calculate candidate pencil marks for all empty cells.
- **Timer / Pause**: Tap the timer to pause gameplay and blur the board.

### Hardware Keyboard Shortcuts
| Shortcut | Action |
| :--- | :--- |
| `Arrow Keys` or `W`, `A`, `S`, `D` | Move board selection (with boundary wrap-around) |
| `1` – `9` | Place digit / toggle note |
| `Backspace`, `Delete`, `0` | Erase selected cell |
| `N` | Toggle Notes mode |
| `U` or `Ctrl + Z` / `Cmd + Z` | Undo last move |
| `H` | Apply hint |
| `Space` | Pause / Resume timer |

---

## Migration Relationship

This Flutter application is built based on the core algorithms of the root Python implementation:
- The Python implementation remains intact and runnable in the parent directory (`../sudoku.py`).
- Detailed architecture comparisons, enhancement records, and technical mappings can be found in [MIGRATION_LOG.md](../MIGRATION_LOG.md).
