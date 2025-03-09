import 'package:flutter/material.dart';
import '../widgets/bottom_navigator.dart';
import '../widgets/page_title.dart';

class CameraPage extends StatefulWidget {
  const CameraPage({super.key});

  @override
  State<CameraPage> createState() => _CameraPageState();
}

class _CameraPageState extends State<CameraPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(toolbarHeight: 30),
      body: const Padding(
        padding: EdgeInsets.symmetric(horizontal: 30),
        child: Column(
          children: [
            PageTitle(title: 'Camera'),
            Text('Camera'),
          ],
        ),
      ),
      bottomNavigationBar: BottomNavigator(
        thisIndex: 1,
      ),
    );
  }
}
