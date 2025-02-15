import 'package:flutter/material.dart';

class HomePageContent extends StatelessWidget {
  final int counter;
  final VoidCallback onIncrement;

  const HomePageContent({
    super.key,
    required this.counter,
    required this.onIncrement,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          Text('счётчик:', style: Theme.of(context).textTheme.bodyMedium),
          Text(
            '$counter',
            style: Theme.of(context).textTheme.bodyLarge,
          ),
        ],
      ),
    );
  }
}

class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Text('профиль', style: Theme.of(context).textTheme.bodyMedium),
    );
  }
}

class AddPage extends StatelessWidget {
  const AddPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Text('добавить', style: Theme.of(context).textTheme.bodyMedium),
    );
  }
}

class SettingsPage extends StatelessWidget {
  const SettingsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Text('календарь', style: Theme.of(context).textTheme.bodyMedium),
    );
  }
}
