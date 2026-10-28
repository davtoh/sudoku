import 'dart:math';
import '../models/difficulty.dart';

typedef SudokuGrid = List<List<int>>;

/// Service providing Sudoku puzzle generation, backtracking solver,
/// uniqueness verification, and hint analysis.
class SudokuGenerator {
  static const int gridDim = 9;
  static const int boxDim = 3;

  /// Checks if placing [num] at [row], [col] in [grid] is valid under Sudoku rules.
  static bool isValidPlacement(SudokuGrid grid, int row, int col, int num) {
    // Row check
    for (int c = 0; c < gridDim; c++) {
      if (c != col && grid[row][c] == num) {
        return false;
      }
    }

    // Column check
    for (int r = 0; r < gridDim; r++) {
      if (r != row && grid[r][col] == num) {
        return false;
      }
    }

    // 3x3 Box check
    final startRow = (row ~/ boxDim) * boxDim;
    final startCol = (col ~/ boxDim) * boxDim;
    for (int r = startRow; r < startRow + boxDim; r++) {
      for (int c = startCol; c < startCol + boxDim; c++) {
        if ((r != row || c != col) && grid[r][c] == num) {
          return false;
        }
      }
    }

    return true;
  }

  /// Fills an empty 9x9 grid with a random valid completed Sudoku board.
  static bool _fillGrid(SudokuGrid grid, Random random) {
    for (int row = 0; row < gridDim; row++) {
      for (int col = 0; col < gridDim; col++) {
        if (grid[row][col] == 0) {
          final numbers = List<int>.generate(9, (i) => i + 1)..shuffle(random);
          for (final num in numbers) {
            if (isValidPlacement(grid, row, col, num)) {
              grid[row][col] = num;
              if (_fillGrid(grid, random)) {
                return true;
              }
              grid[row][col] = 0;
            }
          }
          return false;
        }
      }
    }
    return true;
  }

  /// Generates a complete valid 9x9 board.
  static SudokuGrid generateFullBoard([Random? random]) {
    final rng = random ?? Random();
    final grid = List.generate(gridDim, (_) => List.filled(gridDim, 0));
    _fillGrid(grid, rng);
    return grid;
  }

  /// Counts valid solutions up to [limit] (used to verify unique solution).
  static int countSolutions(SudokuGrid grid, {int limit = 2}) {
    int solutions = 0;

    bool solveAndCount(SudokuGrid g) {
      if (solutions >= limit) return true;

      for (int r = 0; r < gridDim; r++) {
        for (int c = 0; c < gridDim; c++) {
          if (g[r][c] == 0) {
            for (int num = 1; num <= 9; num++) {
              if (isValidPlacement(g, r, c, num)) {
                g[r][c] = num;
                if (solveAndCount(g)) {
                  if (solutions >= limit) {
                    g[r][c] = 0;
                    return true;
                  }
                }
                g[r][c] = 0;
              }
            }
            return false;
          }
        }
      }

      solutions++;
      return false;
    }

    final copiedGrid = List.generate(gridDim, (r) => List<int>.from(grid[r]));
    solveAndCount(copiedGrid);
    return solutions;
  }

  /// Generates a puzzle and its solution grid matching the Python algorithm.
  /// Returns a record: (puzzle: SudokuGrid, solution: SudokuGrid).
  static ({SudokuGrid puzzle, SudokuGrid solution}) generatePuzzle(
    Difficulty difficulty, [
    Random? random,
  ]) {
    final rng = random ?? Random();
    final solution = generateFullBoard(rng);
    final puzzle = List.generate(gridDim, (r) => List<int>.from(solution[r]));

    final emptiesTarget = difficulty.emptiesCount;

    // Collect all cell positions and shuffle
    final positions = <({int r, int c})>[];
    for (int r = 0; r < gridDim; r++) {
      for (int c = 0; c < gridDim; c++) {
        positions.add((r: r, c: c));
      }
    }
    positions.shuffle(rng);

    int removedCount = 0;
    for (final pos in positions) {
      if (removedCount >= emptiesTarget) break;

      final temp = puzzle[pos.r][pos.c];
      puzzle[pos.r][pos.c] = 0;

      // For Easy and Medium, strictly verify uniqueness
      if (difficulty == Difficulty.easy || difficulty == Difficulty.medium) {
        if (countSolutions(puzzle, limit: 2) != 1) {
          puzzle[pos.r][pos.c] = temp;
          continue;
        }
      }

      removedCount++;
    }

    // If target not reached (e.g. for Hard/Expert), remove remaining
    if (removedCount < emptiesTarget) {
      for (final pos in positions) {
        if (removedCount >= emptiesTarget) break;
        if (puzzle[pos.r][pos.c] != 0) {
          puzzle[pos.r][pos.c] = 0;
          removedCount++;
        }
      }
    }

    return (puzzle: puzzle, solution: solution);
  }

  /// Calculates candidate pencil marks (1-9) for a specific cell.
  static Set<int> getCandidatesForCell(SudokuGrid currentGrid, int row, int col) {
    if (currentGrid[row][col] != 0) return <int>{};
    final candidates = <int>{};
    for (int n = 1; n <= 9; n++) {
      if (isValidPlacement(currentGrid, row, col, n)) {
        candidates.add(n);
      }
    }
    return candidates;
  }

  /// Automatically generates all candidate notes for empty cells in a grid.
  static Map<int, Set<int>> calculateAllCandidates(SudokuGrid grid) {
    final result = <int, Set<int>>{};
    for (int r = 0; r < gridDim; r++) {
      for (int c = 0; c < gridDim; c++) {
        if (grid[r][c] == 0) {
          result[r * 9 + c] = getCandidatesForCell(grid, r, c);
        }
      }
    }
    return result;
  }
}
