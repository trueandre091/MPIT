import 'package:flutter/material.dart';
import '../widgets/bottom_navigator.dart';
import '../widgets/page_title.dart';

class CalendarPage extends StatefulWidget {
  const CalendarPage({super.key});

  @override
  State<CalendarPage> createState() => _CalendarPageState();
}

class _CalendarPageState extends State<CalendarPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(toolbarHeight: 30),
      body: const Padding(
        padding: EdgeInsets.symmetric(horizontal: 30),
        child: Column(
          children: [
            PageTitle(title: 'Calendar'),
            Text('Calendar'),
          ],
        ),
      ),
      bottomNavigationBar: const BottomNavigator(
        thisIndex: 2,
      ),
    );
  }
}
