"""Menu scene for difficulty selection and layout/theme settings."""

import pygame
from typing import List, Tuple, TYPE_CHECKING
from ..config import Difficulty, KeypadPlacement, Theme
from .base_scene import BaseScene
from ..ui.components import Button, Card, FontCache

if TYPE_CHECKING:
    from ..app import SudokuApp


class MenuScene(BaseScene):
    """Main menu scene for selecting difficulty and configuring game options."""

    def __init__(self, app: "SudokuApp") -> None:
        super().__init__(app)
        self.difficulty_buttons: List[Tuple[Button, Difficulty]] = []
        self.layout_buttons: List[Tuple[Button, KeypadPlacement]] = []
        self.theme_button: Optional[Button] = None
        self._rebuild_ui()

    def _rebuild_ui(self) -> None:
        """Reconstructs all menu buttons based on current screen size."""
        w, h = self.app.screen_width, self.app.screen_height
        scale = min(w, h) / 600.0
        scale = max(0.7, min(scale, 1.6))

        card_w = min(int(340 * scale), w - 40)
        btn_h = max(42, int(52 * scale))
        pad = max(8, int(12 * scale))
        start_x = (w - card_w) // 2

        # 1. Difficulty Buttons
        self.difficulty_buttons.clear()
        diff_configs = [
            (Difficulty.EASY, "Easy", "49 clues"),
            (Difficulty.MEDIUM, "Medium", "39 clues"),
            (Difficulty.HARD, "Hard", "31 clues"),
            (Difficulty.EXPERT, "Expert", "25 clues"),
        ]

        diff_start_y = int(h * 0.28)
        for i, (diff, label, sub) in enumerate(diff_configs):
            rect = pygame.Rect(start_x, diff_start_y + i * (btn_h + pad), card_w, btn_h)
            btn = Button(rect=rect, label=label, subtext=sub, is_action=False, border_radius=10)
            self.difficulty_buttons.append((btn, diff))

        # 2. Keypad Placement Options (Auto, Bottom, Right)
        layout_y = diff_start_y + len(diff_configs) * (btn_h + pad) + pad * 2
        layout_btn_w = (card_w - 2 * pad) // 3
        self.layout_buttons.clear()

        layout_configs = [
            (KeypadPlacement.AUTO, "Auto", "Adapt"),
            (KeypadPlacement.BOTTOM, "Bottom", "Down"),
            (KeypadPlacement.RIGHT, "Right", "Side"),
        ]

        for i, (placement, label, sub) in enumerate(layout_configs):
            rect = pygame.Rect(start_x + i * (layout_btn_w + pad), layout_y, layout_btn_w, int(btn_h * 0.9))
            btn = Button(rect=rect, label=label, subtext=sub, is_action=True, border_radius=8)
            btn.is_active = (self.app.layout_manager.preferred_placement == placement)
            self.layout_buttons.append((btn, placement))

        # 3. Theme Toggle Button
        theme_y = layout_y + int(btn_h * 0.9) + pad * 2
        theme_rect = pygame.Rect(start_x, theme_y, card_w, int(btn_h * 0.8))
        theme_label = f"Theme: {self.app.theme.name.capitalize()}"
        self.theme_button = Button(
            rect=theme_rect, label=theme_label, is_action=False, border_radius=8
        )

    def on_resize(self, width: int, height: int) -> None:
        """Handles screen resize and recalculates button positions."""
        self._rebuild_ui()

    def handle_event(self, event: pygame.event.Event) -> None:
        """Processes difficulty selection, layout mode change, and theme toggle."""
        # Difficulty selection
        for btn, diff in self.difficulty_buttons:
            if btn.handle_event(event):
                self.app.start_game(diff)
                return

        # Layout mode selection
        for btn, placement in self.layout_buttons:
            if btn.handle_event(event):
                self.app.layout_manager.set_placement(placement)
                for b, p in self.layout_buttons:
                    b.is_active = (p == placement)
                return

        # Theme toggle
        if self.theme_button and self.theme_button.handle_event(event):
            self.app.toggle_theme()
            self.theme_button.label = f"Theme: {self.app.theme.name.capitalize()}"

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        """Renders title, subtitle, and menu cards."""
        theme = self.app.theme
        w, h = self.app.screen_width, self.app.screen_height
        surface.fill(theme.bg_primary)

        scale = min(w, h) / 600.0
        scale = max(0.7, min(scale, 1.6))

        # Title
        title_font = FontCache.get_font(int(46 * scale), bold=True)
        title_surf = title_font.render("SUDOKU", True, theme.text_accent)
        title_rect = title_surf.get_rect(center=(w // 2, int(h * 0.12)))
        surface.blit(title_surf, title_rect)

        # Subtitle
        sub_font = FontCache.get_font(int(18 * scale))
        sub_surf = sub_font.render("Choose a difficulty to begin", True, theme.text_secondary)
        sub_rect = sub_surf.get_rect(center=(w // 2, int(h * 0.19)))
        surface.blit(sub_surf, sub_rect)

        # Render difficulty buttons
        for btn, _ in self.difficulty_buttons:
            btn.render(surface, theme, font_size=int(22 * scale))

        # Layout Section Label
        if self.layout_buttons:
            lbl_y = self.layout_buttons[0][0].rect.top - int(18 * scale)
            lbl_surf = sub_font.render("Keypad Placement:", True, theme.text_secondary)
            lbl_rect = lbl_surf.get_rect(center=(w // 2, lbl_y))
            surface.blit(lbl_surf, lbl_rect)

            for btn, _ in self.layout_buttons:
                btn.render(surface, theme, font_size=int(16 * scale))

        # Render theme toggle
        if self.theme_button:
            self.theme_button.render(surface, theme, font_size=int(16 * scale))

