class Plant {
  final int id;
  final String name;
  final String description;
  final String image;
  final int userId;
  final List<Map<String, dynamic>> notes;
  final String createdAt;
  final String updatedAt;

  Plant(
      {required this.id,
      required this.name,
      required this.description,
      required this.image,
      required this.userId,
      required this.notes,
      required this.createdAt,
      required this.updatedAt});

  factory Plant.fromJson(Map<String, dynamic> json) {
    return Plant(
        id: json['id'],
        name: json['name'],
        description: json['description'],
        image: json['image'],
        userId: json['user_id'],
        notes: json['notes'],
        createdAt: json['created_at'],
        updatedAt: json['updated_at']);
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'image': image,
      'created_at': createdAt,
      'updated_at': updatedAt,
    };
  }
}
