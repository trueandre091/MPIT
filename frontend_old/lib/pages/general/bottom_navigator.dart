import 'package:flutter/material.dart';
import '../../pages/calendar_page.dart';
import '../../pages/notes_page.dart';
import '../../pages/camera_page.dart';

class BottomNavigator extends StatelessWidget {
  const BottomNavigator({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.symmetric(horizontal: 16.0, vertical: 20.0),
      child: Container(
        decoration: BoxDecoration(
          color: Theme.of(context).cardColor,
          borderRadius: BorderRadius.circular(20),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            // Страница с камерой
            IconButton(
              onPressed: () {
                Navigator.pushReplacement(
                  context,
                  MaterialPageRoute(builder: (context) => CameraPage()),
                );
              },
              icon: Icon(Icons.camera_enhance_outlined),
              style: IconButton.styleFrom(
                foregroundColor: Theme.of(context).focusColor,
                iconSize: 50,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(20),
                ),
              ),
            ),
            // Страница с календарем
            IconButton(
              onPressed: () {
                Navigator.pushReplacement(
                  context,
                  MaterialPageRoute(builder: (context) => const CalendarPage()),
                );
              },
              icon: Icon(Icons.calendar_month_outlined),
              style: IconButton.styleFrom(
                foregroundColor: Theme.of(context).focusColor,
                iconSize: 50,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(20),
                ),
              ),
            ),
            // Страница с растениями
            IconButton(
              onPressed: () {},
              icon: Icon(Icons.eco_outlined),
              style: IconButton.styleFrom(
                foregroundColor: Theme.of(context).focusColor,
                iconSize: 50,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(20),
                ),
              ),
            ),
            // Страница с заметками
            IconButton(
              onPressed: () {
                Navigator.pushReplacement(
                  context,
                  MaterialPageRoute(builder: (context) => NotesPage()),
                );
              },
              icon: Icon(Icons.book_outlined),
              style: IconButton.styleFrom(
                foregroundColor: Theme.of(context).focusColor,
                iconSize: 50,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(20),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
