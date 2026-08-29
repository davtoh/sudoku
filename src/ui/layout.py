"""Responsive Layout Manager for dynamic board and keypad sizing, positioning, and free movement."""

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
    """Computes responsive layouts for Sudoku board and keypad across any screen dimensions, supporting drag/move offsets."""

    def __init__(self, placement: KeypadPlacement = KeypadPlacement.AUTO) -> None:
        self.preferred_placement: KeypadPlacement = placement
        self.margin: int = 10
        self.header_height: int = 50
        
        # Free movement offsets
        self.board_offset_x: int = 0
        self.board_offset_y: int = 0
        self.keypad_offset_x: int = 0
        self.keypad_offset_y: int = 0

    def set_placement(self, placement: KeypadPlacement) -> None:
        """Sets preferred placement: AUTO, BOTTOM, or RIGHT."""
        self.preferred_placement = placement

    def set_board_offset(self, dx: int, dy: int) -> None:
        """Sets custom manual offset for the board."""
        self.board_offset_x = dx
        self.board_offset_y = dy

    def set_keypad_offset(self, dx: int, dy: int) -> None:
        """Sets custom manual offset for the keypad."""
        self.keypad_offset_x = dx
        self.keypad_offset_y = dy

    def adjust_board_offset(self, delta_x: int, delta_y: int) -> None:
        """Nudges the board position by delta."""
        self.board_offset_x += delta_x
        self.board_offset_y += delta_y

    def adjust_keypad_offset(self, delta_x: int, delta_y: int) -> None:
        """Nudges the keypad position by delta."""
        self.keypad_offset_x += delta_x
        self.keypad_offset_y += delta_y

    def reset_offsets(self) -> None:
        """Resets both board and keypad offsets to default centered layout."""
        self.board_offset_x = 0
        self.board_offset_y = 0
        self.keypad_offset_x = 0
        self.keypad_offset_y = 0

    @property
    def has_custom_offsets(self) -> bool:
        """Returns True if user has modified element positions."""
        return (
            self.board_offset_x != 0
            or self.board_offset_y != 0
            or self.keypad_offset_x != 0
            or self.keypad_offset_y != 0
        )

    def resolve_placement(self, width: int, height: int) -> KeypadPlacement:
        """Determines whether keypad goes to the bottom or right based on aspect ratio."""
        if self.preferred_placement != KeypadPlacement.AUTO:
            return self.preferred_placement
        # If width is at least 1.12x of height, landscape layout (right keypad) is optimal
        if width >= height * 1.12:
            return KeypadPlacement.RIGHT
        return KeypadPlacement.BOTTOM

    def calculate(self, screen_width: int, screen_height: int) -> LayoutMetrics:
        """Calculates bounding boxes and button geometries ensuring 100% on-screen containment."""
        placement = self.resolve_placement(screen_width, screen_height)

        # Scale base header & margins adaptively
        scale_factor = min(screen_width, screen_height) / 600.0
        scale_factor = max(0.65, min(scale_factor, 1.6))

        margin = max(6, min(14, int(self.margin * scale_factor)))
        header_h = max(38, min(56, int(self.header_height * scale_factor)))
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
        """Calculates portrait layout with Keypad strictly fitting below the Board within screen dimensions."""
        avail_w = width - 2 * margin
        avail_h = height - header_rect.bottom - 3 * margin

        # Allocate max ~60% vertical space to board so keypad always has guaranteed ample room
        max_board_h = int(avail_h * 0.60)
        max_board_dim = min(avail_w, max_board_h)

        cell_size = max(18, max_board_dim // GRID_SIZE)
        board_size = cell_size * GRID_SIZE

        # Default centered base positions
        default_board_x = (width - board_size) // 2
        default_board_y = header_rect.bottom + margin
        default_board_bottom = default_board_y + board_size

        board_x = default_board_x + self.board_offset_x
        board_y = default_board_y + self.board_offset_y
        board_rect = pygame.Rect(board_x, board_y, board_size, board_size)

        # Keypad area (independent base anchor)
        keypad_base_y = default_board_bottom + margin
        keypad_h = max(70, height - keypad_base_y - margin)
        keypad_w = min(board_size + margin * 2, width - 2 * margin)
        default_keypad_x = (width - keypad_w) // 2

        keypad_x = default_keypad_x + self.keypad_offset_x
        keypad_y = keypad_base_y + self.keypad_offset_y
        keypad_rect = pygame.Rect(keypad_x, keypad_y, keypad_w, keypad_h)

        buttons = self._layout_portrait_keypad(keypad_rect, margin)

        font_cell = max(16, int(cell_size * 0.58))
        font_note = max(9, int(cell_size * 0.26))
        font_btn = max(14, int(min(keypad_rect.width, keypad_rect.height) * 0.13))
        font_header = max(16, int(header_rect.height * 0.42))
        font_small = max(11, int(font_header * 0.72))

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
        """Calculates landscape layout with Board and Keypad centered together side-by-side."""
        avail_h = height - header_rect.bottom - 2 * margin
        avail_w = width - 2 * margin

        # Keypad gets ~35% width, max 280px
        keypad_w = max(130, min(int(avail_w * 0.36), 280))
        gap = margin * 2

        # Board gets remaining width, bounded by available height
        max_board_w = avail_w - keypad_w - gap
        max_board_dim = min(avail_h, max_board_w)

        cell_size = max(18, max_board_dim // GRID_SIZE)
        board_size = cell_size * GRID_SIZE
        keypad_h = board_size  # Match keypad height exactly to board height

        # Default centered base positions
        total_content_w = board_size + gap + keypad_w
        default_start_x = max(margin, (width - total_content_w) // 2)
        default_start_y = header_rect.bottom + (avail_h - board_size) // 2

        board_x = default_start_x + self.board_offset_x
        board_y = default_start_y + self.board_offset_y
        board_rect = pygame.Rect(board_x, board_y, board_size, board_size)

        default_keypad_x = default_start_x + board_size + gap
        keypad_x = default_keypad_x + self.keypad_offset_x
        keypad_y = default_start_y + self.keypad_offset_y
        keypad_rect = pygame.Rect(keypad_x, keypad_y, keypad_w, keypad_h)

        buttons = self._layout_landscape_keypad(keypad_rect, margin)

        font_cell = max(16, int(cell_size * 0.58))
        font_note = max(9, int(cell_size * 0.26))
        font_btn = max(14, int(min(keypad_rect.width, keypad_rect.height) * 0.09))
        font_header = max(16, int(header_rect.height * 0.42))
        font_small = max(11, int(font_header * 0.72))

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
        """Arranges keypad buttons for portrait mode strictly inside area (Action bar on top, 2 rows of 5 numbers)."""
        buttons: List[ButtonGeometry] = []
        pad = max(3, min(8, int(area.width * 0.015)))

        # Action row on top: Undo, Notes, Erase
        action_bar_h = max(26, min(44, int(area.height * 0.26)))
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

        # Numbers: 2 rows of 5 (1-5 in row 0, 6-9 + Clear in row 1)
        num_area_y = area.y + action_bar_h + pad
        num_area_h = max(30, area.bottom - num_area_y)

        cols = 5
        rows = 2
        btn_w = (area.width - (cols - 1) * pad) // cols
        btn_h = (num_area_h - (rows - 1) * pad) // rows
        btn_h = max(18, btn_h)

        # Digits 1-5 in top row, 6-9 in bottom row
        for digit in range(1, 10):
            idx = digit - 1
            r = idx // cols
            c = idx % cols
            bx = area.x + c * (btn_w + pad)
            by = num_area_y + r * (btn_h + pad)
            b_rect = pygame.Rect(bx, by, btn_w, btn_h)
            buttons.append(ButtonGeometry(id=str(digit), rect=b_rect, label=str(digit), is_action=False))

        # 10th slot (r=1, c=4): Clear button
        bx = area.x + 4 * (btn_w + pad)
        by = num_area_y + 1 * (btn_h + pad)
        buttons.append(ButtonGeometry(id="clear", rect=pygame.Rect(bx, by, btn_w, btn_h), label="Clear", is_action=True))

        return buttons

    def _layout_landscape_keypad(self, area: pygame.Rect, margin: int) -> List[ButtonGeometry]:
        """Arranges keypad buttons for landscape mode (3x3 number grid + action buttons) vertically aligned."""
        buttons: List[ButtonGeometry] = []
        pad = max(4, min(10, int(area.width * 0.025)))

        # 1. Top Action bar: Undo, Notes, Erase
        action_bar_h = max(26, min(40, int(area.height * 0.13)))
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

        # 2. Bottom Action: Clear All
        bottom_action_h = max(26, min(38, int(area.height * 0.12)))
        bottom_y = area.bottom - bottom_action_h
        clear_rect = pygame.Rect(area.x, bottom_y, area.width, bottom_action_h)
        buttons.append(ButtonGeometry(id="clear", rect=clear_rect, label="Clear All", is_action=True))

        # 3. 3x3 Numeric Grid in middle
        grid_top = area.y + action_bar_h + pad
        grid_avail_h = max(50, bottom_y - pad - grid_top)

        cols = 3
        rows = 3
        btn_w = (area.width - (cols - 1) * pad) // cols
        btn_h = (grid_avail_h - (rows - 1) * pad) // rows
        btn_dim = max(18, min(btn_w, btn_h))

        grid_total_w = 3 * btn_dim + 2 * pad
        grid_total_h = 3 * btn_dim + 2 * pad
        grid_start_x = area.x + (area.width - grid_total_w) // 2
        grid_start_y = grid_top + (grid_avail_h - grid_total_h) // 2

        for digit in range(1, 10):
            idx = digit - 1
            r = idx // cols
            c = idx % cols
            bx = grid_start_x + c * (btn_dim + pad)
            by = grid_start_y + r * (btn_dim + pad)
            b_rect = pygame.Rect(bx, by, btn_dim, btn_dim)
            buttons.append(ButtonGeometry(id=str(digit), rect=b_rect, label=str(digit), is_action=False))

        return buttons
