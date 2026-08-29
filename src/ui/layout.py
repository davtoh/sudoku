"""Responsive Layout Manager for dynamic board and keypad sizing and positioning."""

import pygame
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from ..config import KeypadPlacement, GRID_SIZE


@dataclass
class ButtonGeometry:
    id: str
    rect: pygame.Rect
    label: str
    subtext: str = ""
    is_action: bool = False


@dataclass
class LayoutMetrics:
    screen_width: int
    screen_height: int
    placement: KeypadPlacement
    header_rect: pygame.Rect
    board_rect: pygame.Rect
    cell_size: int
    board_size: int
    keypad_rect: pygame.Rect
    keypad_buttons: List[ButtonGeometry]
    font_size_cell: int
    font_size_note: int
    font_size_btn: int
    font_size_header: int
    font_size_small: int


class LayoutManager:
    """Computes responsive layouts for Sudoku board and keypad across any screen dimensions."""

    def __init__(self, placement: KeypadPlacement = KeypadPlacement.AUTO) -> None:
        self.preferred_placement: KeypadPlacement = placement
        self.margin: int = 12
        self.header_height: int = 56
        self.board_offset_x: int = 0
        self.board_offset_y: int = 0

    def set_placement(self, placement: KeypadPlacement) -> None:
        """Sets preferred placement: AUTO, BOTTOM, or RIGHT."""
        self.preferred_placement = placement

    def set_board_offset(self, dx: int, dy: int) -> None:
        """Applies custom manual offset to board position."""
        self.board_offset_x = dx
        self.board_offset_y = dy

    def resolve_placement(self, width: int, height: int) -> KeypadPlacement:
        """Determines whether keypad goes to the bottom or right based on aspect ratio."""
        if self.preferred_placement != KeypadPlacement.AUTO:
            return self.preferred_placement
        # If width is at least 1.15x of height, landscape layout (right keypad) is optimal
        if width >= height * 1.12:
            return KeypadPlacement.RIGHT
        return KeypadPlacement.BOTTOM

    def calculate(self, screen_width: int, screen_height: int) -> LayoutMetrics:
        """Calculates layout bounding boxes and button geometries for given dimensions."""
        placement = self.resolve_placement(screen_width, screen_height)

        # Scale base header & margins adaptively for very small or large screens
        scale_factor = min(screen_width, screen_height) / 600.0
        scale_factor = max(0.65, min(scale_factor, 1.8))

        margin = max(8, int(self.margin * scale_factor))
        header_h = max(42, min(int(self.header_height * scale_factor), 72))
        header_rect = pygame.Rect(margin, margin // 2, screen_width - 2 * margin, header_h)

        if placement == KeypadPlacement.RIGHT:
            return self._calculate_landscape_layout(
                screen_width, screen_height, header_rect, margin, scale_factor
            )
        else:
            return self._calculate_portrait_layout(
                screen_width, screen_height, header_rect, margin, scale_factor
            )

    def _calculate_portrait_layout(
        self,
        width: int,
        height: int,
        header_rect: pygame.Rect,
        margin: int,
        scale: float
    ) -> LayoutMetrics:
        """Calculates layout with Keypad located below (down from) the Board."""
        available_w = width - 2 * margin
        available_h = height - header_rect.bottom - 2 * margin

        # Allocate ~65-72% height to board, remainder to keypad & controls
        keypad_min_h = int(available_h * 0.28)
        max_board_h = available_h - keypad_min_h - margin

        max_board_dim = min(available_w, max_board_h)
        cell_size = max(24, max_board_dim // GRID_SIZE)
        board_size = cell_size * GRID_SIZE

        board_x = (width - board_size) // 2 + self.board_offset_x
        board_y = header_rect.bottom + margin // 2 + self.board_offset_y
        board_rect = pygame.Rect(board_x, board_y, board_size, board_size)

        # Keypad area
        keypad_y = board_rect.bottom + margin
        keypad_h = max(80, height - keypad_y - margin)
        keypad_w = min(board_size + margin * 2, width - 2 * margin)
        keypad_x = (width - keypad_w) // 2
        keypad_rect = pygame.Rect(keypad_x, keypad_y, keypad_w, keypad_h)

        buttons = self._layout_portrait_keypad(keypad_rect, margin)

        font_cell = max(18, int(cell_size * 0.58))
        font_note = max(10, int(cell_size * 0.26))
        font_btn = max(16, int(min(keypad_rect.width, keypad_rect.height) * 0.12))
        font_header = max(18, int(header_rect.height * 0.42))
        font_small = max(12, int(font_header * 0.7))

        return LayoutMetrics(
            screen_width=width,
            screen_height=height,
            placement=KeypadPlacement.BOTTOM,
            header_rect=header_rect,
            board_rect=board_rect,
            cell_size=cell_size,
            board_size=board_size,
            keypad_rect=keypad_rect,
            keypad_buttons=buttons,
            font_size_cell=font_cell,
            font_size_note=font_note,
            font_size_btn=font_btn,
            font_size_header=font_header,
            font_size_small=font_small,
        )

    def _calculate_landscape_layout(
        self,
        width: int,
        height: int,
        header_rect: pygame.Rect,
        margin: int,
        scale: float
    ) -> LayoutMetrics:
        """Calculates layout with Keypad located to the right of the Board."""
        available_h = height - header_rect.bottom - 2 * margin
        available_w = width - 2 * margin

        # In landscape, allocate ~55-65% width to board, remainder to right control panel
        max_board_w = int(available_w * 0.62)
        max_board_dim = min(available_h, max_board_w)

        cell_size = max(24, max_board_dim // GRID_SIZE)
        board_size = cell_size * GRID_SIZE

        # Board position (left side)
        board_x = margin + self.board_offset_x
        board_y = header_rect.bottom + (available_h - board_size) // 2 + self.board_offset_y
        board_rect = pygame.Rect(board_x, board_y, board_size, board_size)

        # Keypad area (right side)
        keypad_x = board_rect.right + margin * 2
        keypad_y = header_rect.bottom + margin // 2
        keypad_w = max(140, width - keypad_x - margin)
        keypad_h = max(board_size, available_h)
        keypad_rect = pygame.Rect(keypad_x, keypad_y, keypad_w, keypad_h)

        buttons = self._layout_landscape_keypad(keypad_rect, margin)

        font_cell = max(18, int(cell_size * 0.58))
        font_note = max(10, int(cell_size * 0.26))
        font_btn = max(16, int(min(keypad_rect.width, keypad_rect.height) * 0.08))
        font_header = max(18, int(header_rect.height * 0.42))
        font_small = max(12, int(font_header * 0.7))

        return LayoutMetrics(
            screen_width=width,
            screen_height=height,
            placement=KeypadPlacement.RIGHT,
            header_rect=header_rect,
            board_rect=board_rect,
            cell_size=cell_size,
            board_size=board_size,
            keypad_rect=keypad_rect,
            keypad_buttons=buttons,
            font_size_cell=font_cell,
            font_size_note=font_note,
            font_size_btn=font_btn,
            font_size_header=font_header,
            font_size_small=font_small,
        )

    def _layout_portrait_keypad(self, area: pygame.Rect, margin: int) -> List[ButtonGeometry]:
        """Arranges keypad buttons for portrait mode (Action bar on top, 2 rows of 5 numbers)."""
        buttons: List[ButtonGeometry] = []
        pad = max(4, margin // 2)

        # Action row on top: Undo, Notes, Erase
        action_bar_h = max(32, int(area.height * 0.28))
        num_action_btns = 3
        action_btn_w = (area.width - (num_action_btns - 1) * pad) // num_action_btns

        action_configs = [
            ("undo", "Undo", "U"),
            ("notes", "Notes", "N"),
            ("erase", "Erase", "⌫"),
        ]

        for i, (btn_id, label, subtext) in enumerate(action_configs):
            bx = area.x + i * (action_btn_w + pad)
            by = area.y
            b_rect = pygame.Rect(bx, by, action_btn_w, action_bar_h)
            buttons.append(ButtonGeometry(id=btn_id, rect=b_rect, label=label, subtext=subtext, is_action=True))

        # Numbers: 2 rows of 5 (1-5 in row 0, 6-9 + Clear in row 1) or 1 row of 9 if wide
        num_area_y = area.y + action_bar_h + pad
        num_area_h = area.bottom - num_area_y

        cols = 5
        rows = 2
        btn_w = (area.width - (cols - 1) * pad) // cols
        btn_h = (num_area_h - (rows - 1) * pad) // rows

        # Digits 1-5 in top row, 6-9 + 0/blank in bottom row
        for digit in range(1, 10):
            idx = digit - 1
            r = idx // cols
            c = idx % cols
            bx = area.x + c * (btn_w + pad)
            by = num_area_y + r * (btn_h + pad)
            b_rect = pygame.Rect(bx, by, btn_w, btn_h)
            buttons.append(ButtonGeometry(id=str(digit), rect=b_rect, label=str(digit), is_action=False))

        # 10th slot (r=1, c=4): quick restart / clear cell
        bx = area.x + 4 * (btn_w + pad)
        by = num_area_y + 1 * (btn_h + pad)
        buttons.append(ButtonGeometry(id="clear", rect=pygame.Rect(bx, by, btn_w, btn_h), label="Clear", is_action=True))

        return buttons

    def _layout_landscape_keypad(self, area: pygame.Rect, margin: int) -> List[ButtonGeometry]:
        """Arranges keypad buttons for landscape mode (3x3 number grid + action buttons)."""
        buttons: List[ButtonGeometry] = []
        pad = max(6, margin // 2)

        # Action bar at top of keypad panel
        action_bar_h = max(36, int(area.height * 0.12))
        num_action_btns = 3
        action_btn_w = (area.width - (num_action_btns - 1) * pad) // num_action_btns

        action_configs = [
            ("undo", "Undo", "U"),
            ("notes", "Notes", "N"),
            ("erase", "Erase", "⌫"),
        ]

        for i, (btn_id, label, subtext) in enumerate(action_configs):
            bx = area.x + i * (action_btn_w + pad)
            by = area.y
            b_rect = pygame.Rect(bx, by, action_btn_w, action_bar_h)
            buttons.append(ButtonGeometry(id=btn_id, rect=b_rect, label=label, subtext=subtext, is_action=True))

        # 3x3 Numeric Grid
        num_area_y = area.y + action_bar_h + pad * 2
        num_area_h = int(area.height * 0.65)

        cols = 3
        rows = 3
        btn_w = (area.width - (cols - 1) * pad) // cols
        btn_h = (num_area_h - (rows - 1) * pad) // rows
        btn_dim = min(btn_w, btn_h)

        grid_start_x = area.x + (area.width - (3 * btn_dim + 2 * pad)) // 2

        for digit in range(1, 10):
            idx = digit - 1
            r = idx // cols
            c = idx % cols
            bx = grid_start_x + c * (btn_dim + pad)
            by = num_area_y + r * (btn_dim + pad)
            b_rect = pygame.Rect(bx, by, btn_dim, btn_dim)
            buttons.append(ButtonGeometry(id=str(digit), rect=b_rect, label=str(digit), is_action=False))

        # Bottom Action: Clear / Restart
        bottom_y = num_area_y + 3 * (btn_dim + pad) + pad
        bottom_h = max(34, min(48, area.bottom - bottom_y))
        clear_rect = pygame.Rect(area.x, bottom_y, area.width, bottom_h)
        buttons.append(ButtonGeometry(id="clear", rect=clear_rect, label="Clear All Errors", is_action=True))

        return buttons

