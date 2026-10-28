import 'package:flutter/material.dart';
import '../../../core/theme/theme_view_model.dart';
import '../../../data/storage/game_storage.dart';
import '../../../domain/models/difficulty.dart';
import '../game/game_screen.dart';
import '../game/view_models/game_view_model.dart';
import '../settings/settings_screen.dart';

class MenuScreen extends StatefulWidget {
  final GameViewModel gameViewModel;
  final ThemeViewModel themeViewModel;

  const MenuScreen({
    super.key,
    required this.gameViewModel,
    required this.themeViewModel,
  });

  @override
  State<MenuScreen> createState() => _MenuScreenState();
}

class _MenuScreenState extends State<MenuScreen> {
  bool _hasSavedGame = false;
  Map<Difficulty, int?> _bestTimes = {};
  Map<Difficulty, int> _winCounts = {};

  @override
  void initState() {
    super.initState();
    _loadStatsAndSavedGame();
  }

  Future<void> _loadStatsAndSavedGame() async {
    final saved = await GameStorage.loadSavedGame();
    final bestTimes = <Difficulty, int?>{};
    final winCounts = <Difficulty, int>{};

    for (final diff in Difficulty.values) {
      bestTimes[diff] = await GameStorage.getBestTime(diff);
      winCounts[diff] = await GameStorage.getWins(diff);
    }

    if (mounted) {
      setState(() {
        _hasSavedGame = saved != null && !saved.board.isSolved;
        _bestTimes = bestTimes;
        _winCounts = winCounts;
      });
    }
  }

  String _formatTime(int? seconds) {
    if (seconds == null) return '--:--';
    final m = (seconds ~/ 60).toString().padLeft(2, '0');
    final s = (seconds % 60).toString().padLeft(2, '0');
    return '$m:$s';
  }

  void _navigateToGame() {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (ctx) => GameScreen(
          viewModel: widget.gameViewModel,
          themeViewModel: widget.themeViewModel,
        ),
      ),
    ).then((_) => _loadStatsAndSavedGame());
  }

  void _onSelectDifficulty(Difficulty diff) async {
    await widget.gameViewModel.startNewGame(diff);
    if (!mounted) return;
    _navigateToGame();
  }

  void _onResumeGame() async {
    final restored = await widget.gameViewModel.restoreSavedGame();
    if (restored && mounted) {
      _navigateToGame();
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Sudoku'),
        centerTitle: true,
        actions: [
          IconButton(
            icon: const Icon(Icons.settings_outlined),
            tooltip: 'Settings',
            onPressed: () {
              Navigator.of(context).push(
                MaterialPageRoute(
                  builder: (ctx) => SettingsScreen(
                    gameViewModel: widget.gameViewModel,
                    themeViewModel: widget.themeViewModel,
                  ),
                ),
              );
            },
          ),
        ],
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 580),
          child: ListView(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
            children: [
              // Hero Banner
              Center(
                child: Container(
                  padding: const EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    color: theme.colorScheme.primaryContainer.withValues(alpha: 0.5),
                    shape: BoxShape.circle,
                  ),
                  child: Icon(
                    Icons.grid_on_rounded,
                    size: 64,
                    color: theme.colorScheme.primary,
                  ),
                ),
              ),
              const SizedBox(height: 16),
              Center(
                child: Text(
                  'Classic Sudoku',
                  style: theme.textTheme.headlineMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const SizedBox(height: 6),
              Center(
                child: Text(
                  'Mindful logic puzzles across all difficulty levels',
                  style: theme.textTheme.bodyMedium?.copyWith(
                    color: theme.colorScheme.onSurfaceVariant,
                  ),
                ),
              ),
              const SizedBox(height: 28),

              // Resume In-Progress Game Button
              if (_hasSavedGame) ...[
                FilledButton.tonalIcon(
                  onPressed: _onResumeGame,
                  icon: const Icon(Icons.play_arrow_rounded),
                  label: const Text('Resume Current Puzzle'),
                  style: FilledButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
                    ),
                  ),
                ),
                const SizedBox(height: 24),
              ],

              // Difficulty selection header
              Text(
                'New Game',
                style: theme.textTheme.titleMedium?.copyWith(
                  fontWeight: FontWeight.bold,
                  color: theme.colorScheme.primary,
                ),
              ),
              const SizedBox(height: 12),

              for (final diff in Difficulty.values) ...[
                _buildDifficultyCard(context, diff),
                const SizedBox(height: 12),
              ],

              const SizedBox(height: 24),

              // Desktop/Keyboard Shortcut Hint Card
              Card(
                elevation: 0,
                color: theme.colorScheme.surfaceContainerHighest.withValues(alpha: 0.3),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Icon(
                            Icons.keyboard_outlined,
                            size: 18,
                            color: theme.colorScheme.primary,
                          ),
                          const SizedBox(width: 8),
                          Text(
                            'Keyboard Controls Supported',
                            style: theme.textTheme.titleSmall?.copyWith(
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      Text(
                        '• Arrow Keys / WASD : Navigate board\n'
                        '• 1 - 9 : Place number\n'
                        '• Backspace / Delete : Erase\n'
                        '• N : Toggle Notes mode\n'
                        '• U / Ctrl+Z : Undo\n'
                        '• Space : Pause / Resume',
                        style: theme.textTheme.bodySmall?.copyWith(
                          color: theme.colorScheme.onSurfaceVariant,
                          height: 1.5,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 24),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildDifficultyCard(BuildContext context, Difficulty diff) {
    final theme = Theme.of(context);
    final bestTime = _bestTimes[diff];
    final wins = _winCounts[diff] ?? 0;

    return Card(
      elevation: 0,
      color: theme.colorScheme.surfaceContainerHighest.withValues(alpha: 0.4),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: BorderSide(
          color: theme.colorScheme.outlineVariant.withValues(alpha: 0.5),
        ),
      ),
      child: InkWell(
        onTap: () => _onSelectDifficulty(diff),
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
          child: Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      diff.label,
                      style: theme.textTheme.titleMedium?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      diff.description,
                      style: theme.textTheme.bodySmall?.copyWith(
                        color: theme.colorScheme.onSurfaceVariant,
                      ),
                    ),
                    if (wins > 0 || bestTime != null) ...[
                      const SizedBox(height: 6),
                      Row(
                        children: [
                          if (bestTime != null) ...[
                            Icon(Icons.timer_outlined, size: 14, color: theme.colorScheme.primary),
                            const SizedBox(width: 4),
                            Text(
                              'Best: ${_formatTime(bestTime)}',
                              style: theme.textTheme.labelSmall?.copyWith(
                                color: theme.colorScheme.primary,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                            const SizedBox(width: 12),
                          ],
                          Icon(Icons.check_circle_outline, size: 14, color: theme.colorScheme.secondary),
                          const SizedBox(width: 4),
                          Text(
                            'Won: $wins',
                            style: theme.textTheme.labelSmall?.copyWith(
                              color: theme.colorScheme.secondary,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ],
                ),
              ),
              const SizedBox(width: 12),
              FilledButton(
                onPressed: () => _onSelectDifficulty(diff),
                style: FilledButton.styleFrom(
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                child: const Text('Play'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
