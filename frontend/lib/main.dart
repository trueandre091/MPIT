import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'styles/app_theme.dart';
import 'pages/pages.dart';

void main() {
  runApp(const App());
}

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => ThemeProvider(),
      child: Consumer<ThemeProvider>(
        builder: (context, themeProvider, child) => MaterialApp(
          title: 'Flutter App',
          theme: themeProvider.isDarkMode ? AppThemes.darkTheme : AppThemes.lightTheme,
          home: const HomePage(),
        ),
      ),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int _counter = 0;
  int _selectedIndex = 0;

  List<Widget> get _pages => [
        HomePageContent(counter: _counter, onIncrement: _incrementCounter),
        const ProfilePage(),
        const SettingsPage(),
      ];

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: PreferredSize(
        preferredSize: const Size.fromHeight(100),
        child: Container(
          margin: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
          child: Consumer<ThemeProvider>(
            builder: (context, themeProvider, child) => AppBar(
              titleSpacing: 24,
              leadingWidth: 72,
              title: Text(
                'главная',
                style: Theme.of(context).textTheme.titleLarge,
              ),
              actions: [
                Container(
                  margin: const EdgeInsets.symmetric(horizontal: 25.0),
                  child: IconButton(
                    onPressed: () => themeProvider.toggleTheme(),
                    icon: Icon(themeProvider.isDarkMode ? Icons.dark_mode : Icons.light_mode),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
      body: _pages[_selectedIndex],
      bottomNavigationBar: BottomAppBar(
        shape: const CircularNotchedRectangle(),
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 10),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              IconButton(
                icon: const Icon(Icons.home),
                onPressed: () => setState(() => _selectedIndex = 0),
                color: _selectedIndex == 0 ? Theme.of(context).primaryColor : null,
              ),
              IconButton(
                icon: const Icon(Icons.person),
                onPressed: () => setState(() => _selectedIndex = 1),
                color: _selectedIndex == 1 ? Theme.of(context).primaryColor : null,
              ),
              const SizedBox(width: 40), // пространство для FAB
              IconButton(
                icon: const Icon(Icons.settings),
                onPressed: () => setState(() => _selectedIndex = 2),
                color: _selectedIndex == 2 ? Theme.of(context).primaryColor : null,
              ),
            ],
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        child: const Icon(Icons.add),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerDocked,
    );
  }
}
