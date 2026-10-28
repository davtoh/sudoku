import 'cell.dart';
import 'difficulty.dart';
import 'move_record.dart';
import '../services/sudoku_generator.dart';

/// Sudoku Board managing the 9x9 grid of Cells, selection, move history (undo/redo),
/// conflict validation, and win state.
class Board {
  static const int size = 9;
  static const int boxSize = 3;

  late List<List<Cell>> cells;
  ({int row, int col})? selected;
  Difficulty difficulty = Difficulty.medium;
  final List<MoveRecord> history = [];
  final List<MoveRecord> redoStack = [];
  bool notesMode = false;

  Board() {
    _initCells();
  }

  void _initCells() {
    cells = List.generate(
      size,
      (r) => List.generate(size, (c) => Cell(row: r, col: c)),
    );
  }

  /// Initializes a new game with the given difficulty.
  void newGame(Difficulty diff, {SudokuGrid? customPuzzle, SudokuGrid? customSolution}) {
    difficulty = diff;
    if (customPuzzle != null && customSolution != null) {
      loadFromGrids(customPuzzle, customSolution, diff);
    } else {
      final generated = SudokuGenerator.generatePuzzle(diff);
      loadFromGrids(generated.puzzle, generated.solution, diff);
    }
  }

  /// Loads puzzle and solution 2D arrays into cells.
  void loadFromGrids(
    SudokuGrid puzzleGrid,
    SudokuGrid solutionGrid,
    Difficulty diff,
  ) {
    difficulty = diff;
    history.clear();
    redoStack.clear();
    notesMode = false;

    for (int r = 0; r < size; r++) {
      for (int c = 0; c < size; c++) {
        final pVal = puzzleGrid[r][c];
        final sVal = solutionGrid[r][c];
        final cell = cells[r][c];
        cell.solutionValue = sVal;
        cell.value = pVal;
        cell.isGiven = (pVal != 0);
        cell.isError = false;
        cell.notes.clear();
      }
    }

    // Select the first empty cell if available
    selected = null;
    for (int r = 0; r < size; r++) {
      for (int c = 0; c < size; c++) {
        if (!cells[r][c].isGiven) {
          selected = (row: r, col: c);
          return;
        }
      }
    }
    selected = (row: 0, col: 0);
  }

  Cell getCell(int row, int col) => cells[row][col];

  Cell? get selectedCell => selected != null ? cells[selected!.row][selected!.col] : null;

  void select(int row, int col) {
    if (row >= 0 && row < size && col >= 0 && col < size) {
      selected = (row: row, col: col);
    }
  }

  /// Moves selection with wrap-around boundaries.
  void moveSelection(int dRow, int dCol) {
    if (selected == null) {
      selected = (row: 0, col: 0);
      return;
    }
    final newR = (selected!.row + dRow + size) % size;
    final newC = (selected!.col + dCol + size) % size;
    selected = (row: newR, col: newC);
  }

  /// Inputs a number (1-9) or 0 (erase) into the selected cell.
  bool inputNumber(int num, {bool autoClearPeerNotes = true}) {
    if (selected == null) return false;
    final r = selected!.row;
    final c = selected!.col;
    final cell = cells[r][c];
    if (cell.isGiven) return false;

    if (num == 0) {
      return eraseSelected();
    }

    final prevVal = cell.value;
    final prevNotes = Set<int>.from(cell.notes);

    if (notesMode) {
      cell.toggleNote(num);
      final record = MoveRecord(
        row: r,
        col: c,
        prevValue: prevVal,
        newValue: cell.value,
        prevNotes: prevNotes,
        newNotes: Set<int>.from(cell.notes),
        wasNote: true,
      );
      history.add(record);
      redoStack.clear();
      return true;
    } else {
      if (cell.value == num) {
        // Toggle off if re-entering same value
        cell.setValue(0);
      } else {
        cell.setValue(num);
        if (autoClearPeerNotes) {
          _removeCandidateFromPeers(r, c, num);
        }
      }

      final record = MoveRecord(
        row: r,
        col: c,
        prevValue: prevVal,
        newValue: cell.value,
        prevNotes: prevNotes,
        newNotes: Set<int>.from(cell.notes),
        wasNote: false,
      );
      history.add(record);
      redoStack.clear();
      validateConflicts();
      return true;
    }
  }

  /// Automatically eliminates placed candidate [num] from peers in row, col, and box.
  void _removeCandidateFromPeers(int row, int col, int num) {
    // Row
    for (int c = 0; c < size; c++) {
      if (c != col) cells[row][c].notes.remove(num);
    }
    // Column
    for (int r = 0; r < size; r++) {
      if (r != row) cells[r][col].notes.remove(num);
    }
    // 3x3 Box
    final startRow = (row ~/ boxSize) * boxSize;
    final startCol = (col ~/ boxSize) * boxSize;
    for (int r = startRow; r < startRow + boxSize; r++) {
      for (int c = startCol; c < startCol + boxSize; c++) {
        if (r != row || c != col) {
          cells[r][c].notes.remove(num);
        }
      }
    }
  }

  /// Erases value and notes in the selected cell.
  bool eraseSelected() {
    if (selected == null) return false;
    final r = selected!.row;
    final c = selected!.col;
    final cell = cells[r][c];
    if (cell.isGiven || (cell.value == 0 && cell.notes.isEmpty)) return false;

    final prevVal = cell.value;
    final prevNotes = Set<int>.from(cell.notes);

    cell.clear();

    final record = MoveRecord(
      row: r,
      col: c,
      prevValue: prevVal,
      newValue: 0,
      prevNotes: prevNotes,
      newNotes: const <int>{},
      wasNote: false,
    );
    history.add(record);
    redoStack.clear();
    validateConflicts();
    return true;
  }

  /// Reverts the last move made by the user.
  bool undo() {
    if (history.isEmpty) return false;
    final record = history.removeLast();
    final cell = cells[record.row][record.col];

    redoStack.add(record);

    cell.value = record.prevValue;
    cell.notes = Set<int>.from(record.prevNotes);
    selected = (row: record.row, col: record.col);
    validateConflicts();
    return true;
  }

  /// Redoes an undone move.
  bool redo() {
    if (redoStack.isEmpty) return false;
    final record = redoStack.removeLast();
    final cell = cells[record.row][record.col];

    history.add(record);

    cell.value = record.newValue;
    cell.notes = Set<int>.from(record.newNotes);
    selected = (row: record.row, col: record.col);
    validateConflicts();
    return true;
  }

  bool toggleNotesMode() {
    notesMode = !notesMode;
    return notesMode;
  }

  /// Populates all empty cells with valid pencil candidate notes.
  void autoFillAllNotes() {
    final currentGrid = toGrid();
    for (int r = 0; r < size; r++) {
      for (int c = 0; c < size; c++) {
        if (cells[r][c].value == 0 && !cells[r][c].isGiven) {
          cells[r][c].notes = SudokuGenerator.getCandidatesForCell(currentGrid, r, c);
        }
      }
    }
  }

  /// Validates duplicate numbers in rows, columns, and 3x3 boxes.
  void validateConflicts() {
    // Reset all errors
    for (int r = 0; r < size; r++) {
      for (int c = 0; c < size; c++) {
        cells[r][c].isError = false;
      }
    }

    // Row check
    for (int r = 0; r < size; r++) {
      final seen = <int, List<int>>{};
      for (int c = 0; c < size; c++) {
        final v = cells[r][c].value;
        if (v != 0) {
          seen.putIfAbsent(v, () => []).add(c);
        }
      }
      for (final cols in seen.values) {
        if (cols.length > 1) {
          for (final c in cols) {
            cells[r][c].isError = true;
          }
        }
      }
    }

    // Column check
    for (int c = 0; c < size; c++) {
      final seenCol = <int, List<int>>{};
      for (int r = 0; r < size; r++) {
        final v = cells[r][c].value;
        if (v != 0) {
          seenCol.putIfAbsent(v, () => []).add(r);
        }
      }
      for (final rows in seenCol.values) {
        if (rows.length > 1) {
          for (final r in rows) {
            cells[r][c].isError = true;
          }
        }
      }
    }

    // 3x3 Box check
    for (int br = 0; br < boxSize; br++) {
      for (int bc = 0; bc < boxSize; bc++) {
        final seenBox = <int, List<({int r, int c})>>{};
        for (int r = br * boxSize; r < (br + 1) * boxSize; r++) {
          for (int c = bc * boxSize; c < (bc + 1) * boxSize; c++) {
            final v = cells[r][c].value;
            if (v != 0) {
              seenBox.putIfAbsent(v, () => []).add((r: r, c: c));
            }
          }
        }
        for (final coords in seenBox.values) {
          if (coords.length > 1) {
            for (final coord in coords) {
              cells[coord.r][coord.c].isError = true;
            }
          }
        }
      }
    }
  }

  /// Checks if the puzzle is completely and accurately solved.
  bool get isSolved {
    for (int r = 0; r < size; r++) {
      for (int c = 0; c < size; c++) {
        final cell = cells[r][c];
        if (cell.value == 0 || cell.value != cell.solutionValue) {
          return false;
        }
      }
    }
    return true;
  }

  /// Returns count of each number (1-9) currently on the board.
  Map<int, int> getNumberCounts() {
    final counts = {for (var i = 1; i <= 9; i++) i: 0};
    for (int r = 0; r < size; r++) {
      for (int c = 0; c < size; c++) {
        final v = cells[r][c].value;
        if (v >= 1 && v <= 9) {
          counts[v] = (counts[v] ?? 0) + 1;
        }
      }
    }
    return counts;
  }

  /// Resets all non-given cells to empty.
  void restartGame() {
    history.clear();
    redoStack.clear();
    for (int r = 0; r < size; r++) {
      for (int c = 0; c < size; c++) {
        cells[r][c].resetToInitial();
      }
    }
    validateConflicts();
  }

  /// Converts the current board values into a 9x9 integer grid.
  SudokuGrid toGrid() {
    return List.generate(
      size,
      (r) => List.generate(size, (c) => cells[r][c].value),
    );
  }

  /// Converts solution values into a 9x9 integer grid.
  SudokuGrid toSolutionGrid() {
    return List.generate(
      size,
      (r) => List.generate(size, (c) => cells[r][c].solutionValue),
    );
  }

  /// Applies a hint: reveals solution for selected cell or next unsolved cell.
  bool applyHint() {
    if (selected != null) {
      final cell = cells[selected!.row][selected!.col];
      if (!cell.isGiven && cell.value != cell.solutionValue) {
        cell.value = cell.solutionValue;
        cell.notes.clear();
        cell.isError = false;
        validateConflicts();
        return true;
      }
    }
    // Search first incorrect or empty cell
    for (int r = 0; r < size; r++) {
      for (int c = 0; c < size; c++) {
        final cell = cells[r][c];
        if (!cell.isGiven && cell.value != cell.solutionValue) {
          selected = (row: r, col: c);
          cell.value = cell.solutionValue;
          cell.notes.clear();
          cell.isError = false;
          validateConflicts();
          return true;
        }
      }
    }
    return false;
  }

  Map<String, dynamic> toJson() => {
    'difficulty': difficulty.name,
    'selectedRow': selected?.row,
    'selectedCol': selected?.col,
    'notesMode': notesMode,
    'cells': cells.map((row) => row.map((c) => c.toJson()).toList()).toList(),
    'history': history.map((h) => h.toJson()).toList(),
  };

  factory Board.fromJson(Map<String, dynamic> json) {
    final board = Board();
    board.difficulty = Difficulty.fromString(json['difficulty'] as String?);
    final selR = json['selectedRow'] as int?;
    final selC = json['selectedCol'] as int?;
    if (selR != null && selC != null) {
      board.selected = (row: selR, col: selC);
    }
    board.notesMode = json['notesMode'] as bool? ?? false;

    if (json['cells'] != null) {
      final rawCells = json['cells'] as List<dynamic>;
      for (int r = 0; r < size && r < rawCells.length; r++) {
        final rowList = rawCells[r] as List<dynamic>;
        for (int c = 0; c < size && c < rowList.length; c++) {
          board.cells[r][c] = Cell.fromJson(rowList[c] as Map<String, dynamic>);
        }
      }
    }
    if (json['history'] != null) {
      final rawHistory = json['history'] as List<dynamic>;
      for (final h in rawHistory) {
        board.history.add(MoveRecord.fromJson(h as Map<String, dynamic>));
      }
    }
    board.validateConflicts();
    return board;
  }
}
