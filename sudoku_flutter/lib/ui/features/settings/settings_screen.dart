import 'package:flutter/material.dart';
import 'package:sudoku_flutter/core/theme/app_theme.dart';
import 'package:sudoku_flutter/core/theme/theme_view_model.dart';
import 'package:sudoku_flutter/core/utils/haptic_util.dart';
import 'package:sudoku_flutter/data/storage/game_storage.dart';
import 'package:sudoku_flutter/ui/features/game/view_models/game_view_model.dart';

class SettingsScreen extends StatelessWidget {
  final GameViewModel gameViewModel;
  final ThemeViewModel themeViewModel;

  const SettingsScreen({
    super.key,
    required this.gameViewModel,
    required this.themeViewModel,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Settings'),
        centerTitle: true,
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 600),
          child: ListView(
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
            children: [
              _buildSectionHeader(context, 'Appearance & Theme'),
              ListenableBuilder(
                listenable: themeViewModel,
                builder: (context, _) {
                  return Card(
                    elevation: 0,
                    color: theme.colorScheme.surfaceContainerHighest.withValues(alpha: 0.4),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Padding(
                      padding: const EdgeInsets.all(12),
                      child: Column(
                        children: [
                          for (final mode in AppThemeMode.values)
                            ListTile(
                              leading: Icon(mode.icon),
                              title: Text(mode.label),
                              trailing: mode == themeViewModel.currentMode
                                  ? Icon(Icons.check_circle, color: theme.colorScheme.primary)
                                  : const Icon(Icons.circle_outlined),
                              onTap: () => themeViewModel.setTheme(mode),
                            ),
                        ],
                      ),
                    ),
                  );
                },
              ),
              const SizedBox(height: 24),

              _buildSectionHeader(context, 'Layout & Controls'),
              ListenableBuilder(
                listenable: gameViewModel,
                builder: (context, _) {
                  return Card(
                    elevation: 0,
                    color: theme.colorScheme.surfaceContainerHighest.withValues(alpha: 0.4),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Padding(
                      padding: const EdgeInsets.all(12),
                      child: Column(
                        children: [
                          for (final pos in KeypadPositionPreference.values)
                            ListTile(
                              title: Text(pos.label),
                              subtitle: Text(pos.description),
                              trailing: pos == gameViewModel.keypadPos
                                  ? Icon(Icons.check_circle, color: theme.colorScheme.primary)
                                  : const Icon(Icons.circle_outlined),
                              onTap: () => gameViewModel.setKeypadPos(pos),
                            ),
                        ],
                      ),
                    ),
                  );
                },
              ),
              const SizedBox(height: 24),

              _buildSectionHeader(context, 'Gameplay Helpers'),
              ListenableBuilder(
                listenable: gameViewModel,
                builder: (context, _) {
                  return Card(
                    elevation: 0,
                    color: theme.colorScheme.surfaceContainerHighest.withValues(alpha: 0.4),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Column(
                      children: [
                        SwitchListTile(
                          title: const Text('Auto-Clear Notes'),
                          subtitle: const Text(
                            'Automatically remove numbers from notes in the same row, column, and box',
                          ),
                          value: gameViewModel.autoClearNotes,
                          onChanged: gameViewModel.setAutoClearNotes,
                        ),
                        const Divider(height: 1),
                        SwitchListTile(
                          title: const Text('Highlight Conflicts & Errors'),
                          subtitle: const Text(
                            'Highlight duplicate numbers and incorrect entries immediately',
                          ),
                          value: gameViewModel.autoCheckErrors,
                          onChanged: gameViewModel.setAutoCheckErrors,
                        ),
                        const Divider(height: 1),
                        SwitchListTile(
                          title: const Text('Haptic Feedback'),
                          subtitle: const Text('Vibrate gently on tap, notes, and errors'),
                          value: HapticUtil.enabled,
                          onChanged: gameViewModel.setHaptics,
                        ),
                      ],
                    ),
                  );
                },
              ),
              const SizedBox(height: 24),

              // About section
              Center(
                child: Text(
                  'Sudoku Flutter v1.0.0\nModernized from Python codebase',
                  textAlign: TextAlign.center,
                  style: theme.textTheme.bodySmall?.copyWith(
                    color: theme.colorScheme.onSurfaceVariant,
                  ),
                ),
              ),
              const SizedBox(height: 16),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSectionHeader(BuildContext context, String title) {
    return Padding(
      padding: const EdgeInsets.only(left: 4, bottom: 8),
      child: Text(
        title,
        style: Theme.of(context).textTheme.titleSmall?.copyWith(
          fontWeight: FontWeight.bold,
          color: Theme.of(context).colorScheme.primary,
        ),
      ),
    );
  }
}
