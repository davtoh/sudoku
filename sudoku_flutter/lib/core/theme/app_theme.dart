import 'package:flutter/material.dart';

enum AppThemeMode {
  light('Light', Icons.light_mode_outlined),
  dark('Dark', Icons.dark_mode_outlined),
  sepia('Warm Sepia', Icons.menu_book_outlined),
  oled('OLED Black', Icons.brightness_2_outlined);

  final String label;
  final IconData icon;
  const AppThemeMode(this.label, this.icon);
}

/// Custom semantic colors for the Sudoku grid, cells, and highlights.
class SudokuThemeColors extends ThemeExtension<SudokuThemeColors> {
  final Color bgBoard;
  final Color bgCard;
  final Color gridThin;
  final Color gridThick;
  final Color cellGiven;
  final Color cellUser;
  final Color cellError;
  final Color cellNote;
  final Color highlightSelected;
  final Color highlightRelated;
  final Color highlightSameNumber;
  final Color highlightError;
  final Color keypadButtonBg;
  final Color keypadButtonText;
  final Color badgeBg;
  final Color badgeText;

  const SudokuThemeColors({
    required this.bgBoard,
    required this.bgCard,
    required this.gridThin,
    required this.gridThick,
    required this.cellGiven,
    required this.cellUser,
    required this.cellError,
    required this.cellNote,
    required this.highlightSelected,
    required this.highlightRelated,
    required this.highlightSameNumber,
    required this.highlightError,
    required this.keypadButtonBg,
    required this.keypadButtonText,
    required this.badgeBg,
    required this.badgeText,
  });

  @override
  SudokuThemeColors copyWith({
    Color? bgBoard,
    Color? bgCard,
    Color? gridThin,
    Color? gridThick,
    Color? cellGiven,
    Color? cellUser,
    Color? cellError,
    Color? cellNote,
    Color? highlightSelected,
    Color? highlightRelated,
    Color? highlightSameNumber,
    Color? highlightError,
    Color? keypadButtonBg,
    Color? keypadButtonText,
    Color? badgeBg,
    Color? badgeText,
  }) {
    return SudokuThemeColors(
      bgBoard: bgBoard ?? this.bgBoard,
      bgCard: bgCard ?? this.bgCard,
      gridThin: gridThin ?? this.gridThin,
      gridThick: gridThick ?? this.gridThick,
      cellGiven: cellGiven ?? this.cellGiven,
      cellUser: cellUser ?? this.cellUser,
      cellError: cellError ?? this.cellError,
      cellNote: cellNote ?? this.cellNote,
      highlightSelected: highlightSelected ?? this.highlightSelected,
      highlightRelated: highlightRelated ?? this.highlightRelated,
      highlightSameNumber: highlightSameNumber ?? this.highlightSameNumber,
      highlightError: highlightError ?? this.highlightError,
      keypadButtonBg: keypadButtonBg ?? this.keypadButtonBg,
      keypadButtonText: keypadButtonText ?? this.keypadButtonText,
      badgeBg: badgeBg ?? this.badgeBg,
      badgeText: badgeText ?? this.badgeText,
    );
  }

  @override
  SudokuThemeColors lerp(ThemeExtension<SudokuThemeColors>? other, double t) {
    if (other is! SudokuThemeColors) return this;
    return SudokuThemeColors(
      bgBoard: Color.lerp(bgBoard, other.bgBoard, t)!,
      bgCard: Color.lerp(bgCard, other.bgCard, t)!,
      gridThin: Color.lerp(gridThin, other.gridThin, t)!,
      gridThick: Color.lerp(gridThick, other.gridThick, t)!,
      cellGiven: Color.lerp(cellGiven, other.cellGiven, t)!,
      cellUser: Color.lerp(cellUser, other.cellUser, t)!,
      cellError: Color.lerp(cellError, other.cellError, t)!,
      cellNote: Color.lerp(cellNote, other.cellNote, t)!,
      highlightSelected: Color.lerp(highlightSelected, other.highlightSelected, t)!,
      highlightRelated: Color.lerp(highlightRelated, other.highlightRelated, t)!,
      highlightSameNumber: Color.lerp(highlightSameNumber, other.highlightSameNumber, t)!,
      highlightError: Color.lerp(highlightError, other.highlightError, t)!,
      keypadButtonBg: Color.lerp(keypadButtonBg, other.keypadButtonBg, t)!,
      keypadButtonText: Color.lerp(keypadButtonText, other.keypadButtonText, t)!,
      badgeBg: Color.lerp(badgeBg, other.badgeBg, t)!,
      badgeText: Color.lerp(badgeText, other.badgeText, t)!,
    );
  }
}

class AppThemes {
  // LIGHT THEME (Faithful to Python Light Theme with refined M3 elevation)
  static final lightColors = SudokuThemeColors(
    bgBoard: Colors.white,
    bgCard: const Color(0xFFF8FAFC),
    gridThin: const Color(0xFFE2E8F0),
    gridThick: const Color(0xFF334155),
    cellGiven: const Color(0xFF0F172A),
    cellUser: const Color(0xFF2563EB), // Vibrant blue
    cellError: const Color(0xFFDC2626), // Error red
    cellNote: const Color(0xFF64748B), // Slate note
    highlightSelected: const Color(0x3D3B82F6),
    highlightRelated: const Color(0x1F3B82F6),
    highlightSameNumber: const Color(0x3860A5FA),
    highlightError: const Color(0x3DDC2626),
    keypadButtonBg: const Color(0xFFF1F5F9),
    keypadButtonText: const Color(0xFF0F172A),
    badgeBg: const Color(0xFFE2E8F0),
    badgeText: const Color(0xFF475569),
  );

  static final light = ThemeData(
    useMaterial3: true,
    brightness: Brightness.light,
    scaffoldBackgroundColor: const Color(0xFFF1F5F9),
    colorScheme: ColorScheme.fromSeed(
      seedColor: const Color(0xFF2563EB),
      brightness: Brightness.light,
      surface: const Color(0xFFF8FAFC),
    ),
    extensions: [lightColors],
  );

  // DARK THEME (Faithful to Python Dark Theme)
  static final darkColors = SudokuThemeColors(
    bgBoard: const Color(0xFF1E293B),
    bgCard: const Color(0xFF1E293B),
    gridThin: const Color(0xFF334155),
    gridThick: const Color(0xFF94A3B8),
    cellGiven: const Color(0xFFF8FAFC),
    cellUser: const Color(0xFF60A5FA), // Light blue
    cellError: const Color(0xFFF87171), // Vibrant coral red
    cellNote: const Color(0xFF94A3B8),
    highlightSelected: const Color(0x523B82F6),
    highlightRelated: const Color(0x2E2563EB),
    highlightSameNumber: const Color(0x4760A5FA),
    highlightError: const Color(0x47EF4444),
    keypadButtonBg: const Color(0xFF334155),
    keypadButtonText: const Color(0xFFF8FAFC),
    badgeBg: const Color(0xFF1E293B),
    badgeText: const Color(0xFFCBD5E1),
  );

  static final dark = ThemeData(
    useMaterial3: true,
    brightness: Brightness.dark,
    scaffoldBackgroundColor: const Color(0xFF0F172A),
    colorScheme: ColorScheme.fromSeed(
      seedColor: const Color(0xFF3B82F6),
      brightness: Brightness.dark,
      surface: const Color(0xFF1E293B),
    ),
    extensions: [darkColors],
  );

  // WARM SEPIA THEME (Reading / Book comfort)
  static final sepiaColors = SudokuThemeColors(
    bgBoard: const Color(0xFFFAF6EE),
    bgCard: const Color(0xFFF4ECE1),
    gridThin: const Color(0xFFE5D9C8),
    gridThick: const Color(0xFF5D4037),
    cellGiven: const Color(0xFF3E2723),
    cellUser: const Color(0xFF8D5B4C),
    cellError: const Color(0xFFC62828),
    cellNote: const Color(0xFF8D6E63),
    highlightSelected: const Color(0x42BCAAA4),
    highlightRelated: const Color(0x22D7CCC8),
    highlightSameNumber: const Color(0x42FFE082),
    highlightError: const Color(0x3DC62828),
    keypadButtonBg: const Color(0xFFEFE6D8),
    keypadButtonText: const Color(0xFF3E2723),
    badgeBg: const Color(0xFFDFD4C4),
    badgeText: const Color(0xFF6D4C41),
  );

  static final sepia = ThemeData(
    useMaterial3: true,
    brightness: Brightness.light,
    scaffoldBackgroundColor: const Color(0xFFF4EDE4),
    colorScheme: ColorScheme.fromSeed(
      seedColor: const Color(0xFF8D5B4C),
      brightness: Brightness.light,
      surface: const Color(0xFFFAF6EE),
    ),
    extensions: [sepiaColors],
  );

  // OLED BLACK THEME (Max contrast & AMOLED battery saving)
  static final oledColors = SudokuThemeColors(
    bgBoard: Colors.black,
    bgCard: const Color(0xFF121212),
    gridThin: const Color(0xFF27272A),
    gridThick: const Color(0xFFA1A1AA),
    cellGiven: Colors.white,
    cellUser: const Color(0xFF38BDF8),
    cellError: const Color(0xFFFB7185),
    cellNote: const Color(0xFF71717A),
    highlightSelected: const Color(0x660284C7),
    highlightRelated: const Color(0x330284C7),
    highlightSameNumber: const Color(0x5538BDF8),
    highlightError: const Color(0x55E11D48),
    keypadButtonBg: const Color(0xFF18181B),
    keypadButtonText: Colors.white,
    badgeBg: const Color(0xFF27272A),
    badgeText: const Color(0xFFA1A1AA),
  );

  static final oled = ThemeData(
    useMaterial3: true,
    brightness: Brightness.dark,
    scaffoldBackgroundColor: Colors.black,
    colorScheme: ColorScheme.fromSeed(
      seedColor: const Color(0xFF38BDF8),
      brightness: Brightness.dark,
      surface: const Color(0xFF121212),
    ),
    extensions: [oledColors],
  );

  static ThemeData getTheme(AppThemeMode mode) {
    switch (mode) {
      case AppThemeMode.light:
        return light;
      case AppThemeMode.dark:
        return dark;
      case AppThemeMode.sepia:
        return sepia;
      case AppThemeMode.oled:
        return oled;
    }
  }
}
