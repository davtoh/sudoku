"""Main application runner managing Pygame display, event loop, and scenes."""

import sys
import pygame
from typing import Optional
from .config import Theme, LIGHT_THEME, DARK_THEME, KeypadPlacement, Difficulty, FPS
from .ui.layout import LayoutManager
from .scenes.base_scene import BaseScene
from .scenes.menu_scene import MenuScene
from .scenes.game_scene import GameScene


class SudokuApp:
    """Core Sudoku game application orchestrator."""

    def __init__(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        placement: KeypadPlacement = KeypadPlacement.AUTO,
        theme: Theme = LIGHT_THEME
    ) -> None:
        pygame.init()
        pygame.font.init()

        # Determine initial window resolution
        info = pygame.display.Info()
        detected_w = info.current_w
        detected_h = info.current_h

        # Default to portrait friendly size on desktop if detection yields huge resolution
        if width and height:
            self.screen_width = width
            self.screen_height = height
        elif detected_w > 1200 and detected_h > 800:
            # Desktop window mode default
            self.screen_width = 460
            self.screen_height = 780
        else:
            # Mobile or small screen
            self.screen_width = detected_w
            self.screen_height = detected_h

        self.screen: pygame.Surface = pygame.display.set_mode(
            (self.screen_width, self.screen_height), pygame.RESIZABLE
        )
        pygame.display.set_caption("Sudoku")

        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.theme: Theme = theme
        self.layout_manager: LayoutManager = LayoutManager(placement=placement)

        self.is_running: bool = False
        self.current_scene: Optional[BaseScene] = None

    def start_game(self, difficulty: Difficulty = Difficulty.MEDIUM) -> None:
        """Transitions to active gameplay scene."""
        self.current_scene = GameScene(self, difficulty=difficulty)

    def show_menu(self) -> None:
        """Transitions to the main menu scene."""
        self.current_scene = MenuScene(self)

    def toggle_theme(self) -> None:
        """Switches between Light and Dark themes."""
        self.theme = DARK_THEME if self.theme.name == "light" else LIGHT_THEME

    def handle_resize(self, new_w: int, new_h: int) -> None:
        """Handles screen resolution change (window resize or device rotation)."""
        self.screen_width = max(300, new_w)
        self.screen_height = max(400, new_h)
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height), pygame.RESIZABLE
        )
        if self.current_scene:
            self.current_scene.on_resize(self.screen_width, self.screen_height)

    def run(self) -> None:
        """Main game loop."""
        self.is_running = True
        self.show_menu()

        while self.is_running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    break

                elif event.type == pygame.VIDEORESIZE:
                    self.handle_resize(event.w, event.h)

                elif self.current_scene:
                    self.current_scene.handle_event(event)

            if not self.is_running:
                break

            if self.current_scene:
                self.current_scene.update(dt)
                self.current_scene.render(self.screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

