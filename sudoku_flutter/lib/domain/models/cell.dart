/// Model representing a single cell in the 9x9 Sudoku grid.
class Cell {
  final int row;
  final int col;
  int solutionValue;
  int value;
  bool isGiven;
  bool isError;
  Set<int> notes;

  Cell({
    required this.row,
    required this.col,
    this.solutionValue = 0,
    this.value = 0,
    this.isGiven = false,
    this.isError = false,
    Set<int>? notes,
  }) : notes = notes != null ? Set<int>.from(notes) : <int>{};

  /// Sets the cell's value. Pre-filled given cells cannot be modified.
  bool setValue(int newVal) {
    if (isGiven) return false;
    if (newVal < 0 || newVal > 9) return false;
    value = newVal;
    if (newVal != 0) {
      notes.clear();
      isError = false;
    }
    return true;
  }

  /// Clears the value and notes of the cell if not given.
  bool clear() {
    if (isGiven) return false;
    value = 0;
    notes.clear();
    isError = false;
    return true;
  }

  /// Toggles a candidate pencil note (1-9).
  bool toggleNote(int noteDigit) {
    if (isGiven || value != 0) return false;
    if (noteDigit >= 1 && noteDigit <= 9) {
      if (notes.contains(noteDigit)) {
        notes.remove(noteDigit);
      } else {
        notes.add(noteDigit);
      }
      return true;
    }
    return false;
  }

  /// Clears all pencil notes.
  void clearNotes() {
    notes.clear();
  }

  bool get isFilled => value != 0;

  bool get isCorrect => value == solutionValue;

  /// Resets to initial puzzle state.
  void resetToInitial() {
    if (!isGiven) {
      value = 0;
      notes.clear();
      isError = false;
    }
  }

  /// Creates a deep copy of this cell.
  Cell copyWith({
    int? row,
    int? col,
    int? solutionValue,
    int? value,
    bool? isGiven,
    bool? isError,
    Set<int>? notes,
  }) {
    return Cell(
      row: row ?? this.row,
      col: col ?? this.col,
      solutionValue: solutionValue ?? this.solutionValue,
      value: value ?? this.value,
      isGiven: isGiven ?? this.isGiven,
      isError: isError ?? this.isError,
      notes: notes != null ? Set<int>.from(notes) : Set<int>.from(this.notes),
    );
  }

  /// Accessible description for Screen Readers (TalkBack / VoiceOver)
  String get accessibilityLabel {
    final pos = 'Row ${row + 1}, Column ${col + 1}';
    if (isGiven) {
      return '$pos: Given number $value';
    } else if (value != 0) {
      final status = isError ? ', conflict detected' : '';
      return '$pos: Number $value$status';
    } else if (notes.isNotEmpty) {
      final sortedNotes = notes.toList()..sort();
      return '$pos: Empty cell with notes ${sortedNotes.join(", ")}';
    } else {
      return '$pos: Empty cell';
    }
  }

  Map<String, dynamic> toJson() => {
    'row': row,
    'col': col,
    'solutionValue': solutionValue,
    'value': value,
    'isGiven': isGiven,
    'isError': isError,
    'notes': notes.toList(),
  };

  factory Cell.fromJson(Map<String, dynamic> json) => Cell(
    row: json['row'] as int,
    col: json['col'] as int,
    solutionValue: json['solutionValue'] as int? ?? 0,
    value: json['value'] as int? ?? 0,
    isGiven: json['isGiven'] as bool? ?? false,
    isError: json['isError'] as bool? ?? false,
    notes: (json['notes'] as List<dynamic>?)?.map((e) => e as int).toSet() ?? <int>{},
  );
}
