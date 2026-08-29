"""Board view component handling grid rendering, highlights, cell values, and notes."""

import pygame
from typing import Optional, Tuple
from ..config import Theme, GRID_SIZE, BOX_SIZE
from ..core.board import Board
from .components import FontCache
from .layout import LayoutMetrics


class BoardView:
    """Renders the 9x9 Sudoku grid and handles cell hit testing."""

    def __init__(self) -> None:
        pass

    def get_cell_at_pos(
        self, pos: Tuple[int, int], metrics: LayoutMetrics
    ) -> Optional[Tuple[int, int]]:
        """Maps screen coordinate (x, y) to (row, col) on the board."""
        bx = metrics.board_rect.x
        by = metrics.board_rect.y
        bs = metrics.board_size
        cs = metrics.cell_size

        px, py = pos
        if bx <= px < bx + bs and by <= py < by + bs:
            col = (px - bx) // cs
            row = (py - by) // cs
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                return (row, col)
        return None

    def render(
        self,
        surface: pygame.Surface,
        board: Board,
        metrics: LayoutMetrics,
        theme: Theme
    ) -> None:
        """Renders the complete board state onto surface."""
        bx = metrics.board_rect.x
        by = metrics.board_rect.y
        bs = metrics.board_size
        cs = metrics.cell_size

        # 1. Background
        pygame.draw.rect(surface, theme.bg_board, metrics.board_rect)

        # 2. Highlights (related row/col/box, matching numbers, selected cell)
        self._render_highlights(surface, board, metrics, theme)

        # 3. Cell Contents (Values & Notes)
        self._render_cells(surface, board, metrics, theme)

        # 4. Grid Lines
        self._render_grid_lines(surface, metrics, theme)

    def _render_highlights(
        self,
        surface: pygame.Surface,
        board: Board,
        metrics: LayoutMetrics,
        theme: Theme
    ) -> None:
        """Draws translucent highlight overlays for selection, related cells, matching numbers, and errors."""
        bx = metrics.board_rect.x
        by = metrics.board_rect.y
        cs = metrics.cell_size

        selected = board.selected
        selected_val = 0
        if selected:
            sr, sc = selected
            selected_val = board.get_cell(sr, sc).value

        # Create overlay surface for alpha blending
        overlay = pygame.Surface((cs, cs), pygame.SRCALPHA)

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                cell = board.get_cell(r, c)
                cell_x = bx + c * cs
                cell_y = by + r * cs

                # Error highlight
                if cell.is_error:
                    overlay.fill(theme.highlight_error)
                    surface.blit(overlay, (cell_x, cell_y))
                    continue

                if selected:
                    sr, sc = selected
                    # Selected cell
                    if r == sr and c == sc:
                        overlay.fill(theme.highlight_selected)
                        surface.blit(overlay, (cell_x, cell_y))
                    # Matching numbers across board
                    elif selected_val > 0 and cell.value == selected_val:
                        overlay.fill(theme.highlight_same_number)
                        surface.blit(overlay, (cell_x, cell_y))
                    # Same row, column, or 3x3 block
                    elif r == sr or c == sc or (r // BOX_SIZE == sr // BOX_SIZE and c // BOX_SIZE == sc // BOX_SIZE):
                        overlay.fill(theme.highlight_related)
                        surface.blit(overlay, (cell_x, cell_y))

    def _render_cells(
        self,
        surface: pygame.Surface,
        board: Board,
        metrics: LayoutMetrics,
        theme: Theme
    ) -> None:
        """Draws numbers and pencil notes inside cells."""
        bx = metrics.board_rect.x
        by = metrics.board_rect.y
        cs = metrics.cell_size

        cell_font = FontCache.get_font(metrics.font_size_cell, bold=True)
        note_font = FontCache.get_font(metrics.font_size_note)

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                cell = board.get_cell(r, c)
                cell_x = bx + c * cs
                cell_y = by + r * cs

                if cell.value != 0:
                    # Determine text color
                    if cell.is_given:
                        color = theme.cell_given
                    elif cell.is_error:
                        color = theme.cell_error
                    else:
                        color = theme.cell_user

                    text_surf = cell_font.render(str(cell.value), True, color)
                    text_rect = text_surf.get_rect(
                        center=(cell_x + cs // 2, cell_y + cs // 2)
                    )
                    surface.blit(text_surf, text_rect)

                elif cell.notes:
                    # Draw mini 3x3 notes
                    note_step = cs / 3.0
                    for n in cell.notes:
                        nr = (n - 1) // 3
                        nc = (n - 1) % 3
                        nx = cell_x + int((nc + 0.5) * note_step)
                        ny = cell_y + int((nr + 0.5) * note_step)

                        n_surf = note_font.render(str(n), True, theme.cell_note)
                        n_rect = n_surf.get_rect(center=(nx, ny))
                        surface.blit(n_surf, n_rect)

    def _render_grid_lines(
        self,
        surface: pygame.Surface,
        metrics: LayoutMetrics,
        theme: Theme
    ) -> None:
        """Draws thin 1x1 cell boundaries and thick 3x3 box boundaries."""
        bx = metrics.board_rect.x
        by = metrics.board_rect.y
        bs = metrics.board_size
        cs = metrics.cell_size

        # Thin grid lines
        for i in range(1, GRID_SIZE):
            if i % BOX_SIZE != 0:
                # Vertical line
                pygame.draw.line(
                    surface, theme.grid_thin,
                    (bx + i * cs, by), (bx + i * cs, by + bs), 1
                )
                # Horizontal line
                pygame.draw.line(
                    surface, theme.grid_thin,
                    (bx, by + i * cs), (bx + bs, by + i * cs), 1
                )

        # Thick box lines
        for i in range(0, GRID_SIZE + 1, BOX_SIZE):
            line_w = 3
            # Vertical thick line
            pygame.draw.line(
                surface, theme.grid_thick,
                (bx + i * cs, by), (bx + i * cs, by + bs), line_w
            )
            # Horizontal thick line
            pygame.draw.line(
                surface, theme.grid_thick,
                (bx, by + i * cs), (bx + bs, by + i * cs), line_w
            )

