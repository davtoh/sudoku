import 'dart:ui';
import 'package:flutter/material.dart';
import '../../../../core/theme/app_theme.dart';
import '../view_models/game_view_model.dart';
import 'cell_widget.dart';

class SudokuBoardWidget extends StatelessWidget {
  final GameViewModel viewModel;

  const SudokuBoardWidget({super.key, required this.viewModel});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colors = theme.extension<SudokuThemeColors>() ?? AppThemes.lightColors;

    final selected = viewModel.selected;
    final selectedValue = selected != null
        ? viewModel.board.getCell(selected.row, selected.col).value
        : 0;

    return Center(
      child: AspectRatio(
        aspectRatio: 1.0,
        child: Container(
          decoration: BoxDecoration(
            color: colors.bgBoard,
            borderRadius: BorderRadius.circular(16.0),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withValues(alpha: 0.08),
                blurRadius: 16.0,
                offset: const Offset(0, 4),
              ),
            ],
            border: Border.all(color: colors.gridThick, width: 2.5),
          ),
          clipBehavior: Clip.antiAlias,
          child: Stack(
            children: [
              // 9x9 Grid layout with 3x3 blocks
              Column(
                children: [
                  for (int br = 0; br < 3; br++) ...[
                    Expanded(
                      child: Row(
                        children: [
                          for (int bc = 0; bc < 3; bc++) ...[
                            Expanded(
                              child: _build3x3Block(
                                blockRow: br,
                                blockCol: bc,
                                selected: selected,
                                selectedValue: selectedValue,
                                colors: colors,
                              ),
                            ),
                            if (bc < 2)
                              Container(
                                width: 2.0,
                                color: colors.gridThick,
                              ),
                          ],
                        ],
                      ),
                    ),
                    if (br < 2)
                      Container(
                        height: 2.0,
                        color: colors.gridThick,
                      ),
                  ],
                ],
              ),

              // Pause Anti-Cheat Overlay
              if (viewModel.isPaused)
                Positioned.fill(
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(14.0),
                    child: BackdropFilter(
                      filter: ImageFilter.blur(sigmaX: 12.0, sigmaY: 12.0),
                      child: Container(
                        color: colors.bgBoard.withValues(alpha: 0.7),
                        child: Center(
                          child: Column(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(
                                Icons.pause_circle_filled_rounded,
                                size: 54,
                                color: theme.colorScheme.primary,
                              ),
                              const SizedBox(height: 12),
                              Text(
                                'Game Paused',
                                style: theme.textTheme.headlineSmall?.copyWith(
                                  fontWeight: FontWeight.bold,
                                  color: colors.cellGiven,
                                ),
                              ),
                              const SizedBox(height: 8),
                              FilledButton.icon(
                                onPressed: viewModel.togglePause,
                                icon: const Icon(Icons.play_arrow_rounded),
                                label: const Text('Resume Play'),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ),
                ),

              // Generating loading indicator
              if (viewModel.isGenerating)
                Positioned.fill(
                  child: Container(
                    color: colors.bgBoard.withValues(alpha: 0.8),
                    child: Center(
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          CircularProgressIndicator(color: theme.colorScheme.primary),
                          const SizedBox(height: 16),
                          Text(
                            'Generating Puzzle...',
                            style: theme.textTheme.titleMedium?.copyWith(
                              fontWeight: FontWeight.w600,
                              color: colors.cellGiven,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _build3x3Block({
    required int blockRow,
    required int blockCol,
    required ({int row, int col})? selected,
    required int selectedValue,
    required SudokuThemeColors colors,
  }) {
    return Column(
      children: [
        for (int r = 0; r < 3; r++) ...[
          Expanded(
            child: Row(
              children: [
                for (int c = 0; c < 3; c++) ...[
                  Expanded(
                    child: Builder(
                      builder: (context) {
                        final cellRow = blockRow * 3 + r;
                        final cellCol = blockCol * 3 + c;
                        final cell = viewModel.board.getCell(cellRow, cellCol);

                        final isSelected = selected != null &&
                            selected.row == cellRow &&
                            selected.col == cellCol;

                        final isRelated = selected != null &&
                            (selected.row == cellRow ||
                                selected.col == cellCol ||
                                (selected.row ~/ 3 == blockRow &&
                                    selected.col ~/ 3 == blockCol));

                        final isSameNumber = selectedValue != 0 &&
                            cell.value == selectedValue &&
                            !isSelected;

                        return CellWidget(
                          cell: cell,
                          isSelected: isSelected,
                          isRelated: isRelated,
                          isSameNumber: isSameNumber,
                          onTap: () => viewModel.selectCell(cellRow, cellCol),
                        );
                      },
                    ),
                  ),
                  if (c < 2)
                    Container(
                      width: 1.0,
                      color: colors.gridThin,
                    ),
                ],
              ],
            ),
          ),
          if (r < 2)
            Container(
              height: 1.0,
              color: colors.gridThin,
            ),
        ],
      ],
    );
  }
}
