"""Keypad view component managing on-screen number and action buttons."""

import pygame
from typing import Dict, Optional
from ..config import Theme
from ..core.board import Board
from .components import Button
from .layout import LayoutMetrics


class KeypadView:
    """Manages responsive buttons for digits 1-9, notes toggle, undo, erase, and clear."""

    def __init__(self) -> None:
        self.buttons: Dict[str, Button] = {}

    def sync_layout(self, metrics: LayoutMetrics) -> None:
        """Synchronizes button instances and geometries with current layout metrics."""
        current_ids = set()
        for b_geo in metrics.keypad_buttons:
            current_ids.add(b_geo.id)
            if b_geo.id in self.buttons:
                self.buttons[b_geo.id].update_geometry(b_geo.rect)
                self.buttons[b_geo.id].label = b_geo.label
                self.buttons[b_geo.id].subtext = b_geo.subtext
                self.buttons[b_geo.id].is_action = b_geo.is_action
            else:
                self.buttons[b_geo.id] = Button(
                    rect=b_geo.rect,
                    label=b_geo.label,
                    id=b_geo.id,
                    subtext=b_geo.subtext,
                    is_action=b_geo.is_action
                )

        # Remove obsolete buttons
        to_remove = [k for k in self.buttons if k not in current_ids]
        for k in to_remove:
            del self.buttons[k]

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """Dispatches event to keypad buttons. Returns button ID if one was activated."""
        for btn_id, button in self.buttons.items():
            if button.handle_event(event):
                return btn_id
        return None

    def render(
        self,
        surface: pygame.Surface,
        board: Board,
        metrics: LayoutMetrics,
        theme: Theme
    ) -> None:
        """Updates button active/disabled states and renders all keypad buttons."""
        counts = board.get_number_counts()

        # Update notes mode toggle button active state
        if "notes" in self.buttons:
            self.buttons["notes"].is_active = board.notes_mode

        # Update number buttons disabled state if 9 of that digit are already placed
        for digit in range(1, 10):
            d_str = str(digit)
            if d_str in self.buttons:
                is_completed = (counts.get(digit, 0) >= 9)
                self.buttons[d_str].is_disabled = is_completed

        # Render each button
        for button in self.buttons.values():
            btn_font_size = metrics.font_size_btn
            if button.is_action and len(button.label) > 4:
                btn_font_size = max(13, int(metrics.font_size_btn * 0.8))
            button.render(surface, theme, font_size=btn_font_size)

