import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../pages/profile_page.dart';
import '../pages/home_page.dart';

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        toolbarHeight: 30,
      ),
      body: const Padding(
        padding: EdgeInsets.symmetric(horizontal: 30),
        child: Column(
          children: [
            SettingsAppBar(),
            SettingsList(),
          ],
        ),
      ),
    );
  }
}

class SettingsAppBar extends StatelessWidget {
  const SettingsAppBar({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 50,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Expanded(
              flex: 3,
              child: IconButton(
                  onPressed: () {
                    Navigator.pushAndRemoveUntil(
                      context,
                      PageRouteBuilder(
                        pageBuilder: (context, animation, secondaryAnimation) => const ProfilePage(),
                        transitionDuration: Duration.zero,
                      ),
                      (route) => false,
                    );
                  },
                  icon: Icon(Icons.person_outline, size: 40, color: Theme.of(context).primaryColorDark))),
          Expanded(
            flex: 7,
            child: Align(
              alignment: Alignment.bottomCenter,
              child: Text(
                'Settings',
                style: GoogleFonts.mulish(
                  textStyle: TextStyle(
                    fontSize: 32,
                    fontWeight: FontWeight.normal,
                    color: Theme.of(context).primaryColorDark,
                  ),
                ),
              ),
            ),
          ),
          Expanded(
            flex: 3,
            child: Align(
              alignment: Alignment.bottomCenter,
              child: IconButton(
                onPressed: () {
                  Navigator.pushReplacement(
                    context,
                    MaterialPageRoute(builder: (context) => const HomePage()),
                  );
                },
                icon: Icon(
                  Icons.home_outlined,
                  size: 45,
                  color: Theme.of(context).primaryColorDark,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class SettingsList extends StatefulWidget {
  const SettingsList({super.key});

  @override
  State<SettingsList> createState() => _SettingsListState();
}

class _SettingsListState extends State<SettingsList> {
  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Container(
            decoration: BoxDecoration(
              color: Theme.of(context).shadowColor,
              borderRadius: BorderRadius.circular(15),
            ),
            child: Padding(
              padding: EdgeInsets.symmetric(horizontal: 30, vertical: 40),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.start,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Container(
                    padding: EdgeInsets.only(bottom: 20),
                    child: Text(
                      'Обратиться в поддержку:',
                      style: GoogleFonts.mulish(
                          fontSize: 20, fontWeight: FontWeight.normal, color: Theme.of(context).primaryColorLight),
                    ),
                  ),
                  Container(
                    margin: EdgeInsets.only(bottom: 20),
                    child: ElevatedButton(
                      onPressed: () {},
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Theme.of(context).focusColor,
                      ),
                      child: Padding(
                        padding: EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                        child: Text(
                          'Почта',
                          style: GoogleFonts.mulish(
                              fontSize: 20, fontWeight: FontWeight.bold, color: Theme.of(context).primaryColorDark),
                        ),
                      ),
                    ),
                  ),
                  Container(
                    child: ElevatedButton(
                      onPressed: () {},
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Theme.of(context).focusColor,
                      ),
                      child: Padding(
                        padding: EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                        child: Text(
                          'Наша нейросеть',
                          style: GoogleFonts.mulish(
                              fontSize: 20, fontWeight: FontWeight.bold, color: Theme.of(context).primaryColorDark),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
