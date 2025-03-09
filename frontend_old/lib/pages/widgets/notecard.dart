import 'package:flutter/material.dart';
import '../../../models/note.dart';

class NoteCard extends StatelessWidget {
  final Note note;

  const NoteCard({super.key, required this.note});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Column(
        children: [
          Text(note.title),
          Text(note.text),
        ],
      ),
    );
  }
}
