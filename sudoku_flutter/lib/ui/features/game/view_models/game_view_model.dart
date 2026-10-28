import 'dart:async';
import 'package:flutter/foundation.dart';
import '../../../../core/utils/haptic_util.dart';
import '../../../../data/storage/game_storage.dart';
import '../../../../domain/models/board.dart';
import '../../../../domain/models/difficulty.dart';
import '../../../../domain/services/sudoku_generator.dart';

/// Top-level isolate worker function for background puzzle generation.
({SudokuGrid puzzle, SudokuGrid solution}) _generateWorker(Difficulty difficulty) {
  return SudokuGenerator.generatePuzzle(difficulty);
}

class GameViewModel extends ChangeNotifier {
  Board _board = Board();
  int _timerSeconds = 0;
  Timer? _timer;
  bool _isPaused = false;
  bool _isWon = false;
  bool _isGenerating = false;
  int _mistakesCount = 0;

  // Settings
  bool _autoClearNotes = true;
  bool _autoCheckErrors = true;
  KeypadPositionPreference _keypadPos = KeypadPositionPreference.auto;

  Board get board => _board;
  int get timerSeconds => _timerSeconds;
  bool get isPaused => _isPaused;
  bool get isWon => _isWon;
  bool get isGenerating => _isGenerating;
  int get mistakesCount => _mistakesCount;
  bool get autoClearNotes => _autoClearNotes;
  bool get autoCheckErrors => _autoCheckErrors;
  KeypadPositionPreference get keypadPos => _keypadPos;

  Difficulty get difficulty => _board.difficulty;
  ({int row, int col})? get selected => _board.selected;
  bool get notesMode => _board.notesMode;
  bool get canUndo => _board.history.isNotEmpty;
  bool get canRedo => _board.redoStack.isNotEmpty;

  GameViewModel() {
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    _autoClearNotes = await GameStorage.loadAutoClearNotes();
    _autoCheckErrors = await GameStorage.loadAutoCheckErrors();
    _keypadPos = await GameStorage.loadKeypadPos();
    HapticUtil.enabled = await GameStorage.loadHaptics();
    notifyListeners();
  }

  void _startTimer() {
    _timer?.cancel();
    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (!_isPaused && !_isWon && !_isGenerating) {
        _timerSeconds++;
        notifyListeners();
        // Periodic auto-save every 10 seconds
        if (_timerSeconds % 10 == 0) {
          GameStorage.saveGame(_board, _timerSeconds);
        }
      }
    });
  }

  /// Starts a new game with the given difficulty, generating in background isolate.
  Future<void> startNewGame(Difficulty diff) async {
    _isGenerating = true;
    _isWon = false;
    _isPaused = false;
    _mistakesCount = 0;
    _timerSeconds = 0;
    _timer?.cancel();
    notifyListeners();

    try {
      final result = await compute(_generateWorker, diff);
      _board.loadFromGrids(result.puzzle, result.solution, diff);
    } catch (_) {
      // Fallback in case compute is unavailable (e.g., test environment)
      _board.newGame(diff);
    } finally {
      _isGenerating = false;
      _startTimer();
      await GameStorage.saveGame(_board, _timerSeconds);
      notifyListeners();
    }
  }

  /// Attempts to restore a previously saved game. Returns true if restored.
  Future<bool> restoreSavedGame() async {
    final saved = await GameStorage.loadSavedGame();
    if (saved != null) {
      _board = saved.board;
      _timerSeconds = saved.seconds;
      _isWon = _board.isSolved;
      _isPaused = false;
      _isGenerating = false;
      if (!_isWon) {
        _startTimer();
      }
      notifyListeners();
      return true;
    }
    return false;
  }

  void selectCell(int r, int c) {
    if (_isPaused || _isWon) return;
    HapticUtil.selection();
    _board.select(r, c);
    notifyListeners();
  }

  void moveSelection(int dr, int dc) {
    if (_isPaused || _isWon) return;
    HapticUtil.selection();
    _board.moveSelection(dr, dc);
    notifyListeners();
  }

  void inputNumber(int num) {
    if (_isPaused || _isWon || _board.selected == null) return;

    final cell = _board.selectedCell;
    if (cell == null || cell.isGiven) return;

    final success = _board.inputNumber(num, autoClearPeerNotes: _autoClearNotes);
    if (!success) return;

    if (_board.notesMode) {
      HapticUtil.light();
    } else {
      if (num != 0 && _autoCheckErrors && cell.value != cell.solutionValue) {
        _mistakesCount++;
        HapticUtil.error();
      } else {
        HapticUtil.medium();
      }
    }

    _checkWinCondition();
    GameStorage.saveGame(_board, _timerSeconds);
    notifyListeners();
  }

  void erase() {
    if (_isPaused || _isWon) return;
    if (_board.eraseSelected()) {
      HapticUtil.light();
      GameStorage.saveGame(_board, _timerSeconds);
      notifyListeners();
    }
  }

  void undo() {
    if (_isPaused || _isWon) return;
    if (_board.undo()) {
      HapticUtil.light();
      GameStorage.saveGame(_board, _timerSeconds);
      notifyListeners();
    }
  }

  void redo() {
    if (_isPaused || _isWon) return;
    if (_board.redo()) {
      HapticUtil.light();
      GameStorage.saveGame(_board, _timerSeconds);
      notifyListeners();
    }
  }

  void toggleNotesMode() {
    HapticUtil.selection();
    _board.toggleNotesMode();
    notifyListeners();
  }

  void togglePause() {
    if (_isWon) return;
    HapticUtil.light();
    _isPaused = !_isPaused;
    notifyListeners();
  }

  void applyHint() {
    if (_isPaused || _isWon) return;
    if (_board.applyHint()) {
      HapticUtil.medium();
      _checkWinCondition();
      GameStorage.saveGame(_board, _timerSeconds);
      notifyListeners();
    }
  }

  void autoFillCandidates() {
    if (_isPaused || _isWon) return;
    HapticUtil.medium();
    _board.autoFillAllNotes();
    GameStorage.saveGame(_board, _timerSeconds);
    notifyListeners();
  }

  void restartCurrentGame() {
    HapticUtil.light();
    _board.restartGame();
    _timerSeconds = 0;
    _mistakesCount = 0;
    _isWon = false;
    _isPaused = false;
    _startTimer();
    GameStorage.saveGame(_board, _timerSeconds);
    notifyListeners();
  }

  void _checkWinCondition() {
    if (_board.isSolved) {
      _isWon = true;
      _timer?.cancel();
      HapticUtil.heavy();
      GameStorage.recordWin(_board.difficulty, _timerSeconds);
      GameStorage.clearSavedGame();
    }
  }

  // Settings setters
  Future<void> setAutoClearNotes(bool val) async {
    _autoClearNotes = val;
    notifyListeners();
    await GameStorage.saveAutoClearNotes(val);
  }

  Future<void> setAutoCheckErrors(bool val) async {
    _autoCheckErrors = val;
    if (!val) {
      // Clear error flags
      for (final row in _board.cells) {
        for (final cell in row) {
          cell.isError = false;
        }
      }
    } else {
      _board.validateConflicts();
    }
    notifyListeners();
    await GameStorage.saveAutoCheckErrors(val);
  }

  Future<void> setKeypadPos(KeypadPositionPreference pos) async {
    _keypadPos = pos;
    notifyListeners();
    await GameStorage.saveKeypadPos(pos);
  }

  Future<void> setHaptics(bool val) async {
    HapticUtil.enabled = val;
    notifyListeners();
    await GameStorage.saveHaptics(val);
  }

  String get formattedTime {
    final minutes = (_timerSeconds ~/ 60).toString().padLeft(2, '0');
    final seconds = (_timerSeconds % 60).toString().padLeft(2, '0');
    return '$minutes:$seconds';
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }
}
