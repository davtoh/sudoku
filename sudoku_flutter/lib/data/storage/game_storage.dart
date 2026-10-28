import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../../core/theme/app_theme.dart';
import '../../domain/models/board.dart';
import '../../domain/models/difficulty.dart';

enum KeypadPositionPreference {
  auto('Auto (Adaptive)', 'Switches automatically based on screen aspect ratio'),
  bottom('Bottom', 'Keep keypad below the board'),
  side('Side (Right)', 'Keep keypad to the side of the board');

  final String label;
  final String description;
  const KeypadPositionPreference(this.label, this.description);
}

class GameStorage {
  static const _keySavedGame = 'sudoku_saved_game';
  static const _keyTimerSeconds = 'sudoku_timer_seconds';
  static const _keyTheme = 'sudoku_theme_mode';
  static const _keyHaptics = 'sudoku_haptics_enabled';
  static const _keyAutoClearNotes = 'sudoku_auto_clear_notes';
  static const _keyAutoCheckErrors = 'sudoku_auto_check_errors';
  static const _keyKeypadPos = 'sudoku_keypad_position_pref';
  static const _keyBestTimesPrefix = 'sudoku_best_time_';
  static const _keyGamesWonPrefix = 'sudoku_games_won_';

  static Future<void> saveGame(Board board, int seconds) async {
    final prefs = await SharedPreferences.getInstance();
    final jsonStr = jsonEncode(board.toJson());
    await prefs.setString(_keySavedGame, jsonStr);
    await prefs.setInt(_keyTimerSeconds, seconds);
  }

  static Future<({Board board, int seconds})?> loadSavedGame() async {
    final prefs = await SharedPreferences.getInstance();
    final jsonStr = prefs.getString(_keySavedGame);
    if (jsonStr == null) return null;
    try {
      final map = jsonDecode(jsonStr) as Map<String, dynamic>;
      final board = Board.fromJson(map);
      final seconds = prefs.getInt(_keyTimerSeconds) ?? 0;
      return (board: board, seconds: seconds);
    } catch (_) {
      return null;
    }
  }

  static Future<void> clearSavedGame() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_keySavedGame);
    await prefs.remove(_keyTimerSeconds);
  }

  static Future<void> recordWin(Difficulty difficulty, int elapsedSeconds) async {
    final prefs = await SharedPreferences.getInstance();
    final bestKey = '$_keyBestTimesPrefix${difficulty.name}';
    final currentBest = prefs.getInt(bestKey);
    if (currentBest == null || elapsedSeconds < currentBest) {
      await prefs.setInt(bestKey, elapsedSeconds);
    }

    final winCountKey = '$_keyGamesWonPrefix${difficulty.name}';
    final currentWins = prefs.getInt(winCountKey) ?? 0;
    await prefs.setInt(winCountKey, currentWins + 1);
  }

  static Future<int?> getBestTime(Difficulty difficulty) async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getInt('$_keyBestTimesPrefix${difficulty.name}');
  }

  static Future<int> getWins(Difficulty difficulty) async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getInt('$_keyGamesWonPrefix${difficulty.name}') ?? 0;
  }

  // Settings
  static Future<AppThemeMode> loadThemeMode() async {
    final prefs = await SharedPreferences.getInstance();
    final name = prefs.getString(_keyTheme);
    return AppThemeMode.values.firstWhere(
      (m) => m.name == name,
      orElse: () => AppThemeMode.light,
    );
  }

  static Future<void> saveThemeMode(AppThemeMode mode) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_keyTheme, mode.name);
  }

  static Future<bool> loadHaptics() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool(_keyHaptics) ?? true;
  }

  static Future<void> saveHaptics(bool enabled) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_keyHaptics, enabled);
  }

  static Future<bool> loadAutoClearNotes() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool(_keyAutoClearNotes) ?? true;
  }

  static Future<void> saveAutoClearNotes(bool enabled) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_keyAutoClearNotes, enabled);
  }

  static Future<bool> loadAutoCheckErrors() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool(_keyAutoCheckErrors) ?? true;
  }

  static Future<void> saveAutoCheckErrors(bool enabled) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_keyAutoCheckErrors, enabled);
  }

  static Future<KeypadPositionPreference> loadKeypadPos() async {
    final prefs = await SharedPreferences.getInstance();
    final name = prefs.getString(_keyKeypadPos);
    return KeypadPositionPreference.values.firstWhere(
      (p) => p.name == name,
      orElse: () => KeypadPositionPreference.auto,
    );
  }

  static Future<void> saveKeypadPos(KeypadPositionPreference pref) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_keyKeypadPos, pref.name);
  }
}
