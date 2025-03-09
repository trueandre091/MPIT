class Note {
  int id;
  String title;
  String text;
  int userId;
  int? plantId;
  DateTime? day;
  DateTime? createdAt;
  DateTime? updatedAt;

  Note({
    required this.id,
    required this.title,
    required this.text,
    required this.userId,
    this.plantId,
    this.day,
    this.createdAt,
    this.updatedAt,
  });

  factory Note.fromJson(Map<String, dynamic> json) {
    return Note(
      id: json['id'],
      title: json['title'],
      text: json['text'],
      userId: json['user_id'],
      plantId: json['plant_id'],
      day: DateTime.parse(json['day']),
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'text': text,
      'user_id': userId,
      'plant_id': plantId,
      'day': day,
      'created_at': createdAt,
      'updated_at': updatedAt,
    };
  }
}
