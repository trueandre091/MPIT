import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../widgets/page_title.dart';
import '../models/user.dart';
import '../services/auth_service.dart';
import '../pages/login_page.dart';
import '../pages/home_page.dart';
import '../pages/settings_page.dart';

class ProfilePage extends StatefulWidget {
  const ProfilePage({super.key});

  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  late AuthService _authService;
  User? _user;
  bool _isLoading = false;
  String _error = '';

  @override
  void initState() {
    super.initState();
    initServices();
  }

  Future<void> initServices() async {
    _authService = await AuthService.create();
    await _getUser();
  }

  Future<void> _getUser() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final response = await _authService.me();
      if (response['status'] == 200) {
        setState(() {
          _user = response['user'];
        });
      } else if (response['status'] == 401) {
        await _authService.clearToken();
        if (mounted) {
          Navigator.pushAndRemoveUntil(
            context,
            PageRouteBuilder(
              pageBuilder: (context, animation, secondaryAnimation) => const LoginPage(),
              transitionDuration: Duration.zero,
            ),
            (route) => false,
          );
        }
      }
    } catch (e) {
      setState(() {
        _error = e.toString();
      });
    } finally {
      await Future.delayed(Duration(milliseconds: 500));
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> _logout() async {
    await _authService.logout();
    Navigator.pushAndRemoveUntil(
      context,
      PageRouteBuilder(
        pageBuilder: (context, animation, secondaryAnimation) => const HomePage(),
        transitionDuration: Duration.zero,
      ),
      (route) => false,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(toolbarHeight: 30),
      body: Padding(
        padding: EdgeInsets.symmetric(horizontal: 30),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            PageTitle(title: 'Profile', showHomeButton: true),
            if (!_isLoading && _user != null) ...[
              ProfileForm(user: _user!, logout: _logout),
              if (_error.isNotEmpty) Text(_error),
            ] else if (_isLoading) ...[
              Center(
                child: CircularProgressIndicator(
                  color: Theme.of(context).primaryColorDark,
                ),
              ),
            ] else ...[
              Text('Ошибка загрузки профиля'),
            ],
          ],
        ),
      ),
    );
  }
}

class ProfileForm extends StatefulWidget {
  const ProfileForm({super.key, required this.user, required this.logout});

  final User user;
  final Function logout;

  @override
  State<ProfileForm> createState() => _ProfileFormState();
}

class _ProfileFormState extends State<ProfileForm> {
  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Padding(
        padding: EdgeInsets.symmetric(vertical: 30.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Expanded(
              flex: 2,
              child: Container(
                decoration: BoxDecoration(
                  color: Theme.of(context).canvasColor,
                  borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(30),
                    topRight: Radius.circular(30),
                  ),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    Expanded(
                      flex: 3,
                      child: Container(
                        decoration: BoxDecoration(
                          shape: BoxShape.rectangle,
                          color: Theme.of(context).canvasColor,
                          borderRadius: BorderRadius.only(
                            topLeft: Radius.circular(30),
                            topRight: Radius.circular(30),
                          ),
                        ),
                        child: Padding(
                          padding: EdgeInsets.all(30.0),
                          child: Text(
                            'Добро\nпожаловать,\nпользователь!',
                            style: GoogleFonts.mulish(
                              color: Theme.of(context).primaryColorLight,
                              fontSize: 24,
                              fontWeight: FontWeight.normal,
                            ),
                          ),
                        ),
                      ),
                    ),
                    Expanded(
                      flex: 2,
                      child: Container(
                        margin: EdgeInsets.only(bottom: 10.0),
                        decoration: BoxDecoration(
                          shape: BoxShape.rectangle,
                          color: Theme.of(context).focusColor,
                          borderRadius: BorderRadius.circular(30),
                          border: Border.all(
                            color: Theme.of(context).primaryColorLight,
                            width: 10,
                          ),
                        ),
                        child: Icon(
                          Icons.person,
                          size: 70,
                          color: Theme.of(context).primaryColorLight,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            SizedBox(
              height: 10,
              child: Container(
                color: Theme.of(context).shadowColor,
              ),
            ),
            Expanded(
              flex: 3,
              child: Container(
                decoration: BoxDecoration(
                  color: Theme.of(context).shadowColor,
                  borderRadius: BorderRadius.only(
                    bottomLeft: Radius.circular(30),
                    bottomRight: Radius.circular(30),
                  ),
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.start,
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    ProfileInfo(title: 'имя', value: widget.user.name),
                    ProfileInfo(title: 'email', value: widget.user.email),
                    ProfileInfo(title: 'статус', value: widget.user.role),
                    ProfileInfo(title: 'аккаунт создан', value: '${widget.user.createdAt.toString().substring(0, 10)}'),
                  ],
                ),
              ),
            ),
            Expanded(
              flex: 4,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.start,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Container(
                    margin: EdgeInsets.symmetric(vertical: 20),
                    child: ElevatedButton(
                      onPressed: () {},
                      style: ElevatedButton.styleFrom(
                        elevation: 0,
                        backgroundColor: Theme.of(context).focusColor,
                        foregroundColor: Theme.of(context).primaryColorDark,
                      ),
                      child: Padding(
                        padding: EdgeInsets.symmetric(vertical: 10, horizontal: 30),
                        child: Text('Награды',
                            style: GoogleFonts.mulish(
                                fontSize: 20, fontWeight: FontWeight.bold, color: Theme.of(context).primaryColorDark)),
                      ),
                    ),
                  ),
                  ElevatedButton(
                    onPressed: () {},
                    style: ElevatedButton.styleFrom(
                      elevation: 0,
                      backgroundColor: Theme.of(context).focusColor,
                      foregroundColor: Theme.of(context).primaryColorDark,
                    ),
                    child: Padding(
                      padding: EdgeInsets.symmetric(vertical: 10, horizontal: 30),
                      child: Text('Тесты',
                          style: GoogleFonts.mulish(
                              fontSize: 20, fontWeight: FontWeight.bold, color: Theme.of(context).primaryColorDark)),
                    ),
                  ),
                  Container(
                    margin: EdgeInsets.symmetric(vertical: 20),
                    child: ElevatedButton(
                      onPressed: () => widget.logout(),
                      style: ElevatedButton.styleFrom(
                        elevation: 0,
                        backgroundColor: Theme.of(context).primaryColorLight,
                        foregroundColor: Theme.of(context).primaryColorDark,
                      ),
                      child: Text('Выйти из аккаунта',
                          style: GoogleFonts.mulish(
                              fontSize: 15, fontWeight: FontWeight.normal, color: Theme.of(context).primaryColorDark)),
                    ),
                  ),
                  SizedBox(
                    height: 20,
                  ),
                  Container(
                    margin: EdgeInsets.only(top: 30),
                    child: ElevatedButton(
                      onPressed: () {
                        Navigator.pushAndRemoveUntil(
                          context,
                          PageRouteBuilder(
                            pageBuilder: (context, animation, secondaryAnimation) => const SettingsPage(),
                            transitionDuration: Duration.zero,
                          ),
                          (route) => false,
                        );
                      },
                      style: ButtonStyle(
                        elevation: MaterialStateProperty.all(0),
                        backgroundColor: MaterialStateProperty.all(Colors.transparent),
                        foregroundColor: MaterialStateProperty.all(Theme.of(context).primaryColorDark),
                        shape: MaterialStateProperty.all(RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(15),
                          side: BorderSide(
                            color: Theme.of(context).primaryColorDark,
                            width: 3,
                          ),
                        )),
                      ),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.start,
                        children: [
                          Icon(Icons.settings, size: 20, color: Theme.of(context).primaryColorDark),
                          Container(
                            margin: EdgeInsets.only(left: 10),
                            child: Padding(
                              padding: EdgeInsets.symmetric(vertical: 10),
                              child: Text('Настройки',
                                  style: GoogleFonts.mulish(
                                      fontSize: 22,
                                      fontWeight: FontWeight.bold,
                                      color: Theme.of(context).primaryColorDark)),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class ProfileInfo extends StatefulWidget {
  const ProfileInfo({
    super.key,
    required this.title,
    required this.value,
  });

  final String title;
  final String value;

  @override
  State<ProfileInfo> createState() => _ProfileInfoState();
}

class _ProfileInfoState extends State<ProfileInfo> {
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.symmetric(vertical: 10, horizontal: 30),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text('${widget.title}: ',
              style: GoogleFonts.mulish(
                  fontSize: 20, fontWeight: FontWeight.normal, color: Theme.of(context).primaryColorLight)),
          Text(widget.value,
              style: GoogleFonts.mulish(
                  fontSize: 15, fontWeight: FontWeight.normal, color: Theme.of(context).primaryColorLight)),
        ],
      ),
    );
  }
}
