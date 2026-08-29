"""Sudoku puzzle generator and solver."""

import random
from typing import List, Tuple, Optional
from ..config import Difficulty, DIFFICULTY_EMPTIES, GRID_SIZE, BOX_SIZE

GridType = List[List[int]]


class SudokuGenerator:
    """Generates complete valid Sudoku boards and creates playable puzzles by removing numbers."""

    @staticmethod
    def is_valid_placement(grid: GridType, row: int, col: int, num: int) -> bool:
        """Checks if placing num at (row, col) is valid in the 9x9 grid."""
        # Row check
        for c in range(GRID_SIZE):
            if c != col and grid[row][c] == num:
                return False

        # Column check
        for r in range(GRID_SIZE):
            if r != row and grid[r][col] == num:
                return False

        # 3x3 Box check
        start_row = (row // BOX_SIZE) * BOX_SIZE
        start_col = (col // BOX_SIZE) * BOX_SIZE
        for r in range(start_row, start_row + BOX_SIZE):
            for c in range(start_col, start_col + BOX_SIZE):
                if (r != row or c != col) and grid[r][c] == num:
                    return False

        return True

    @classmethod
    def _fill_grid(cls, grid: GridType) -> bool:
        """Fills an empty 9x9 grid using randomized backtracking to produce a valid solution."""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if grid[row][col] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for num in nums:
                        if cls.is_valid_placement(grid, row, col, num):
                            grid[row][col] = num
                            if cls._fill_grid(grid):
                                return True
                            grid[row][col] = 0
                    return False
        return True

    @classmethod
    def generate_full_board(cls) -> GridType:
        """Creates a fully populated valid 9x9 Sudoku board."""
        grid: GridType = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        cls._fill_grid(grid)
        return grid

    @classmethod
    def count_solutions(cls, grid: GridType, limit: int = 2) -> int:
        """Counts the number of valid solutions for a given puzzle grid up to `limit`."""
        solutions = 0

        def solve_and_count(g: GridType) -> bool:
            nonlocal solutions
            if solutions >= limit:
                return True

            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    if g[r][c] == 0:
                        for num in range(1, 10):
                            if cls.is_valid_placement(g, r, c, num):
                                g[r][c] = num
                                if solve_and_count(g):
                                    if solutions >= limit:
                                        g[r][c] = 0
                                        return True
                                g[r][c] = 0
                        return False

            solutions += 1
            return False

        copied_grid = [row[:] for row in grid]
        solve_and_count(copied_grid)
        return solutions

    @classmethod
    def generate_puzzle(cls, difficulty: Difficulty = Difficulty.MEDIUM) -> Tuple[GridType, GridType]:
        """
        Generates a new puzzle and its corresponding solution.
        Returns:
            Tuple of (puzzle_grid, solution_grid)
        """
        solution = cls.generate_full_board()
        puzzle = [row[:] for row in solution]
        empties_target = DIFFICULTY_EMPTIES.get(difficulty, 42)

        # Get all cell coordinates and shuffle
        positions = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)]
        random.shuffle(positions)

        removed_count = 0
        for r, c in positions:
            if removed_count >= empties_target:
                break

            temp = puzzle[r][c]
            puzzle[r][c] = 0

            # Verify uniqueness for lower difficulties, or accept high difficulty removals
            if difficulty in (Difficulty.EASY, Difficulty.MEDIUM):
                if cls.count_solutions(puzzle, limit=2) != 1:
                    puzzle[r][c] = temp
                    continue

            removed_count += 1

        # If for hard/expert we need to remove more to match target:
        if removed_count < empties_target:
            for r, c in positions:
                if removed_count >= empties_target:
                    break
                if puzzle[r][c] != 0:
                    puzzle[r][c] = 0
                    removed_count += 1

        return puzzle, solution

