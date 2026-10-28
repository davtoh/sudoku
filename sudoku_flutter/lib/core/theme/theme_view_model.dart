import 'package:flutter/material.dart';
import '../../data/storage/game_storage.dart';
import 'app_theme.dart';

class ThemeViewModel extends ChangeNotifier {
  AppThemeMode _currentMode = AppThemeMode.light;

  AppThemeMode get currentMode => _currentMode;
  ThemeData get currentTheme => AppThemes.getTheme(_currentMode);

  ThemeViewModel() {
    _loadTheme();
  }

  Future<void> _loadTheme() async {
    _currentMode = await GameStorage.loadThemeMode();
    notifyListeners();
  }

  Future<void> setTheme(AppThemeMode mode) async {
    if (_currentMode == mode) return;
    _currentMode = mode;
    notifyListeners();
    await GameStorage.saveThemeMode(mode);
  }
}
