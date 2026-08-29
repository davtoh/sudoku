"""Unit tests for Cell and Board domain logic."""

import unittest
from src.config import Difficulty, GRID_SIZE
from src.core.cell import Cell
from src.core.board import Board


class TestCellAndBoard(unittest.TestCase):
    def test_cell_behavior(self):
        cell = Cell(row=0, col=0, solution_value=5, value=0, is_given=False)
        self.assertFalse(cell.is_filled)
        self.assertFalse(cell.is_correct)

        # Set value
        cell.set_value(5)
        self.assertTrue(cell.is_filled)
        self.assertTrue(cell.is_correct)

        # Given cell cannot be overwritten
        given_cell = Cell(row=0, col=1, solution_value=3, value=3, is_given=True)
        self.assertFalse(given_cell.set_value(4))
        self.assertEqual(given_cell.value, 3)

        # Notes toggle
        cell.clear()
        cell.toggle_note(2)
        cell.toggle_note(4)
        self.assertEqual(cell.notes, {2, 4})
        cell.toggle_note(2)
        self.assertEqual(cell.notes, {4})

    def test_board_selection_and_input(self):
        board = Board()
        board.new_game(Difficulty.EASY)

        # Select an empty cell
        empty_cell = None
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if not board.get_cell(r, c).is_given:
                    empty_cell = (r, c)
                    break
            if empty_cell:
                break

        self.assertIsNotNone(empty_cell)
        r, c = empty_cell
        board.select(r, c)

        # Input number
        board.input_number(7)
        self.assertEqual(board.get_cell(r, c).value, 7)

        # Undo
        board.undo()
        self.assertEqual(board.get_cell(r, c).value, 0)

    def test_board_conflict_validation(self):
        board = Board()
        # Initialize empty board
        grid = [[0] * 9 for _ in range(9)]
        board.load_from_grids(grid, grid, Difficulty.EASY)

        # Put two identical numbers in same row
        board.select(0, 0)
        board.input_number(8)
        board.select(0, 5)
        board.input_number(8)

        self.assertTrue(board.get_cell(0, 0).is_error)
        self.assertTrue(board.get_cell(0, 5).is_error)

        # Change one number
        board.select(0, 5)
        board.input_number(4)

        self.assertFalse(board.get_cell(0, 0).is_error)
        self.assertFalse(board.get_cell(0, 5).is_error)


if __name__ == "__main__":
    unittest.main()

