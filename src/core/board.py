"""Board model managing the 9x9 grid of Cells, selection, move history, validation, and win state."""

from dataclasses import dataclass
from typing import List, Optional, Tuple, Set, Dict
from ..config import GRID_SIZE, BOX_SIZE, Difficulty
from .cell import Cell
from .generator import SudokuGenerator


@dataclass
class MoveRecord:
    """Records a single move or note alteration for undo/redo functionality."""
    row: int
    col: int
    prev_value: int
    new_value: int
    prev_notes: Set[int]
    new_notes: Set[int]
    was_note: bool


class Board:
    """Manages the 9x9 Sudoku board state, selection, validation, and history."""

    def __init__(self) -> None:
        self.cells: List[List[Cell]] = [
            [Cell(row=r, col=c) for c in range(GRID_SIZE)]
            for r in range(GRID_SIZE)
        ]
        self.selected: Optional[Tuple[int, int]] = None
        self.difficulty: Difficulty = Difficulty.MEDIUM
        self.history: List[MoveRecord] = []
        self.notes_mode: bool = False

    def new_game(self, difficulty: Difficulty = Difficulty.MEDIUM) -> None:
        """Generates a new puzzle with the specified difficulty and initializes all cells."""
        self.difficulty = difficulty
        puzzle_grid, solution_grid = SudokuGenerator.generate_puzzle(difficulty)
        self.load_from_grids(puzzle_grid, solution_grid, difficulty)

    def load_from_grids(
        self,
        puzzle_grid: List[List[int]],
        solution_grid: List[List[int]],
        difficulty: Difficulty = Difficulty.MEDIUM
    ) -> None:
        """Loads pre-generated puzzle and solution grids into the board."""
        self.difficulty = difficulty
        self.history.clear()
        self.selected = None
        self.notes_mode = False

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                p_val = puzzle_grid[r][c]
                s_val = solution_grid[r][c]
                cell = self.cells[r][c]
                cell.row = r
                cell.col = c
                cell.solution_value = s_val
                cell.value = p_val
                cell.is_given = (p_val != 0)
                cell.is_error = False
                cell.notes.clear()

        # Select first empty cell if possible
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if not self.cells[r][c].is_given:
                    self.selected = (r, c)
                    return
        self.selected = (0, 0)

    def get_cell(self, row: int, col: int) -> Cell:
        """Returns the Cell at (row, col)."""
        return self.cells[row][col]

    def select(self, row: int, col: int) -> None:
        """Selects the cell at (row, col)."""
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            self.selected = (row, col)

    def move_selection(self, d_row: int, d_col: int) -> None:
        """Moves current selection by (d_row, d_col) with wrap-around boundaries."""
        if self.selected is None:
            self.selected = (0, 0)
            return

        r, c = self.selected
        new_r = (r + d_row) % GRID_SIZE
        new_c = (c + d_col) % GRID_SIZE
        self.selected = (new_r, new_c)

    def input_number(self, num: int) -> bool:
        """
        Inputs a number (1-9) or 0 (erase) into the currently selected cell.
        If notes_mode is active and num > 0, toggles pencil mark.
        """
        if self.selected is None:
            return False

        r, c = self.selected
        cell = self.cells[r][c]
        if cell.is_given:
            return False

        if num == 0:
            return self.erase_selected()

        prev_val = cell.value
        prev_notes = set(cell.notes)

        if self.notes_mode:
            # Toggle note
            cell.toggle_note(num)
            record = MoveRecord(
                row=r,
                col=c,
                prev_value=prev_val,
                new_value=cell.value,
                prev_notes=prev_notes,
                new_notes=set(cell.notes),
                was_note=True
            )
            self.history.append(record)
            return True
        else:
            # Set number
            if cell.value == num:
                # Pressing the same number again clears it
                cell.set_value(0)
            else:
                cell.set_value(num)

            record = MoveRecord(
                row=r,
                col=c,
                prev_value=prev_val,
                new_value=cell.value,
                prev_notes=prev_notes,
                new_notes=set(cell.notes),
                was_note=False
            )
            self.history.append(record)
            self.validate_conflicts()
            return True

    def erase_selected(self) -> bool:
        """Erases the value and notes in the selected cell."""
        if self.selected is None:
            return False

        r, c = self.selected
        cell = self.cells[r][c]
        if cell.is_given or (cell.value == 0 and len(cell.notes) == 0):
            return False

        prev_val = cell.value
        prev_notes = set(cell.notes)

        cell.clear()

        record = MoveRecord(
            row=r,
            col=c,
            prev_value=prev_val,
            new_value=0,
            prev_notes=prev_notes,
            new_notes=set(),
            was_note=False
        )
        self.history.append(record)
        self.validate_conflicts()
        return True

    def undo(self) -> bool:
        """Reverts the last move made by the user."""
        if not self.history:
            return False

        record = self.history.pop()
        cell = self.cells[record.row][record.col]
        cell.value = record.prev_value
        cell.notes = set(record.prev_notes)
        self.selected = (record.row, record.col)
        self.validate_conflicts()
        return True

    def toggle_notes_mode(self) -> bool:
        """Toggles pencil notes mode on/off."""
        self.notes_mode = not self.notes_mode
        return self.notes_mode

    def validate_conflicts(self) -> None:
        """Checks for duplicate numbers in rows, columns, and 3x3 boxes, marking error states."""
        # Reset errors
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                self.cells[r][c].is_error = False

        # Row check
        for r in range(GRID_SIZE):
            seen: Dict[int, List[int]] = {}
            for c in range(GRID_SIZE):
                v = self.cells[r][c].value
                if v != 0:
                    seen.setdefault(v, []).append(c)
            for v, cols in seen.items():
                if len(cols) > 1:
                    for c in cols:
                        self.cells[r][c].is_error = True

        # Column check
        for c in range(GRID_SIZE):
            seen_col: Dict[int, List[int]] = {}
            for r in range(GRID_SIZE):
                v = self.cells[r][c].value
                if v != 0:
                    seen_col.setdefault(v, []).append(r)
            for v, rows in seen_col.items():
                if len(rows) > 1:
                    for r in rows:
                        self.cells[r][c].is_error = True

        # 3x3 Box check
        for br in range(BOX_SIZE):
            for bc in range(BOX_SIZE):
                seen_box: Dict[int, List[Tuple[int, int]]] = {}
                for r in range(br * BOX_SIZE, (br + 1) * BOX_SIZE):
                    for c in range(bc * BOX_SIZE, (bc + 1) * BOX_SIZE):
                        v = self.cells[r][c].value
                        if v != 0:
                            seen_box.setdefault(v, []).append((r, c))
                for v, coords in seen_box.items():
                    if len(coords) > 1:
                        for r, c in coords:
                            self.cells[r][c].is_error = True

    def is_solved(self) -> bool:
        """Returns True if the entire grid is correctly filled according to the solution."""
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                cell = self.cells[r][c]
                if cell.value == 0 or cell.value != cell.solution_value:
                    return False
        return True

    def get_number_counts(self) -> Dict[int, int]:
        """Returns the count of each number (1-9) currently present on the board."""
        counts = {i: 0 for i in range(1, 10)}
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                v = self.cells[r][c].value
                if 1 <= v <= 9:
                    counts[v] += 1
        return counts

    def restart_game(self) -> None:
        """Resets all non-given cells to their initial empty state."""
        self.history.clear()
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                self.cells[r][c].reset_to_initial()
        self.validate_conflicts()

