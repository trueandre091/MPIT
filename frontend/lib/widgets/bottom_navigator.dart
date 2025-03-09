import 'package:flutter/material.dart';
import '../pages/home_page.dart';
import '../pages/camera_page.dart';
import '../pages/calendar_page.dart';
import '../pages/profile_page.dart';
import '../pages/plants_page.dart';
import '../pages/notes_page.dart';

class BottomNavigator extends StatefulWidget {
  const BottomNavigator({
    super.key,
    required this.thisIndex,
  });

  final int thisIndex;

  @override
  State<BottomNavigator> createState() => _BottomNavigatorState();
}

class _BottomNavigatorState extends State<BottomNavigator> {
  final List<Widget> _pages = [
    const HomePage(),
    const CameraPage(),
    const CalendarPage(),
    const PlantsPage(),
    const NotesPage(),
    const ProfilePage(),
  ];

  void goToPage(int index) {
    Navigator.pushAndRemoveUntil(
      context,
      PageRouteBuilder(
        pageBuilder: (context, animation, secondaryAnimation) => _pages[index],
        transitionDuration: Duration.zero,
      ),
      (route) => false,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 20, horizontal: 16),
      child: Container(
        decoration: BoxDecoration(
          color: Theme.of(context).primaryColorDark,
          borderRadius: BorderRadius.circular(25),
          boxShadow: [
            BoxShadow(
              color: Theme.of(context).shadowColor.withOpacity(0.1),
              blurRadius: 10,
              offset: const Offset(0, 5),
            ),
          ],
        ),
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 5),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              IconButton(
                  onPressed: () {
                    goToPage(1);
                  },
                  icon: Icon(
                    Icons.camera_alt_outlined,
                    size: 40,
                    color: widget.thisIndex == 1 ? Theme.of(context).highlightColor : Theme.of(context).focusColor,
                  )),
              IconButton(
                  onPressed: () {
                    goToPage(2);
                  },
                  icon: Icon(
                    Icons.calendar_month,
                    size: 40,
                    color: widget.thisIndex == 2 ? Theme.of(context).highlightColor : Theme.of(context).focusColor,
                  )),
              IconButton(
                  onPressed: () {
                    goToPage(3);
                  },
                  icon: Icon(
                    Icons.local_florist,
                    size: 40,
                    color: widget.thisIndex == 3 ? Theme.of(context).highlightColor : Theme.of(context).focusColor,
                  )),
              IconButton(
                  onPressed: () {
                    goToPage(4);
                  },
                  icon: Icon(
                    Icons.book_outlined,
                    size: 40,
                    color: widget.thisIndex == 4 ? Theme.of(context).highlightColor : Theme.of(context).focusColor,
                  )),
            ],
          ),
        ),
      ),
    );
  }
}
