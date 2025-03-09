import 'package:flutter/material.dart';
import 'package:table_calendar/table_calendar.dart';
import '../models/note.dart';
import '../services/auth_service.dart';
import 'general/bottom_navigator.dart';
import 'login_page.dart';
import 'profile_page.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  DateTime _focusedDay = DateTime.now();
  DateTime? _selectedDay;
  late AuthService _authService;
  bool _isAuthenticated = false;

  @override
  void initState() {
    super.initState();
    _initService();
  }

  Future<void> _initService() async {
    _authService = await AuthService.create();
    final isAuthenticated = await _authService.isAuthenticated();
    setState(() {
      _isAuthenticated = isAuthenticated;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).primaryColorLight,
      appBar: AppBar(
        backgroundColor: Theme.of(context).primaryColorLight,
      ),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Expanded(
              flex: 1,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Добро пожаловать в',
                        style: Theme.of(context).textTheme.titleMedium,
                      ),
                      Text(
                        'Flora Friend',
                        style: Theme.of(context).textTheme.titleLarge,
                      ),
                    ],
                  ),
                  Padding(
                    padding: EdgeInsets.only(top: 5.0),
                    child: ElevatedButton(
                      onPressed: () {
                        Navigator.pushAndRemoveUntil(
                          context,
                          MaterialPageRoute(
                            builder: (context) => _isAuthenticated ? const ProfilePage() : const LoginPage(),
                          ),
                          (route) => false,
                        );
                      },
                      style: ElevatedButton.styleFrom(
                        elevation: 0,
                        backgroundColor: Theme.of(context).focusColor,
                        foregroundColor: Theme.of(context).highlightColor,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(20),
                        ),
                      ),
                      child: Padding(
                        padding: EdgeInsets.symmetric(horizontal: 10.0, vertical: 20.0),
                        child: Text(
                          'профиль',
                          style: Theme.of(context).textTheme.labelMedium,
                        ),
                      ),
                    ),
                  )
                ],
              ),
            ),
            Expanded(
              flex: 3,
              child: Container(
                padding: EdgeInsets.symmetric(horizontal: 0.0, vertical: 0.0),
                child: TableCalendar(
                  locale: 'ru_RU',
                  focusedDay: _focusedDay, // День, на котором фокусируется календарь
                  firstDay: DateTime(2020), // Первый доступный день
                  lastDay: DateTime(2030), // Последний доступный день
                  startingDayOfWeek: StartingDayOfWeek.monday,
                  selectedDayPredicate: (day) => isSameDay(_selectedDay, day), // Проверка выбранного дня
                  onDaySelected: (selectedDay, focusedDay) {
                    setState(() {
                      _selectedDay = selectedDay; // Обновляем выбранный день
                      _focusedDay = focusedDay; // Обновляем фокусированный день
                    });
                  },
                  onFormatChanged: (format) {
                    setState(() {}); // Перерисовываем виджет при изменении формата
                  },
                  onPageChanged: (focusedDay) {
                    _focusedDay = focusedDay; // Обновляем фокусированный день при листании
                  },
                  calendarFormat: CalendarFormat.month,
                  rowHeight: 40,
                  daysOfWeekHeight: 30,
                  headerStyle: HeaderStyle(
                    formatButtonVisible: false,
                    titleCentered: true,
                    headerPadding: EdgeInsets.only(top: 5.0),
                    titleTextStyle: TextStyle(fontSize: 20),
                  ),
                  daysOfWeekStyle: DaysOfWeekStyle(
                    weekdayStyle: TextStyle(color: Colors.black),
                    weekendStyle: TextStyle(color: Colors.red),
                  ),
                  calendarStyle: CalendarStyle(
                    isTodayHighlighted: true, // Подсвечивать сегодняшний день
                    selectedDecoration: BoxDecoration(
                      color: Theme.of(context).highlightColor, // Цвет выделения выбранного дня
                      shape: BoxShape.rectangle,
                    ),
                    todayDecoration: BoxDecoration(
                      color: Theme.of(context).primaryColor, // Цвет выделения сегодняшнего дня
                      shape: BoxShape.rectangle,
                    ),
                    defaultDecoration: BoxDecoration(
                      shape: BoxShape.circle, // Форма обычных дней
                    ),
                    weekendDecoration: BoxDecoration(
                      shape: BoxShape.circle, // Форма выходных дней
                    ),
                  ),
                ),
              ),
            ),
            Expanded(
              flex: 2,
              child: Container(
                decoration: BoxDecoration(
                  color: Theme.of(context).cardColor,
                  borderRadius: BorderRadius.circular(20),
                ),
                child: NotesList(
                  selectedDate: _selectedDay ?? _focusedDay,
                  onDateChanged: (newDate) {
                    setState(() {
                      _selectedDay = newDate;
                      _focusedDay = newDate;
                    });
                  },
                ),
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: BottomNavigator(),
    );
  }
}

class NotesList extends StatefulWidget {
  final DateTime selectedDate;
  final Function(DateTime) onDateChanged;

  const NotesList({
    super.key,
    required this.selectedDate,
    required this.onDateChanged,
  });

  @override
  State<NotesList> createState() => _NotesListState();
}

class _NotesListState extends State<NotesList> {
  late AuthService _authService;
  List<Note> notes = [];
  bool isLoading = false;
  String? error;

  @override
  void initState() {
    super.initState();
    _initServices();
  }

  Future<void> _initServices() async {
    _authService = await AuthService.create();
    _loadNotes();
  }

  @override
  void didUpdateWidget(NotesList oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.selectedDate != widget.selectedDate) {
      _loadNotes();
    }
  }

  Future<void> _loadNotes() async {
    setState(() {
      isLoading = true;
      error = null;
    });

    // Имитация загрузки данных
    await Future.delayed(Duration(milliseconds: 500));

    // Демо-данные
    setState(() {
      notes = [
        Note(id: 1, title: 'Демо-заметка 1', text: 'Демо-заметка 1', day: widget.selectedDate, userId: 1, plantId: 1),
        Note(id: 2, title: 'Демо-заметка 2', text: 'Демо-заметка 2', day: widget.selectedDate, userId: 1, plantId: 1),
      ];
      isLoading = false;
    });
  }

  void _changeDate(DateTime newDate) {
    widget.onDateChanged(newDate);
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.fromLTRB(16.0, 5.0, 16.0, 0.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'Заметки',
                style: Theme.of(context).textTheme.titleMedium,
              ),
              IconButton(
                onPressed: () {
                  _changeDate(DateTime.now());
                },
                icon: Icon(Icons.today),
              ),
            ],
          ),
          Expanded(
            child: isLoading
                ? Center(child: CircularProgressIndicator())
                : error != null
                    ? Center(
                        child: Text(
                          error!,
                          style: TextStyle(color: Colors.red),
                        ),
                      )
                    : notes.isEmpty
                        ? Center(
                            child: Text(
                              'Нет заметок на выбранную дату',
                              style: Theme.of(context).textTheme.bodyMedium,
                            ),
                          )
                        : ListView.builder(
                            itemCount: notes.length,
                            itemBuilder: (context, index) {
                              final note = notes[index];
                              return Card(
                                margin: EdgeInsets.symmetric(vertical: 5.0),
                                child: ListTile(
                                  title: Text(note.text),
                                  trailing: IconButton(
                                    icon: Icon(Icons.delete),
                                    onPressed: () {
                                      setState(() {
                                        notes.removeAt(index);
                                      });
                                    },
                                  ),
                                ),
                              );
                            },
                          ),
          ),
        ],
      ),
    );
  }
}
