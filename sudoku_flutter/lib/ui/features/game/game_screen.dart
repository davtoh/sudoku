import 'package:flutter/material.dart';
import 'package:sudoku_flutter/core/theme/theme_view_model.dart';
import 'package:sudoku_flutter/ui/features/game/view_models/game_view_model.dart';
import 'package:sudoku_flutter/ui/features/game/widgets/keyboard_listener_wrapper.dart';
import 'package:sudoku_flutter/ui/features/game/widgets/victory_dialog.dart';
import 'package:sudoku_flutter/ui/features/settings/settings_screen.dart';
import 'package:sudoku_flutter/ui/responsive/adaptive_sudoku_layout.dart';

class GameScreen extends StatefulWidget {
  final GameViewModel viewModel;
  final ThemeViewModel themeViewModel;

  const GameScreen({
    super.key,
    required this.viewModel,
    required this.themeViewModel,
  });

  @override
  State<GameScreen> createState() => _GameScreenState();
}

class _GameScreenState extends State<GameScreen> {
  bool _victoryDialogShown = false;

  @override
  void initState() {
    super.initState();
    widget.viewModel.addListener(_onViewModelChanged);
  }

  @override
  void dispose() {
    widget.viewModel.removeListener(_onViewModelChanged);
    super.dispose();
  }

  void _onViewModelChanged() {
    if (widget.viewModel.isWon && !_victoryDialogShown) {
      _victoryDialogShown = true;
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (!mounted) return;
        showDialog(
          context: context,
          barrierDismissible: false,
          builder: (ctx) => VictoryDialog(
            difficulty: widget.viewModel.difficulty,
            formattedTime: widget.viewModel.formattedTime,
            mistakes: widget.viewModel.mistakesCount,
            onPlayAgain: () {
              _victoryDialogShown = false;
              widget.viewModel.startNewGame(widget.viewModel.difficulty);
            },
            onBackToMenu: () {
              _victoryDialogShown = false;
              Navigator.of(context).pop();
            },
          ),
        );
      });
    } else if (!widget.viewModel.isWon) {
      _victoryDialogShown = false;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: ListenableBuilder(
        listenable: widget.viewModel,
        builder: (context, _) {
          return KeyboardListenerWrapper(
            viewModel: widget.viewModel,
            child: AdaptiveSudokuLayout(
              viewModel: widget.viewModel,
              onBackToMenu: () => Navigator.of(context).pop(),
              onOpenSettings: () {
                Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (ctx) => SettingsScreen(
                      gameViewModel: widget.viewModel,
                      themeViewModel: widget.themeViewModel,
                    ),
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }
}
