#!/usr/bin/env python3
"""
Sudoku Game Entry Point.

Run directly on desktop or Android (Pydroid / QPython / Pygame-compatible mobile runners):
    python sudoku.py

Optional CLI flags:
    python sudoku.py --layout right
    python sudoku.py --layout bottom
    python sudoku.py --theme dark
    python sudoku.py --width 800 --height 600
"""

import sys
import argparse
from src.app import SudokuApp
from src.config import KeypadPlacement, LIGHT_THEME, DARK_THEME, Difficulty


def parse_args():
    parser = argparse.ArgumentParser(description="Sudoku Game with Adaptive Responsive Layout")
    parser.add_argument(
        "--width", type=int, default=None, help="Initial window width in pixels"
    )
    parser.add_argument(
        "--height", type=int, default=None, help="Initial window height in pixels"
    )
    parser.add_argument(
        "--layout",
        type=str,
        choices=["auto", "bottom", "right"],
        default="auto",
        help="Keypad placement mode: 'auto' (aspect-ratio adaptive), 'bottom' (down), or 'right' (side)",
    )
    parser.add_argument(
        "--theme",
        type=str,
        choices=["light", "dark"],
        default="light",
        help="Visual theme ('light' or 'dark')",
    )
    parser.add_argument(
        "--difficulty",
        type=str,
        choices=["easy", "medium", "hard", "expert"],
        default=None,
        help="Skip menu and directly start with given difficulty",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    placement_map = {
        "auto": KeypadPlacement.AUTO,
        "bottom": KeypadPlacement.BOTTOM,
        "right": KeypadPlacement.RIGHT,
    }
    placement = placement_map.get(args.layout, KeypadPlacement.AUTO)
    theme = DARK_THEME if args.theme == "dark" else LIGHT_THEME

    app = SudokuApp(
        width=args.width,
        height=args.height,
        placement=placement,
        theme=theme
    )

    if args.difficulty:
        diff_map = {
            "easy": Difficulty.EASY,
            "medium": Difficulty.MEDIUM,
            "hard": Difficulty.HARD,
            "expert": Difficulty.EXPERT,
        }
        app.start_game(diff_map[args.difficulty])

    app.run()


if __name__ == "__main__":
    main()
