import 'package:flutter/material.dart';
import '../widgets/bottom_navigator.dart';
import '../widgets/page_title.dart';

class PlantsPage extends StatefulWidget {
  const PlantsPage({super.key});

  @override
  State<PlantsPage> createState() => _PlantsPageState();
}

class _PlantsPageState extends State<PlantsPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(toolbarHeight: 30),
      body: const Padding(
        padding: EdgeInsets.symmetric(horizontal: 30),
        child: Column(
          children: [
            PageTitle(title: 'Растения'),
            Text('Растения'),
          ],
        ),
      ),
      bottomNavigationBar: BottomNavigator(
        thisIndex: 3,
      ),
    );
  }
}
