#!/usr/bin/env python3
"""
Sudoku Game Entry Point.

Optimized for desktop and Android environments (Pydroid 3, QPython, Termux).
"""

import sys
import pygame

# Force Pygame to bind to the native Android activity context immediately
pygame.init()

from src.app import SudokuApp
from src.config import KeypadPlacement, LIGHT_THEME, DARK_THEME, Difficulty


def main():
    # Ensure all subsystems are fully initialized
    if not pygame.get_init():
        pygame.init()
    if not pygame.display.get_init():
        pygame.display.init()
    if not pygame.font.get_init():
        pygame.font.init()

    # Default parameters
    placement = KeypadPlacement.AUTO
    theme = LIGHT_THEME
    width = None
    height = None
    difficulty = None

    # Safely parse optional CLI arguments if provided (ignores Android launcher args)
    if len(sys.argv) > 1 and not sys.argv[1].startswith("/data/"):
        try:
            import argparse
            parser = argparse.ArgumentParser(description="Sudoku Game with Adaptive Responsive Layout")
            parser.add_argument("--width", type=int, default=None, help="Initial window width")
            parser.add_argument("--height", type=int, default=None, help="Initial window height")
            parser.add_argument(
                "--layout",
                type=str,
                choices=["auto", "bottom", "right"],
                default="auto",
                help="Keypad placement: 'auto', 'bottom', or 'right'"
            )
            parser.add_argument(
                "--theme",
                type=str,
                choices=["light", "dark"],
                default="light",
                help="Theme: 'light' or 'dark'"
            )
            parser.add_argument(
                "--difficulty",
                type=str,
                choices=["easy", "medium", "hard", "expert"],
                default=None,
                help="Directly start difficulty"
            )
            args, _ = parser.parse_known_args()

            placement_map = {
                "auto": KeypadPlacement.AUTO,
                "bottom": KeypadPlacement.BOTTOM,
                "right": KeypadPlacement.RIGHT,
            }
            placement = placement_map.get(args.layout, KeypadPlacement.AUTO)
            theme = DARK_THEME if args.theme == "dark" else LIGHT_THEME
            width = args.width
            height = args.height

            if args.difficulty:
                diff_map = {
                    "easy": Difficulty.EASY,
                    "medium": Difficulty.MEDIUM,
                    "hard": Difficulty.HARD,
                    "expert": Difficulty.EXPERT,
                }
                difficulty = diff_map.get(args.difficulty)
        except Exception:
            pass

    app = SudokuApp(
        width=width,
        height=height,
        placement=placement,
        theme=theme
    )

    if difficulty:
        app.start_game(difficulty)

    app.run()


if __name__ == "__main__":
    main()
