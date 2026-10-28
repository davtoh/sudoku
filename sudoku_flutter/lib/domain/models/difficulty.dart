/// Sudoku game difficulty levels and configurations.
enum Difficulty {
  easy('Easy', 32, 'Casual & relaxing with 49 given clues'),
  medium('Medium', 42, 'Balanced challenge with 39 given clues'),
  hard('Hard', 50, 'Demanding logic with 31 given clues'),
  expert('Expert', 56, 'Master level with 25 given clues');

  final String label;
  final int emptiesCount;
  final String description;

  const Difficulty(this.label, this.emptiesCount, this.description);

  int get givenCluesCount => 81 - emptiesCount;

  static Difficulty fromString(String? name) {
    return Difficulty.values.firstWhere(
      (d) => d.name.toLowerCase() == (name ?? '').toLowerCase() ||
             d.label.toLowerCase() == (name ?? '').toLowerCase(),
      orElse: () => Difficulty.medium,
    );
  }
}
