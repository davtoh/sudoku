import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../view_models/game_view_model.dart';

class KeyboardListenerWrapper extends StatelessWidget {
  final GameViewModel viewModel;
  final Widget child;

  const KeyboardListenerWrapper({
    super.key,
    required this.viewModel,
    required this.child,
  });

  @override
  Widget build(BuildContext context) {
    return Focus(
      autofocus: true,
      onKeyEvent: (node, event) {
        if (event is! KeyDownEvent) return KeyEventResult.ignored;

        // Navigation (Arrow keys or WASD)
        if (event.logicalKey == LogicalKeyboardKey.arrowUp ||
            event.logicalKey == LogicalKeyboardKey.keyW) {
          viewModel.moveSelection(-1, 0);
          return KeyEventResult.handled;
        } else if (event.logicalKey == LogicalKeyboardKey.arrowDown ||
            event.logicalKey == LogicalKeyboardKey.keyS) {
          viewModel.moveSelection(1, 0);
          return KeyEventResult.handled;
        } else if (event.logicalKey == LogicalKeyboardKey.arrowLeft ||
            event.logicalKey == LogicalKeyboardKey.keyA) {
          viewModel.moveSelection(0, -1);
          return KeyEventResult.handled;
        } else if (event.logicalKey == LogicalKeyboardKey.arrowRight ||
            event.logicalKey == LogicalKeyboardKey.keyD) {
          viewModel.moveSelection(0, 1);
          return KeyEventResult.handled;
        }

        // Digits 1-9
        final char = event.character;
        if (char != null && char.length == 1 && '123456789'.contains(char)) {
          final digit = int.tryParse(char);
          if (digit != null) {
            viewModel.inputNumber(digit);
            return KeyEventResult.handled;
          }
        }

        // Erase: Backspace or Delete or '0'
        if (event.logicalKey == LogicalKeyboardKey.backspace ||
            event.logicalKey == LogicalKeyboardKey.delete ||
            event.logicalKey == LogicalKeyboardKey.digit0 ||
            event.logicalKey == LogicalKeyboardKey.numpad0) {
          viewModel.erase();
          return KeyEventResult.handled;
        }

        // Notes Mode: 'N'
        if (event.logicalKey == LogicalKeyboardKey.keyN) {
          viewModel.toggleNotesMode();
          return KeyEventResult.handled;
        }

        // Undo: 'U' or Ctrl+Z / Cmd+Z
        if (event.logicalKey == LogicalKeyboardKey.keyU ||
            ((HardwareKeyboard.instance.isControlPressed ||
                    HardwareKeyboard.instance.isMetaPressed) &&
                event.logicalKey == LogicalKeyboardKey.keyZ)) {
          viewModel.undo();
          return KeyEventResult.handled;
        }

        // Hint: 'H'
        if (event.logicalKey == LogicalKeyboardKey.keyH) {
          viewModel.applyHint();
          return KeyEventResult.handled;
        }

        // Pause/Resume: Space
        if (event.logicalKey == LogicalKeyboardKey.space) {
          viewModel.togglePause();
          return KeyEventResult.handled;
        }

        return KeyEventResult.ignored;
      },
      child: child,
    );
  }
}
