import 'package:flutter/material.dart';
import '../../../../core/theme/app_theme.dart';
import '../../../../domain/models/cell.dart';

class CellWidget extends StatelessWidget {
  final Cell cell;
  final bool isSelected;
  final bool isRelated;
  final bool isSameNumber;
  final VoidCallback onTap;

  const CellWidget({
    super.key,
    required this.cell,
    required this.isSelected,
    required this.isRelated,
    required this.isSameNumber,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colors = theme.extension<SudokuThemeColors>() ?? AppThemes.lightColors;

    // Background highlight color determination
    Color bgColor = colors.bgBoard;
    if (cell.isError) {
      bgColor = colors.highlightError;
    } else if (isSelected) {
      bgColor = colors.highlightSelected;
    } else if (isSameNumber) {
      bgColor = colors.highlightSameNumber;
    } else if (isRelated) {
      bgColor = colors.highlightRelated;
    }

    // Text color
    Color textColor;
    if (cell.isError) {
      textColor = colors.cellError;
    } else if (cell.isGiven) {
      textColor = colors.cellGiven;
    } else {
      textColor = colors.cellUser;
    }

    return Semantics(
      label: cell.accessibilityLabel,
      button: true,
      selected: isSelected,
      child: GestureDetector(
        onTap: onTap,
        behavior: HitTestBehavior.opaque,
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 140),
          decoration: BoxDecoration(
            color: bgColor,
            border: isSelected
                ? Border.all(color: theme.colorScheme.primary, width: 2.0)
                : null,
          ),
          child: Center(
            child: cell.value != 0
                ? AnimatedScale(
                    scale: 1.0,
                    duration: const Duration(milliseconds: 120),
                    child: Text(
                      '${cell.value}',
                      style: TextStyle(
                        fontSize: 26,
                        fontWeight: cell.isGiven ? FontWeight.bold : FontWeight.w600,
                        color: textColor,
                      ),
                    ),
                  )
                : _buildNotesGrid(colors),
          ),
        ),
      ),
    );
  }

  Widget _buildNotesGrid(SudokuThemeColors colors) {
    if (cell.notes.isEmpty) return const SizedBox.shrink();

    return Padding(
      padding: const EdgeInsets.all(2.0),
      child: LayoutBuilder(
        builder: (context, constraints) {
          final noteFontSize = (constraints.maxHeight / 3.6).clamp(8.0, 13.0);
          return Column(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              for (int r = 0; r < 3; r++)
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    for (int c = 0; c < 3; c++)
                      _buildSingleNote(r * 3 + c + 1, colors.cellNote, noteFontSize),
                  ],
                ),
            ],
          );
        },
      ),
    );
  }

  Widget _buildSingleNote(int digit, Color color, double fontSize) {
    final hasNote = cell.notes.contains(digit);
    return SizedBox(
      width: fontSize * 1.2,
      height: fontSize * 1.2,
      child: Center(
        child: hasNote
            ? Text(
                '$digit',
                style: TextStyle(
                  fontSize: fontSize,
                  fontWeight: FontWeight.w600,
                  color: color,
                  height: 1.0,
                ),
              )
            : const SizedBox.shrink(),
      ),
    );
  }
}
