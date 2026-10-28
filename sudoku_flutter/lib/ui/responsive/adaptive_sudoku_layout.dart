import 'package:flutter/material.dart';
import '../../data/storage/game_storage.dart';
import '../features/game/view_models/game_view_model.dart';
import '../features/game/widgets/adaptive_keypad_widget.dart';
import '../features/game/widgets/game_header_widget.dart';
import '../features/game/widgets/sudoku_board_widget.dart';

class AdaptiveSudokuLayout extends StatelessWidget {
  final GameViewModel viewModel;
  final VoidCallback onBackToMenu;
  final VoidCallback onOpenSettings;

  const AdaptiveSudokuLayout({
    super.key,
    required this.viewModel,
    required this.onBackToMenu,
    required this.onOpenSettings,
  });

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final width = constraints.maxWidth;
        final height = constraints.maxHeight;

        bool useSideLayout;
        if (viewModel.keypadPos == KeypadPositionPreference.bottom) {
          useSideLayout = false;
        } else if (viewModel.keypadPos == KeypadPositionPreference.side) {
          useSideLayout = true;
        } else {
          // Auto mode: use side layout if landscape or wide tablet/desktop
          useSideLayout = width >= 720 || (width > height && width >= 540);
        }

        return SafeArea(
          child: Column(
            children: [
              GameHeaderWidget(
                viewModel: viewModel,
                onBackToMenu: onBackToMenu,
                onOpenSettings: onOpenSettings,
              ),
              Expanded(
                child: useSideLayout
                    ? _buildSideLayout(context, width, height)
                    : _buildPortraitLayout(context, width, height),
              ),
            ],
          ),
        );
      },
    );
  }

  // Portrait Layout: Board centered on top, keypad comfortably below
  Widget _buildPortraitLayout(BuildContext context, double width, double height) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
      child: Column(
        children: [
          Expanded(
            flex: 6,
            child: Center(
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 520, maxHeight: 520),
                child: SudokuBoardWidget(viewModel: viewModel),
              ),
            ),
          ),
          const SizedBox(height: 12),
          Expanded(
            flex: 4,
            child: Center(
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 520),
                child: SingleChildScrollView(
                  child: AdaptiveKeypadWidget(viewModel: viewModel),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  // Landscape / Large Screen Layout: Side-by-side
  Widget _buildSideLayout(BuildContext context, double width, double height) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 12.0),
      child: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 1040),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              // Left: Board
              Expanded(
                flex: 5,
                child: Center(
                  child: ConstrainedBox(
                    constraints: const BoxConstraints(maxWidth: 520, maxHeight: 520),
                    child: SudokuBoardWidget(viewModel: viewModel),
                  ),
                ),
              ),
              const SizedBox(width: 32),

              // Right: Controls and Keypad
              Expanded(
                flex: 4,
                child: Center(
                  child: ConstrainedBox(
                    constraints: const BoxConstraints(maxWidth: 420),
                    child: SingleChildScrollView(
                      child: AdaptiveKeypadWidget(viewModel: viewModel),
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
}
