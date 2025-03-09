import 'package:flutter/material.dart';
import '../pages/home_page.dart';
import 'package:google_fonts/google_fonts.dart';

class PageTitle extends StatelessWidget {
  final String title;
  final bool showHomeButton;

  const PageTitle({super.key, required this.title, this.showHomeButton = true});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 0),
      child: Container(
        height: 50,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Expanded(
              flex: 10,
              child: Align(
                alignment: Alignment.bottomLeft,
                child: Text(
                  title,
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
            if (showHomeButton)
              Expanded(
                flex: 3,
                child: Align(
                  alignment: Alignment.bottomCenter,
                  child: IconButton(
                    onPressed: () {
                      Navigator.pushAndRemoveUntil(
                        context,
                        PageRouteBuilder(
                          pageBuilder: (context, animation, secondaryAnimation) => const HomePage(),
                          transitionDuration: Duration.zero,
                        ),
                        (route) => false,
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
      ),
    );
  }
}
