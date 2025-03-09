import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'home_page.dart';
import 'profile_page.dart';
import '../services/auth_service.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  late AuthService _authService;
  String _error = '';
  bool _isLoading = false;
  bool _isLogin = true;
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _nameController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _initServices();
  }

  Future<void> _initServices() async {
    _authService = await AuthService.create();
  }

  Future<void> _login() async {
    setState(() {
      _isLoading = true;
    });

    try {
      Map<String, dynamic> response;
      if (_isLogin) {
        response = await _authService.login(_emailController.text, _passwordController.text);
      } else {
        response = await _authService.register(_emailController.text, _passwordController.text, _nameController.text);
      }
      if (response['status'] == 200 || response['status'] == 201) {
        Navigator.pushAndRemoveUntil(
          context,
          MaterialPageRoute(builder: (context) => const ProfilePage()),
          (route) => false,
        );
      } else {
        _error = '${response['status']}: ${response['detail']}';
      }
    } catch (e) {
      _error = e.toString();
    } finally {
      setState(() {
        _isLoading = false;
        _clearError();
      });
    }
  }

  Future<void> _clearError() async {
    await Future.delayed(Duration(seconds: 3));
    setState(() {
      _error = '';
    });
  }

  void _toggleMode() {
    setState(() {
      _isLogin = !_isLogin;
      _emailController.clear();
      _passwordController.clear();
      _nameController.clear();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(toolbarHeight: 40),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Expanded(
            flex: 2,
            child: LoginAppBar(),
          ),
          Container(
            decoration: BoxDecoration(
              color: Theme.of(context).primaryColorDark,
              borderRadius: BorderRadius.only(
                topLeft: Radius.circular(50),
                topRight: Radius.circular(50),
              ),
              border: Border(
                top: BorderSide(color: Theme.of(context).primaryColorLight),
              ),
            ),
            padding: const EdgeInsets.symmetric(horizontal: 10),
            child: LoginForm(
              isLogin: _isLogin,
              toggleMode: _toggleMode,
              error: _error,
              isLoading: _isLoading,
              emailController: _emailController,
              passwordController: _passwordController,
              nameController: _nameController,
              login: _login,
            ),
          ),
        ],
      ),
    );
  }
}

class LoginAppBar extends StatelessWidget {
  const LoginAppBar({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(left: 30, right: 30, top: 30, bottom: 0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Flora\nFriend',
            style: GoogleFonts.museoModerno(fontSize: 80, fontWeight: FontWeight.bold, height: 1),
          ),
          IconButton(
              onPressed: () {
                Navigator.pushReplacement(
                  context,
                  MaterialPageRoute(builder: (context) => const HomePage()),
                );
              },
              icon: Icon(
                Icons.home_outlined,
                color: Theme.of(context).primaryColorDark,
                size: 50,
              )),
        ],
      ),
    );
  }
}

class LoginForm extends StatefulWidget {
  const LoginForm(
      {super.key,
      required this.isLogin,
      required this.toggleMode,
      required this.error,
      required this.isLoading,
      required this.emailController,
      required this.passwordController,
      required this.nameController,
      required this.login});

  final bool isLogin;
  final void Function() toggleMode;
  final String error;
  final bool isLoading;
  final TextEditingController emailController;
  final TextEditingController passwordController;
  final TextEditingController nameController;
  final void Function() login;

  @override
  State<LoginForm> createState() => _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {
  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          padding: const EdgeInsets.only(left: 10, right: 10, top: 40, bottom: 30),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text('Вход в аккаунт',
                  style: GoogleFonts.mulish(
                      fontSize: 35,
                      fontWeight: FontWeight.w100,
                      color: Theme.of(context).primaryColorLight,
                      height: 1)),
            ],
          ),
        ),
        Container(
          decoration: BoxDecoration(
            color: Theme.of(context).primaryColorLight,
            borderRadius: BorderRadius.circular(30),
          ),
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
          margin: const EdgeInsets.symmetric(vertical: 10),
          child: TextField(
            style: GoogleFonts.mulish(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: Theme.of(context).primaryColorDark,
            ),
            controller: widget.emailController,
            decoration: InputDecoration(
              hintText: 'введите email...',
              hintStyle: GoogleFonts.mulish(
                fontSize: 20,
                fontWeight: FontWeight.w100,
                color: Colors.grey,
              ),
              prefixIcon: Icon(Icons.mail_outline),
              border: InputBorder.none,
            ),
          ),
        ),
        Container(
          decoration: BoxDecoration(
            color: Theme.of(context).primaryColorLight,
            borderRadius: BorderRadius.circular(30),
          ),
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
          margin: const EdgeInsets.symmetric(vertical: 10),
          child: TextField(
            style: GoogleFonts.mulish(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: Theme.of(context).primaryColorDark,
            ),
            controller: widget.passwordController,
            decoration: InputDecoration(
              hintText: 'введите пароль...',
              hintStyle: GoogleFonts.mulish(
                fontSize: 20,
                fontWeight: FontWeight.w100,
                color: Colors.grey,
              ),
              prefixIcon: Icon(Icons.lock_outline),
              border: InputBorder.none,
            ),
          ),
        ),
        widget.isLogin
            ? Container()
            : Container(
                decoration: BoxDecoration(
                  color: Theme.of(context).primaryColorLight,
                  borderRadius: BorderRadius.circular(30),
                ),
                padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                margin: const EdgeInsets.symmetric(vertical: 10),
                child: TextField(
                  style: GoogleFonts.mulish(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: Theme.of(context).primaryColorDark,
                  ),
                  controller: widget.nameController,
                  decoration: InputDecoration(
                    hintText: 'введите имя...',
                    hintStyle: GoogleFonts.mulish(
                      fontSize: 20,
                      fontWeight: FontWeight.w100,
                      color: Colors.grey,
                    ),
                    prefixIcon: Icon(Icons.person_outline),
                    border: InputBorder.none,
                  ),
                ),
              ),
        Padding(
          padding: const EdgeInsets.symmetric(vertical: 10),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Expanded(
                child: ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Theme.of(context).focusColor,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(30),
                        side: BorderSide(color: Theme.of(context).primaryColorDark),
                      ),
                    ),
                    onPressed: widget.login,
                    child: Padding(
                      padding: const EdgeInsets.symmetric(vertical: 15),
                      child: Text('Далее',
                          style: GoogleFonts.mulish(
                              fontSize: 20, fontWeight: FontWeight.bold, color: Theme.of(context).primaryColorDark)),
                    )),
              ),
              const SizedBox(width: 15),
              Expanded(
                child: ElevatedButton(
                    onPressed: widget.toggleMode,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.transparent,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(30),
                        side: BorderSide(color: Theme.of(context).primaryColorLight),
                      ),
                    ),
                    child: Padding(
                      padding: const EdgeInsets.symmetric(vertical: 15),
                      child: Text(widget.isLogin ? 'Впервые?' : 'Есть аккаунт?',
                          style: GoogleFonts.mulish(
                              fontSize: 20, fontWeight: FontWeight.bold, color: Theme.of(context).primaryColorLight)),
                    )),
              ),
            ],
          ),
        ),
        if (widget.error != 'null')
          Text(widget.error,
              style: GoogleFonts.mulish(
                  fontSize: 20, fontWeight: FontWeight.bold, color: Theme.of(context).primaryColorLight)),
      ],
    );
  }
}
