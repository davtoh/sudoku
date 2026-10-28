/// Records a single move or note alteration for undo/redo functionality.
class MoveRecord {
  final int row;
  final int col;
  final int prevValue;
  final int newValue;
  final Set<int> prevNotes;
  final Set<int> newNotes;
  final bool wasNote;

  const MoveRecord({
    required this.row,
    required this.col,
    required this.prevValue,
    required this.newValue,
    required this.prevNotes,
    required this.newNotes,
    required this.wasNote,
  });

  Map<String, dynamic> toJson() => {
    'row': row,
    'col': col,
    'prevValue': prevValue,
    'newValue': newValue,
    'prevNotes': prevNotes.toList(),
    'newNotes': newNotes.toList(),
    'wasNote': wasNote,
  };

  factory MoveRecord.fromJson(Map<String, dynamic> json) => MoveRecord(
    row: json['row'] as int,
    col: json['col'] as int,
    prevValue: json['prevValue'] as int,
    newValue: json['newValue'] as int,
    prevNotes: (json['prevNotes'] as List<dynamic>).map((e) => e as int).toSet(),
    newNotes: (json['newNotes'] as List<dynamic>).map((e) => e as int).toSet(),
    wasNote: json['wasNote'] as bool,
  );
}
