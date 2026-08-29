"""Cell model representing a single cell in the Sudoku grid."""

from dataclasses import dataclass, field
from typing import Set


@dataclass
class Cell:
    row: int
    col: int
    solution_value: int = 0
    value: int = 0
    is_given: bool = False
    is_error: bool = False
    notes: Set[int] = field(default_factory=set)

    def set_value(self, new_val: int) -> bool:
        """Sets the cell's value. Pre-filled/given cells cannot be modified."""
        if self.is_given:
            return False
        if not (0 <= new_val <= 9):
            return False
        self.value = new_val
        if new_val != 0:
            self.notes.clear()
            self.is_error = False
        return True

    def clear(self) -> bool:
        """Clears the value and notes of the cell if it is not a given clue."""
        if self.is_given:
            return False
        self.value = 0
        self.notes.clear()
        self.is_error = False
        return True

    def toggle_note(self, note_digit: int) -> bool:
        """Toggles a pencil note (1-9). If cell already has a fixed value, does nothing."""
        if self.is_given or self.value != 0:
            return False
        if 1 <= note_digit <= 9:
            if note_digit in self.notes:
                self.notes.remove(note_digit)
            else:
                self.notes.add(note_digit)
            return True
        return False

    def clear_notes(self) -> None:
        """Clears all pencil notes in this cell."""
        self.notes.clear()

    @property
    def is_filled(self) -> bool:
        """Returns True if the cell has a non-zero value."""
        return self.value != 0

    @property
    def is_correct(self) -> bool:
        """Returns True if the cell matches its solution value."""
        return self.value == self.solution_value

    def reset_to_initial(self) -> None:
        """Resets the cell to its initial puzzle state."""
        if not self.is_given:
            self.value = 0
            self.notes.clear()
            self.is_error = False

