"""Main gameplay scene coordinating board, keypad, header controls, timer, move mode, and victory screen."""

import pygame
from typing import Optional, Tuple, TYPE_CHECKING
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
    """Coordinates active gameplay, interactive element repositioning, timer, and victory state."""

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

        # Move/Repositioning mode state
        self.is_move_mode: bool = False
        self.selected_move_group: str = "board"  # "board" or "keypad"
        self.is_dragging: bool = False
        self.drag_target: Optional[str] = None
        self.drag_start_pos: Optional[Tuple[int, int]] = None

        # Header buttons
        self.btn_menu: Optional[Button] = None
        self.btn_layout: Optional[Button] = None
        self.btn_move: Optional[Button] = None
        self.btn_restart: Optional[Button] = None

        # Move mode toolbar buttons
        self.btn_move_target: Optional[Button] = None
        self.btn_nudge_up: Optional[Button] = None
        self.btn_nudge_down: Optional[Button] = None
        self.btn_nudge_left: Optional[Button] = None
        self.btn_nudge_right: Optional[Button] = None
        self.btn_reset_pos: Optional[Button] = None
        self.btn_done_move: Optional[Button] = None

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

        # 1. Build header buttons
        hr = self.metrics.header_rect
        btn_h = int(hr.height * 0.82)
        by = hr.y + (hr.height - btn_h) // 2

        # Scale button widths based on available header width
        btn_w = max(44, min(int(hr.width * 0.14), 72))
        gap = max(3, int(hr.width * 0.01))

        self.btn_menu = Button(
            rect=pygame.Rect(hr.x, by, btn_w, btn_h),
            label="Menu",
            is_action=True,
            border_radius=8
        )

        right_x = hr.right
        self.btn_restart = Button(
            rect=pygame.Rect(right_x - btn_w, by, btn_w, btn_h),
            label="Reset",
            is_action=True,
            border_radius=8
        )
        right_x -= (btn_w + gap)

        self.btn_move = Button(
            rect=pygame.Rect(right_x - btn_w, by, btn_w, btn_h),
            label="Done" if self.is_move_mode else "Move",
            is_action=True,
            border_radius=8
        )
        self.btn_move.is_active = self.is_move_mode
        right_x -= (btn_w + gap)

        self.btn_layout = Button(
            rect=pygame.Rect(right_x - btn_w, by, btn_w, btn_h),
            label="Layout",
            is_action=True,
            border_radius=8
        )

        # 2. Build move mode toolbar widgets
        self._build_move_toolbar()

        # 3. Build victory dialog buttons
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

    def _build_move_toolbar(self) -> None:
        """Constructs floating controls for Move / Repositioning Mode."""
        w, h = self.app.screen_width, self.app.screen_height
        panel_w = min(380, w - 20)
        panel_h = 52
        panel_x = (w - panel_w) // 2
        panel_y = h - panel_h - 10
        self.move_panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)

        pad = 4
        btn_w = (panel_w - 7 * pad) // 7
        btn_h = panel_h - 12
        by = panel_y + 6

        # [Target Group Button] (takes 2 slots)
        target_w = btn_w * 2 + pad
        target_label = f"Edit: {self.selected_move_group.capitalize()}"
        self.btn_move_target = Button(
            rect=pygame.Rect(panel_x + pad, by, target_w, btn_h),
            label=target_label,
            is_action=True,
            border_radius=6
        )

        cur_x = panel_x + pad + target_w + pad
        self.btn_nudge_left = Button(
            rect=pygame.Rect(cur_x, by, btn_w, btn_h),
            label="◄", is_action=False, border_radius=6
        )
        cur_x += btn_w + pad

        self.btn_nudge_up = Button(
            rect=pygame.Rect(cur_x, by, btn_w, btn_h),
            label="▲", is_action=False, border_radius=6
        )
        cur_x += btn_w + pad

        self.btn_nudge_down = Button(
            rect=pygame.Rect(cur_x, by, btn_w, btn_h),
            label="▼", is_action=False, border_radius=6
        )
        cur_x += btn_w + pad

        self.btn_nudge_right = Button(
            rect=pygame.Rect(cur_x, by, btn_w, btn_h),
            label="►", is_action=False, border_radius=6
        )
        cur_x += btn_w + pad

        self.btn_reset_pos = Button(
            rect=pygame.Rect(cur_x, by, btn_w, btn_h),
            label="↺", subtext="Center", is_action=True, border_radius=6
        )

    def on_resize(self, width: int, height: int) -> None:
        """Handles display resize."""
        self._rebuild_ui()

    def update(self, dt: float) -> None:
        """Updates timer when active and not won/paused."""
        if not self.is_won and not self.is_paused and not self.is_move_mode:
            self.elapsed_time += dt

    def handle_event(self, event: pygame.event.Event) -> None:
        """Processes keyboard, touch, drag, and UI events."""
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

        if self.btn_move and self.btn_move.handle_event(event):
            self.is_move_mode = not self.is_move_mode
            self._rebuild_ui()
            return

        if self.btn_restart and self.btn_restart.handle_event(event):
            self.board.restart_game()
            return

        # 3. Move / Repositioning Mode Interception
        if self.is_move_mode:
            if self._handle_move_mode_event(event):
                return

        # 4. Normal Board Selection Hit Testing
        if not self.is_move_mode:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cell_coords = self.board_view.get_cell_at_pos(event.pos, self.metrics)
                if cell_coords:
                    self.board.select(cell_coords[0], cell_coords[1])
                    return

            # 5. On-Screen Keypad Interaction
            keypad_action = self.keypad_view.handle_event(event)
            if keypad_action:
                self._execute_action(keypad_action)
                self._check_victory()
                return

            # 6. Physical Keyboard Input
            if event.type == pygame.KEYDOWN:
                self._handle_key_down(event)
                self._check_victory()

    def _handle_move_mode_event(self, event: pygame.event.Event) -> bool:
        """Handles dragging elements and clicking move toolbar buttons."""
        # Toolbar button interactions
        if self.btn_move_target and self.btn_move_target.handle_event(event):
            self.selected_move_group = "keypad" if self.selected_move_group == "board" else "board"
            self._rebuild_ui()
            return True

        nudge_step = 14
        if self.btn_nudge_up and self.btn_nudge_up.handle_event(event):
            self._nudge_selected_group(0, -nudge_step)
            return True
        if self.btn_nudge_down and self.btn_nudge_down.handle_event(event):
            self._nudge_selected_group(0, nudge_step)
            return True
        if self.btn_nudge_left and self.btn_nudge_left.handle_event(event):
            self._nudge_selected_group(-nudge_step, 0)
            return True
        if self.btn_nudge_right and self.btn_nudge_right.handle_event(event):
            self._nudge_selected_group(nudge_step, 0)
            return True
        if self.btn_reset_pos and self.btn_reset_pos.handle_event(event):
            self.app.layout_manager.reset_offsets()
            self._rebuild_ui()
            return True

        # Direct Touch / Mouse Dragging on Board or Keypad
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.metrics.board_rect.collidepoint(pos):
                self.is_dragging = True
                self.drag_target = "board"
                self.selected_move_group = "board"
                self.drag_start_pos = pos
                self._rebuild_ui()
                return True
            elif self.metrics.keypad_rect.collidepoint(pos):
                self.is_dragging = True
                self.drag_target = "keypad"
                self.selected_move_group = "keypad"
                self.drag_start_pos = pos
                self._rebuild_ui()
                return True

        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            if self.drag_start_pos:
                dx = event.pos[0] - self.drag_start_pos[0]
                dy = event.pos[1] - self.drag_start_pos[1]
                if self.drag_target == "board":
                    self.app.layout_manager.adjust_board_offset(dx, dy)
                elif self.drag_target == "keypad":
                    self.app.layout_manager.adjust_keypad_offset(dx, dy)
                self.drag_start_pos = event.pos
                self._rebuild_ui()
                return True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_dragging:
                self.is_dragging = False
                self.drag_target = None
                self.drag_start_pos = None
                return True

        return False

    def _nudge_selected_group(self, dx: int, dy: int) -> None:
        """Nudges the currently selected group (board or keypad) by (dx, dy)."""
        if self.selected_move_group == "board":
            self.app.layout_manager.adjust_board_offset(dx, dy)
        else:
            self.app.layout_manager.adjust_keypad_offset(dx, dy)
        self._rebuild_ui()

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

        # 1. Header (Menu, Timer, Difficulty, Layout, Move, Reset)
        self._render_header(surface, theme)

        # 2. Board
        self.board_view.render(surface, self.board, self.metrics, theme)

        # 3. Keypad
        self.keypad_view.render(surface, self.board, self.metrics, theme)

        # 4. Move Mode Overlay & Visual Indicators
        if self.is_move_mode:
            self._render_move_mode_overlays(surface, theme)

        # 5. Victory Overlay
        if self.is_won:
            self._render_victory_overlay(surface, theme)

    def _render_header(self, surface: pygame.Surface, theme: Theme) -> None:
        """Renders toolbar with action buttons, difficulty badge, and timer."""
        hr = self.metrics.header_rect

        # Render Header Buttons
        if self.btn_menu:
            self.btn_menu.render(surface, theme, font_size=self.metrics.font_size_small)
        if self.btn_layout:
            self.btn_layout.render(surface, theme, font_size=self.metrics.font_size_small)
        if self.btn_move:
            self.btn_move.render(surface, theme, font_size=self.metrics.font_size_small)
        if self.btn_restart:
            self.btn_restart.render(surface, theme, font_size=self.metrics.font_size_small)

        # Timer & Difficulty in center between buttons
        total_seconds = int(self.elapsed_time)
        mins = total_seconds // 60
        secs = total_seconds % 60
        time_str = f"{mins:02d}:{secs:02d}"

        # Center text coordinates
        left_bound = self.btn_menu.rect.right if self.btn_menu else hr.x
        right_bound = self.btn_layout.rect.left if self.btn_layout else hr.right
        center_x = (left_bound + right_bound) // 2

        time_font = FontCache.get_font(self.metrics.font_size_header, bold=True)
        time_surf = time_font.render(time_str, True, theme.text_primary)
        time_rect = time_surf.get_rect(center=(center_x, hr.centery - 7))
        surface.blit(time_surf, time_rect)

        diff_font = FontCache.get_font(self.metrics.font_size_small)
        diff_surf = diff_font.render(self.difficulty.value, True, theme.text_secondary)
        diff_rect = diff_surf.get_rect(center=(center_x, hr.centery + 11))
        surface.blit(diff_surf, diff_rect)

    def _render_move_mode_overlays(self, surface: pygame.Surface, theme: Theme) -> None:
        """Renders bounding box highlights, drag handles, and floating move toolbar."""
        # 1. Highlight bounding box around Board
        board_selected = (self.selected_move_group == "board")
        board_color = theme.cell_user if board_selected else theme.text_secondary
        pygame.draw.rect(surface, board_color, self.metrics.board_rect, width=3, border_radius=8)

        # Board tag
        tag_font = FontCache.get_font(14, bold=True)
        b_tag = tag_font.render("Board (Drag to Move)", True, board_color)
        surface.blit(b_tag, (self.metrics.board_rect.x + 6, self.metrics.board_rect.y - 18))

        # 2. Highlight bounding box around Keypad
        keypad_selected = (self.selected_move_group == "keypad")
        keypad_color = theme.cell_user if keypad_selected else theme.text_secondary
        pygame.draw.rect(surface, keypad_color, self.metrics.keypad_rect, width=3, border_radius=8)

        # Keypad tag
        k_tag = tag_font.render("Keypad (Drag to Move)", True, keypad_color)
        surface.blit(k_tag, (self.metrics.keypad_rect.x + 6, self.metrics.keypad_rect.y - 18))

        # 3. Draw Floating Move Panel
        Card.draw(
            surface, self.move_panel_rect,
            bg_color=theme.bg_card,
            border_color=theme.text_accent,
            border_radius=10,
            border_width=2
        )

        if self.btn_move_target:
            self.btn_move_target.render(surface, theme, font_size=13)
        if self.btn_nudge_left:
            self.btn_nudge_left.render(surface, theme, font_size=15)
        if self.btn_nudge_up:
            self.btn_nudge_up.render(surface, theme, font_size=15)
        if self.btn_nudge_down:
            self.btn_nudge_down.render(surface, theme, font_size=15)
        if self.btn_nudge_right:
            self.btn_nudge_right.render(surface, theme, font_size=15)
        if self.btn_reset_pos:
            self.btn_reset_pos.render(surface, theme, font_size=12)

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
