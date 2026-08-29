"""Unit tests for SudokuGenerator and Solver."""

import unittest
from src.config import Difficulty, GRID_SIZE
from src.core.generator import SudokuGenerator


class TestSudokuGenerator(unittest.TestCase):
    def test_full_board_validity(self):
        board = SudokuGenerator.generate_full_board()
        self.assertEqual(len(board), GRID_SIZE)
        self.assertEqual(len(board[0]), GRID_SIZE)

        # Check all cells are filled (1-9)
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                self.assertIn(board[r][c], range(1, 10))

        # Check rows contain unique digits 1-9
        for r in range(GRID_SIZE):
            self.assertEqual(set(board[r]), set(range(1, 10)))

        # Check columns contain unique digits 1-9
        for c in range(GRID_SIZE):
            col_vals = [board[r][c] for r in range(GRID_SIZE)]
            self.assertEqual(set(col_vals), set(range(1, 10)))

        # Check 3x3 boxes contain unique digits 1-9
        for br in range(3):
            for bc in range(3):
                box_vals = [
                    board[br * 3 + r][bc * 3 + c]
                    for r in range(3)
                    for c in range(3)
                ]
                self.assertEqual(set(box_vals), set(range(1, 10)))

    def test_puzzle_generation_difficulty(self):
        puzzle, solution = SudokuGenerator.generate_puzzle(Difficulty.EASY)
        empties = sum(1 for r in range(GRID_SIZE) for c in range(GRID_SIZE) if puzzle[r][c] == 0)
        self.assertGreaterEqual(empties, 30)

        # Solution should be valid
        self.assertEqual(SudokuGenerator.count_solutions(solution, limit=2), 1)


if __name__ == "__main__":
    unittest.main()

