import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:sudoku_flutter/main.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('SudokuApp smoke test - renders menu screen with difficulties', (WidgetTester tester) async {
    SharedPreferences.setMockInitialValues({});

    // Set viewport size for testing
    tester.view.physicalSize = const Size(1080, 1920);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(() => tester.view.resetPhysicalSize());

    await tester.pumpWidget(const SudokuApp());
    await tester.pumpAndSettle();

    // Verify Title and Difficulty buttons exist
    expect(find.text('Sudoku'), findsOneWidget);
    expect(find.text('Classic Sudoku'), findsOneWidget);
    expect(find.text('Easy'), findsOneWidget);
    expect(find.text('Medium'), findsOneWidget);
    expect(find.text('Hard'), findsOneWidget);
    expect(find.text('Expert'), findsOneWidget);
  });
}
