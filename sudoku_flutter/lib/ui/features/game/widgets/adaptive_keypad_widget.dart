import 'package:flutter/material.dart';
import '../../../../core/theme/app_theme.dart';
import '../view_models/game_view_model.dart';

class AdaptiveKeypadWidget extends StatelessWidget {
  final GameViewModel viewModel;
  final bool isCompact;

  const AdaptiveKeypadWidget({
    super.key,
    required this.viewModel,
    this.isCompact = false,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colors = theme.extension<SudokuThemeColors>() ?? AppThemes.lightColors;
    final counts = viewModel.board.getNumberCounts();

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        // Top Toolbar: Undo, Erase, Notes, Hint, Auto-Pencil
        _buildActionToolbar(context, colors, theme),
        const SizedBox(height: 12),

        // Numeric Keypad 1-9
        _buildNumericKeypad(context, colors, theme, counts),
      ],
    );
  }

  Widget _buildActionToolbar(
    BuildContext context,
    SudokuThemeColors colors,
    ThemeData theme,
  ) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        // Undo
        _buildActionButton(
          context: context,
          icon: Icons.undo_rounded,
          label: 'Undo',
          isEnabled: viewModel.canUndo,
          onTap: viewModel.undo,
          colors: colors,
        ),

        // Erase
        _buildActionButton(
          context: context,
          icon: Icons.backspace_outlined,
          label: 'Erase',
          isEnabled: viewModel.selected != null,
          onTap: viewModel.erase,
          colors: colors,
        ),

        // Notes Toggle
        _buildActionButton(
          context: context,
          icon: Icons.edit_note_rounded,
          label: 'Notes',
          isActive: viewModel.notesMode,
          isEnabled: true,
          onTap: viewModel.toggleNotesMode,
          colors: colors,
          badge: viewModel.notesMode ? 'ON' : 'OFF',
        ),

        // Hint
        _buildActionButton(
          context: context,
          icon: Icons.lightbulb_outline_rounded,
          label: 'Hint',
          isEnabled: true,
          onTap: viewModel.applyHint,
          colors: colors,
        ),

        // Auto-Pencil Candidates
        _buildActionButton(
          context: context,
          icon: Icons.auto_fix_high_rounded,
          label: 'Auto',
          isEnabled: true,
          onTap: viewModel.autoFillCandidates,
          colors: colors,
          tooltip: 'Autofill all candidate notes',
        ),
      ],
    );
  }

  Widget _buildActionButton({
    required BuildContext context,
    required IconData icon,
    required String label,
    required VoidCallback onTap,
    required SudokuThemeColors colors,
    bool isEnabled = true,
    bool isActive = false,
    String? badge,
    String? tooltip,
  }) {
    final theme = Theme.of(context);
    final activeBg = theme.colorScheme.primaryContainer;
    final activeText = theme.colorScheme.onPrimaryContainer;

    Widget btn = InkWell(
      onTap: isEnabled ? onTap : null,
      borderRadius: BorderRadius.circular(12),
      child: Opacity(
        opacity: isEnabled ? 1.0 : 0.4,
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
          decoration: BoxDecoration(
            color: isActive ? activeBg : colors.keypadButtonBg,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(
              color: isActive
                  ? theme.colorScheme.primary
                  : colors.gridThin,
              width: 1.2,
            ),
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Stack(
                clipBehavior: Clip.none,
                children: [
                  Icon(
                    icon,
                    size: 22,
                    color: isActive ? activeText : colors.keypadButtonText,
                  ),
                  if (badge != null)
                    Positioned(
                      top: -6,
                      right: -10,
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 1),
                        decoration: BoxDecoration(
                          color: isActive ? theme.colorScheme.primary : colors.badgeBg,
                          borderRadius: BorderRadius.circular(6),
                        ),
                        child: Text(
                          badge,
                          style: TextStyle(
                            fontSize: 9,
                            fontWeight: FontWeight.bold,
                            color: isActive ? Colors.white : colors.badgeText,
                          ),
                        ),
                      ),
                    ),
                ],
              ),
              const SizedBox(height: 3),
              Text(
                label,
                style: TextStyle(
                  fontSize: 11,
                  fontWeight: FontWeight.w600,
                  color: isActive ? activeText : colors.keypadButtonText,
                ),
              ),
            ],
          ),
        ),
      ),
    );

    if (tooltip != null) {
      btn = Tooltip(message: tooltip, child: btn);
    }
    return btn;
  }

  Widget _buildNumericKeypad(
    BuildContext context,
    SudokuThemeColors colors,
    ThemeData theme,
    Map<int, int> counts,
  ) {
    return LayoutBuilder(
      builder: (context, constraints) {
        // If width allows a neat single row of 9 numbers
        final isWideEnoughForSingleRow = constraints.maxWidth >= 480;

        if (isWideEnoughForSingleRow) {
          return Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              for (int n = 1; n <= 9; n++)
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 2.0),
                    child: _buildNumberButton(context, n, counts[n] ?? 0, colors, theme),
                  ),
                ),
            ],
          );
        } else {
          // 2 Rows or 3x3 grid
          return Wrap(
            spacing: 8.0,
            runSpacing: 8.0,
            alignment: WrapAlignment.center,
            children: [
              for (int n = 1; n <= 9; n++)
                SizedBox(
                  width: (constraints.maxWidth - 36) / 5.2,
                  child: _buildNumberButton(context, n, counts[n] ?? 0, colors, theme),
                ),
            ],
          );
        }
      },
    );
  }

  Widget _buildNumberButton(
    BuildContext context,
    int number,
    int placedCount,
    SudokuThemeColors colors,
    ThemeData theme,
  ) {
    final remaining = 9 - placedCount;
    final isCompleted = remaining <= 0;

    return Semantics(
      label: 'Input $number, $remaining remaining',
      button: true,
      child: Material(
        color: isCompleted
            ? colors.keypadButtonBg.withValues(alpha: 0.4)
            : colors.keypadButtonBg,
        borderRadius: BorderRadius.circular(12),
        elevation: isCompleted ? 0 : 1,
        child: InkWell(
          onTap: isCompleted ? null : () => viewModel.inputNumber(number),
          borderRadius: BorderRadius.circular(12),
          child: Container(
            padding: const EdgeInsets.symmetric(vertical: 8),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(12),
              border: Border.all(
                color: colors.gridThin,
                width: 1.0,
              ),
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  '$number',
                  style: TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                    color: isCompleted
                        ? colors.keypadButtonText.withValues(alpha: 0.3)
                        : colors.keypadButtonText,
                  ),
                ),
                const SizedBox(height: 2),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 5, vertical: 1),
                  decoration: BoxDecoration(
                    color: isCompleted
                        ? colors.badgeBg.withValues(alpha: 0.5)
                        : colors.badgeBg,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: isCompleted
                      ? Icon(
                          Icons.check_rounded,
                          size: 11,
                          color: colors.badgeText,
                        )
                      : Text(
                          '$remaining',
                          style: TextStyle(
                            fontSize: 10,
                            fontWeight: FontWeight.w600,
                            color: colors.badgeText,
                          ),
                        ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
