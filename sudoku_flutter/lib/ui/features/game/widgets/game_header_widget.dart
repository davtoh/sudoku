import 'package:flutter/material.dart';
import '../../../../core/theme/app_theme.dart';
import '../view_models/game_view_model.dart';

class GameHeaderWidget extends StatelessWidget {
  final GameViewModel viewModel;
  final VoidCallback onBackToMenu;
  final VoidCallback onOpenSettings;

  const GameHeaderWidget({
    super.key,
    required this.viewModel,
    required this.onBackToMenu,
    required this.onOpenSettings,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colors = theme.extension<SudokuThemeColors>() ?? AppThemes.lightColors;

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          // Left: Menu button + Difficulty Badge
          Row(
            children: [
              IconButton.filledTonal(
                icon: const Icon(Icons.arrow_back_rounded),
                tooltip: 'Back to Menu',
                onPressed: onBackToMenu,
              ),
              const SizedBox(width: 8),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                decoration: BoxDecoration(
                  color: colors.badgeBg,
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Text(
                  viewModel.difficulty.label,
                  style: TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.bold,
                    color: colors.badgeText,
                  ),
                ),
              ),
            ],
          ),

          // Center: Timer with Pause / Resume
          InkWell(
            onTap: viewModel.togglePause,
            borderRadius: BorderRadius.circular(16),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              decoration: BoxDecoration(
                color: colors.bgCard,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: colors.gridThin),
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(
                    viewModel.isPaused ? Icons.play_arrow_rounded : Icons.pause_rounded,
                    size: 16,
                    color: theme.colorScheme.primary,
                  ),
                  const SizedBox(width: 6),
                  Text(
                    viewModel.formattedTime,
                    style: TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 0.5,
                      color: colors.cellGiven,
                    ),
                  ),
                ],
              ),
            ),
          ),

          // Right: Mistakes + Restart + Settings
          Row(
            children: [
              if (viewModel.autoCheckErrors) ...[
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 5),
                  decoration: BoxDecoration(
                    color: colors.highlightError,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(Icons.close_rounded, size: 14, color: colors.cellError),
                      const SizedBox(width: 2),
                      Text(
                        '${viewModel.mistakesCount}',
                        style: TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                          color: colors.cellError,
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 6),
              ],

              IconButton(
                icon: const Icon(Icons.refresh_rounded),
                tooltip: 'Restart Puzzle',
                onPressed: () => _confirmRestart(context),
              ),

              IconButton(
                icon: const Icon(Icons.settings_outlined),
                tooltip: 'Settings',
                onPressed: onOpenSettings,
              ),
            ],
          ),
        ],
      ),
    );
  }

  void _confirmRestart(BuildContext context) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Restart Puzzle?'),
        content: const Text('This will clear all user entries and reset the timer.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: const Text('Cancel'),
          ),
          FilledButton(
            onPressed: () {
              Navigator.of(ctx).pop();
              viewModel.restartCurrentGame();
            },
            child: const Text('Restart'),
          ),
        ],
      ),
    );
  }
}
