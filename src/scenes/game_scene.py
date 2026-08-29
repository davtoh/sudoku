"""Main gameplay scene coordinating board, keypad, header controls, timer, and victory screen."""

import pygame
from typing import Optional, TYPE_CHECKING
from ..config import Difficulty, KeypadPlacement, Theme
from .base_scene import BaseScene
from ..core.board import Board
from ..ui.layout import LayoutMetrics, KeypadPlacement
from ..ui.board_view import BoardView
from ..ui.keypad_view import KeypadView
from ..ui.components import Button, Card, FontCache

if TYPE_CHECKING:
    from ..app import SudokuApp


class GameScene(BaseScene):
    """Coordinates active gameplay, user interaction, timer, and victory state."""

    def __init__(self, app: "SudokuApp", difficulty: Difficulty = Difficulty.MEDIUM) -> None:
        super().__init__(app)
        self.difficulty: Difficulty = difficulty
        self.board: Board = Board()
        self.board.new_game(difficulty)

        self.board_view: BoardView = BoardView()
        self.keypad_view: KeypadView = KeypadView()

        self.elapsed_time: float = 0.0
        self.is_won: bool = False
        self.is_paused: bool = False

        # Header buttons
        self.btn_menu: Optional[Button] = None
        self.btn_layout: Optional[Button] = None
        self.btn_restart: Optional[Button] = None

        # Victory modal buttons
        self.btn_win_new_game: Optional[Button] = None
        self.btn_win_menu: Optional[Button] = None

        self.metrics: LayoutMetrics = self.app.layout_manager.calculate(
            self.app.screen_width, self.app.screen_height
        )
        self._rebuild_ui()

    def _rebuild_ui(self) -> None:
        """Recalculates layout metrics and updates UI widget geometries."""
        self.metrics = self.app.layout_manager.calculate(
            self.app.screen_width, self.app.screen_height
        )
        self.keypad_view.sync_layout(self.metrics)

        # Build header buttons
        hr = self.metrics.header_rect
        btn_w = max(68, int(hr.height * 1.5))
        btn_h = int(hr.height * 0.82)
        by = hr.y + (hr.height - btn_h) // 2

        self.btn_menu = Button(
            rect=pygame.Rect(hr.x, by, btn_w, btn_h),
            label="← Menu",
            is_action=True,
            border_radius=8
        )

        self.btn_layout = Button(
            rect=pygame.Rect(hr.right - btn_w * 2 - 8, by, btn_w, btn_h),
            label="⇄ Layout",
            is_action=True,
            border_radius=8
        )

        self.btn_restart = Button(
            rect=pygame.Rect(hr.right - btn_w, by, btn_w, btn_h),
            label="↺ Reset",
            is_action=True,
            border_radius=8
        )

        # Build victory dialog buttons
        w, h = self.app.screen_width, self.app.screen_height
        dialog_w = min(360, w - 40)
        dialog_h = 240
        dialog_x = (w - dialog_w) // 2
        dialog_y = (h - dialog_h) // 2

        btn_win_w = (dialog_w - 40) // 2
        self.btn_win_new_game = Button(
            rect=pygame.Rect(dialog_x + 16, dialog_y + dialog_h - 60, btn_win_w, 44),
            label="Play Again",
            is_action=True,
            border_radius=8
        )
        self.btn_win_menu = Button(
            rect=pygame.Rect(dialog_x + 24 + btn_win_w, dialog_y + dialog_h - 60, btn_win_w, 44),
            label="Main Menu",
            is_action=False,
            border_radius=8
        )

    def on_resize(self, width: int, height: int) -> None:
        """Handles display resize."""
        self._rebuild_ui()

    def update(self, dt: float) -> None:
        """Updates timer when active and not won/paused."""
        if not self.is_won and not self.is_paused:
            self.elapsed_time += dt

    def handle_event(self, event: pygame.event.Event) -> None:
        """Processes keyboard, touch, mouse, and victory events."""
        # 1. Victory Dialog Interception
        if self.is_won:
            if self.btn_win_new_game and self.btn_win_new_game.handle_event(event):
                self.board.new_game(self.difficulty)
                self.elapsed_time = 0.0
                self.is_won = False
                return
            if self.btn_win_menu and self.btn_win_menu.handle_event(event):
                self.app.show_menu()
                return
            return

        # 2. Header Buttons
        if self.btn_menu and self.btn_menu.handle_event(event):
            self.app.show_menu()
            return

        if self.btn_layout and self.btn_layout.handle_event(event):
            # Toggle between bottom and right placement
            cur = self.metrics.placement
            new_placement = KeypadPlacement.RIGHT if cur == KeypadPlacement.BOTTOM else KeypadPlacement.BOTTOM
            self.app.layout_manager.set_placement(new_placement)
            self._rebuild_ui()
            return

        if self.btn_restart and self.btn_restart.handle_event(event):
            self.board.restart_game()
            return

        # 3. Board Selection Hit Testing
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            cell_coords = self.board_view.get_cell_at_pos(event.pos, self.metrics)
            if cell_coords:
                self.board.select(cell_coords[0], cell_coords[1])
                return

        # 4. On-Screen Keypad Interaction
        keypad_action = self.keypad_view.handle_event(event)
        if keypad_action:
            self._execute_action(keypad_action)
            self._check_victory()
            return

        # 5. Physical Keyboard Input
        if event.type == pygame.KEYDOWN:
            self._handle_key_down(event)
            self._check_victory()

    def _handle_key_down(self, event: pygame.event.Event) -> None:
        """Handles physical keyboard keypresses."""
        # Navigation
        if event.key in (pygame.K_UP, pygame.K_w):
            self.board.move_selection(-1, 0)
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.board.move_selection(1, 0)
        elif event.key in (pygame.K_LEFT, pygame.K_a):
            self.board.move_selection(0, -1)
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            self.board.move_selection(0, 1)

        # Numbers 1-9
        elif pygame.K_1 <= event.key <= pygame.K_9:
            digit = event.key - pygame.K_1 + 1
            self.board.input_number(digit)
        elif pygame.K_KP1 <= event.key <= pygame.K_KP9:
            digit = event.key - pygame.K_KP1 + 1
            self.board.input_number(digit)

        # Erase / Clear
        elif event.key in (pygame.K_0, pygame.K_KP0, pygame.K_BACKSPACE, pygame.K_DELETE):
            self.board.erase_selected()

        # Notes mode toggle (N)
        elif event.key == pygame.K_n:
            self.board.toggle_notes_mode()

        # Undo (U or Ctrl+Z / Cmd+Z)
        elif event.key == pygame.K_u or (
            event.key == pygame.K_z and (event.mod & (pygame.KMOD_CTRL | pygame.KMOD_META))
        ):
            self.board.undo()

        # Menu (Escape)
        elif event.key == pygame.K_ESCAPE:
            self.app.show_menu()

    def _execute_action(self, action_id: str) -> None:
        """Executes action triggered from keypad."""
        if action_id.isdigit():
            digit = int(action_id)
            self.board.input_number(digit)
        elif action_id == "erase":
            self.board.erase_selected()
        elif action_id == "notes":
            self.board.toggle_notes_mode()
        elif action_id == "undo":
            self.board.undo()
        elif action_id == "clear":
            self.board.restart_game()

    def _check_victory(self) -> None:
        """Checks if the player has successfully solved the puzzle."""
        if self.board.is_solved():
            self.is_won = True

    def render(self, surface: pygame.Surface) -> None:
        """Renders the game scene, header, board, keypad, and overlays."""
        theme = self.app.theme
        surface.fill(theme.bg_primary)

        # 1. Header (Menu button, Timer, Difficulty, Layout button, Restart)
        self._render_header(surface, theme)

        # 2. Board
        self.board_view.render(surface, self.board, self.metrics, theme)

        # 3. Keypad
        self.keypad_view.render(surface, self.board, self.metrics, theme)

        # 4. Victory Overlay
        if self.is_won:
            self._render_victory_overlay(surface, theme)

    def _render_header(self, surface: pygame.Surface, theme: Theme) -> None:
        """Renders toolbar with buttons, difficulty badge, and timer."""
        hr = self.metrics.header_rect

        # Render Header Buttons
        if self.btn_menu:
            self.btn_menu.render(surface, theme, font_size=self.metrics.font_size_small)
        if self.btn_layout:
            self.btn_layout.render(surface, theme, font_size=self.metrics.font_size_small)
        if self.btn_restart:
            self.btn_restart.render(surface, theme, font_size=self.metrics.font_size_small)

        # Timer & Difficulty in center
        total_seconds = int(self.elapsed_time)
        mins = total_seconds // 60
        secs = total_seconds % 60
        time_str = f"{mins:02d}:{secs:02d}"

        time_font = FontCache.get_font(self.metrics.font_size_header, bold=True)
        time_surf = time_font.render(time_str, True, theme.text_primary)
        time_rect = time_surf.get_rect(center=(hr.centerx, hr.centery - 8))
        surface.blit(time_surf, time_rect)

        diff_font = FontCache.get_font(self.metrics.font_size_small)
        diff_surf = diff_font.render(self.difficulty.value, True, theme.text_secondary)
        diff_rect = diff_surf.get_rect(center=(hr.centerx, hr.centery + 12))
        surface.blit(diff_surf, diff_rect)

    def _render_victory_overlay(self, surface: pygame.Surface, theme: Theme) -> None:
        """Draws semi-transparent overlay and win dialog card."""
        w, h = self.app.screen_width, self.app.screen_height

        # Darkened backdrop
        backdrop = pygame.Surface((w, h), pygame.SRCALPHA)
        backdrop.fill((0, 0, 0, 140))
        surface.blit(backdrop, (0, 0))

        # Card container
        dialog_w = min(360, w - 40)
        dialog_h = 220
        dialog_x = (w - dialog_w) // 2
        dialog_y = (h - dialog_h) // 2
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_w, dialog_h)

        Card.draw(
            surface, dialog_rect,
            bg_color=theme.bg_card,
            border_color=theme.text_accent,
            border_radius=16,
            border_width=2
        )

        # Victory Title
        title_font = FontCache.get_font(30, bold=True)
        title_surf = title_font.render("Puzzle Solved!", True, theme.cell_user)
        title_rect = title_surf.get_rect(center=(dialog_rect.centerx, dialog_rect.y + 42))
        surface.blit(title_surf, title_rect)

        # Time & Difficulty stats
        total_seconds = int(self.elapsed_time)
        mins = total_seconds // 60
        secs = total_seconds % 60
        stats_str = f"Difficulty: {self.difficulty.value}  •  Time: {mins:02d}:{secs:02d}"
        stats_font = FontCache.get_font(18)
        stats_surf = stats_font.render(stats_str, True, theme.text_secondary)
        stats_rect = stats_surf.get_rect(center=(dialog_rect.centerx, dialog_rect.y + 90))
        surface.blit(stats_surf, stats_rect)

        # Buttons
        if self.btn_win_new_game:
            self.btn_win_new_game.render(surface, theme, font_size=16)
        if self.btn_win_menu:
            self.btn_win_menu.render(surface, theme, font_size=16)

