class Note {
  final int id;
  final String title;
  final String text;
  final int userId;
  final int plantId;
  final DateTime day;

  Note({
    required this.id,
    required this.title,
    required this.text,
    required this.userId,
    required this.plantId,
    required this.day,
  });

  factory Note.fromJson(Map<String, dynamic> json) {
    return Note(
      id: json['id'],
      title: json['title'],
      text: json['text'],
      userId: json['user_id'],
      plantId: json['plant_id'],
      day: DateTime.parse(json['day']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'text': text,
      'user_id': userId,
      'plant_id': plantId,
      'day': day.toIso8601String(),
    };
  }
}
