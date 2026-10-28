import 'package:flutter_test/flutter_test.dart';
import 'package:sudoku_flutter/domain/models/board.dart';
import 'package:sudoku_flutter/domain/models/cell.dart';
import 'package:sudoku_flutter/domain/models/difficulty.dart';
import 'package:sudoku_flutter/domain/services/sudoku_generator.dart';

void main() {
  group('Cell Model Tests', () {
    test('initializes correctly and respects isGiven immutability', () {
      final cell = Cell(row: 0, col: 0, value: 5, solutionValue: 5, isGiven: true);
      expect(cell.isGiven, isTrue);
      expect(cell.value, equals(5));

      // Attempting to change given cell returns false
      expect(cell.setValue(3), isFalse);
      expect(cell.value, equals(5));
      expect(cell.clear(), isFalse);
    });

    test('mutable cell supports value changes and notes', () {
      final cell = Cell(row: 2, col: 3, solutionValue: 8);
      expect(cell.isGiven, isFalse);

      expect(cell.setValue(8), isTrue);
      expect(cell.value, equals(8));
      expect(cell.isCorrect, isTrue);

      cell.setValue(0);
      expect(cell.toggleNote(4), isTrue);
      expect(cell.notes.contains(4), isTrue);
      expect(cell.toggleNote(4), isTrue);
      expect(cell.notes.contains(4), isFalse);
    });
  });

  group('SudokuGenerator & Solver Tests', () {
    test('generateFullBoard produces valid 9x9 Sudoku grid', () {
      final board = SudokuGenerator.generateFullBoard();
      expect(board.length, equals(9));
      expect(board[0].length, equals(9));

      // Check all cells filled 1-9
      for (int r = 0; r < 9; r++) {
        for (int c = 0; c < 9; c++) {
          expect(board[r][c], inInclusiveRange(1, 9));
        }
      }

      // Check rows have unique digits 1-9
      for (int r = 0; r < 9; r++) {
        expect(board[r].toSet(), equals({1, 2, 3, 4, 5, 6, 7, 8, 9}));
      }

      // Check columns have unique digits 1-9
      for (int c = 0; c < 9; c++) {
        final colSet = {for (int r = 0; r < 9; r++) board[r][c]};
        expect(colSet, equals({1, 2, 3, 4, 5, 6, 7, 8, 9}));
      }

      // Check 3x3 boxes have unique digits 1-9
      for (int br = 0; br < 3; br++) {
        for (int bc = 0; bc < 3; bc++) {
          final boxSet = <int>{};
          for (int r = 0; r < 3; r++) {
            for (int c = 0; c < 3; c++) {
              boxSet.add(board[br * 3 + r][bc * 3 + c]);
            }
          }
          expect(boxSet, equals({1, 2, 3, 4, 5, 6, 7, 8, 9}));
        }
      }
    });

    test('generatePuzzle produces unique solution puzzle for Easy', () {
      final generated = SudokuGenerator.generatePuzzle(Difficulty.easy);
      int empties = 0;
      for (int r = 0; r < 9; r++) {
        for (int c = 0; c < 9; c++) {
          if (generated.puzzle[r][c] == 0) empties++;
        }
      }
      expect(empties, greaterThanOrEqualTo(30));
      expect(SudokuGenerator.countSolutions(generated.puzzle, limit: 2), equals(1));
    });
  });

  group('Board Domain Logic Tests', () {
    test('input, undo, redo, and win check flow', () {
      final board = Board();
      final fullBoard = SudokuGenerator.generateFullBoard();
      final puzzle = List.generate(9, (r) => List<int>.from(fullBoard[r]));
      // Remove one cell
      puzzle[0][0] = 0;

      board.loadFromGrids(puzzle, fullBoard, Difficulty.easy);
      board.select(0, 0);

      expect(board.isSolved, isFalse);

      // Input correct value
      final correctVal = fullBoard[0][0];
      board.inputNumber(correctVal);
      expect(board.isSolved, isTrue);

      // Undo
      board.undo();
      expect(board.cells[0][0].value, equals(0));
      expect(board.isSolved, isFalse);

      // Redo
      board.redo();
      expect(board.cells[0][0].value, equals(correctVal));
      expect(board.isSolved, isTrue);
    });

    test('conflict detection marks conflicting cells', () {
      final board = Board();
      final empty = List.generate(9, (_) => List.filled(9, 0));
      board.loadFromGrids(empty, empty, Difficulty.easy);

      board.select(0, 0);
      board.inputNumber(7);
      board.select(0, 5);
      board.inputNumber(7);

      board.validateConflicts();
      expect(board.cells[0][0].isError, isTrue);
      expect(board.cells[0][5].isError, isTrue);
      expect(board.cells[1][0].isError, isFalse);
    });
  });
}
