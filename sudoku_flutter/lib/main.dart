import 'package:flutter/material.dart';
import 'core/theme/theme_view_model.dart';
import 'ui/features/game/view_models/game_view_model.dart';
import 'ui/features/menu/menu_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const SudokuApp());
}

class SudokuApp extends StatefulWidget {
  const SudokuApp({super.key});

  @override
  State<SudokuApp> createState() => _SudokuAppState();
}

class _SudokuAppState extends State<SudokuApp> {
  late final ThemeViewModel _themeViewModel;
  late final GameViewModel _gameViewModel;

  @override
  void initState() {
    super.initState();
    _themeViewModel = ThemeViewModel();
    _gameViewModel = GameViewModel();
  }

  @override
  void dispose() {
    _themeViewModel.dispose();
    _gameViewModel.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(
      listenable: _themeViewModel,
      builder: (context, _) {
        return MaterialApp(
          title: 'Sudoku',
          debugShowCheckedModeBanner: false,
          theme: _themeViewModel.currentTheme,
          home: MenuScreen(
            gameViewModel: _gameViewModel,
            themeViewModel: _themeViewModel,
          ),
        );
      },
    );
  }
}
