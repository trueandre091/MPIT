import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:table_calendar/table_calendar.dart';
import '../widgets/bottom_navigator.dart';
import 'login_page.dart';
import 'profile_page.dart';
import '../models/note.dart';
import '../services/auth_service.dart';
import '../services/note_service.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  DateTime _selectedDay = DateTime.now();
  void _onDayChanged(DateTime day) {
    setState(() {
      _selectedDay = day;
      _updateSelectedDayNotes();
    });
  }

  late AuthService _authService;
  late NoteService _noteService;
  List<Note> notes = [];
  List<Note> _selectedDayNotes = [];
  bool _isLoading = false;
  String _error = '';
  bool _isAuthenticated = false;

  @override
  void initState() {
    super.initState();
    _initServicesAndLoadNotes();
  }

  Future<void> _initServicesAndLoadNotes() async {
    setState(() {
      _isLoading = true;
    });

    try {
      _authService = await AuthService.create();
      _noteService = NoteService(_authService);
      _isAuthenticated = await _authService.isAuthenticated();
      _isAuthenticated ? await _loadNotes() : _error = "Не авторизован";
    } catch (e) {
      _error = e.toString();
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> _loadNotes() async {
    try {
      notes = await _noteService.getNotes();
      _updateSelectedDayNotes();
    } catch (e) {
      _error = e.toString();
    }
  }

  void _updateSelectedDayNotes() {
    setState(() {
      _selectedDayNotes = notes.where((note) => isSameDay(_selectedDay, note.day)).toList();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(toolbarHeight: 40),
      body: Padding(
        padding: EdgeInsets.symmetric(horizontal: 20),
        child: Column(
          children: [
            HomeAppBar(isAuthenticated: _isAuthenticated),
            HomeCalendar(
              selectedDay: _selectedDay,
              onDayChanged: _onDayChanged,
              notes: notes, // Передаем все заметки в календарь
            ),
            HomeNotes(
                selectedDay: _selectedDay,
                onDayChanged: _onDayChanged,
                notes: _selectedDayNotes,
                isLoading: _isLoading,
                error: _error),
          ],
        ),
      ),
      bottomNavigationBar: const BottomNavigator(
        thisIndex: 0,
      ),
    );
  }
}

class HomeAppBar extends StatefulWidget {
  const HomeAppBar({super.key, required this.isAuthenticated});
  final bool isAuthenticated;

  @override
  State<HomeAppBar> createState() => _HomeAppBarState();
}

class _HomeAppBarState extends State<HomeAppBar> {
  @override
  Widget build(BuildContext context) {
    return Container(
      height: 100,
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.center,
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Добро пожаловать в',
                style: GoogleFonts.mulish(
                  textStyle: TextStyle(
                    fontSize: 23,
                    fontWeight: FontWeight.normal,
                    height: 1.3,
                    color: Theme.of(context).primaryColorDark,
                  ),
                ),
              ),
              Text(
                'Flora Friend',
                style: GoogleFonts.museoModerno(
                  textStyle: TextStyle(
                    fontSize: 43,
                    fontWeight: FontWeight.bold,
                    color: Theme.of(context).primaryColorDark,
                    height: 1.3,
                  ),
                ),
              ),
            ],
          ),
          ElevatedButton(
            onPressed: () async {
              if (widget.isAuthenticated) {
                Navigator.pushAndRemoveUntil(
                  context,
                  PageRouteBuilder(
                    pageBuilder: (context, animation, secondaryAnimation) => const ProfilePage(),
                    transitionDuration: Duration.zero,
                  ),
                  (route) => false,
                );
              } else {
                Navigator.pushAndRemoveUntil(
                  context,
                  PageRouteBuilder(
                    pageBuilder: (context, animation, secondaryAnimation) => const LoginPage(),
                    transitionDuration: Duration.zero,
                  ),
                  (route) => false,
                );
              }
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: Theme.of(context).focusColor,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(30),
              ),
              elevation: 0,
            ),
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 2, vertical: 13),
              child: Text(
                'профиль',
                style: GoogleFonts.mulish(
                  textStyle: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.normal,
                    color: Theme.of(context).primaryColorDark,
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class HomeCalendar extends StatefulWidget {
  const HomeCalendar({
    super.key,
    required this.selectedDay,
    required this.onDayChanged,
    required this.notes,
  });

  final DateTime selectedDay;
  final Function(DateTime) onDayChanged;
  final List<Note> notes; // Список всех заметок

  @override
  State<HomeCalendar> createState() => _HomeCalendarState();
}

class _HomeCalendarState extends State<HomeCalendar> {
  DateTime _focusedDay = DateTime.now();

  List<Note> _getEventsForDay(DateTime day) {
    return widget.notes.where((note) => note.day != null && isSameDay(note.day!, day)).toList();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 20),
      child: TableCalendar(
        locale: 'ru_RU',
        focusedDay: _focusedDay,
        firstDay: DateTime(2020),
        lastDay: DateTime(2030),
        startingDayOfWeek: StartingDayOfWeek.monday,
        selectedDayPredicate: (day) => isSameDay(widget.selectedDay, day),
        eventLoader: _getEventsForDay, // Добавляем загрузчик событий
        onDaySelected: (selectedDay, focusedDay) {
          setState(() {
            widget.onDayChanged(selectedDay);
            _focusedDay = focusedDay;
          });
        },
        onFormatChanged: (format) {
          setState(() {}); // Перерисовываем виджет при изменении формата
        },
        onPageChanged: (focusedDay) {
          _focusedDay = focusedDay; // Обновляем фокусированный день при листании
        },
        calendarFormat: CalendarFormat.month,
        rowHeight: 35,
        daysOfWeekHeight: 40,
        headerStyle: HeaderStyle(
          formatButtonVisible: false,
          titleCentered: true,
          headerPadding: const EdgeInsets.fromLTRB(0.0, 5.0, 0.0, 7.0),
          titleTextStyle: GoogleFonts.mulish(
            textStyle: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.normal,
              color: Theme.of(context).primaryColorDark,
            ),
          ),
        ),
        daysOfWeekStyle: DaysOfWeekStyle(
          weekdayStyle: GoogleFonts.mulish(
            color: Theme.of(context).primaryColorDark,
            fontSize: 25,
            fontWeight: FontWeight.normal,
            height: 1.3,
          ),
          weekendStyle: GoogleFonts.mulish(
            color: Theme.of(context).primaryColorDark,
            fontSize: 25,
            fontWeight: FontWeight.normal,
            height: 1.3,
          ),
        ),
        calendarStyle: CalendarStyle(
          isTodayHighlighted: true,
          markersMaxCount: 1, // Показывать только один маркер
          markerDecoration: BoxDecoration(
            // Стиль маркера
            color: Theme.of(context).shadowColor,
            shape: BoxShape.rectangle,
          ),
          selectedDecoration: BoxDecoration(
            color: Theme.of(context).highlightColor, // Цвет выделения выбранного дня
            shape: BoxShape.rectangle,
          ),
          todayDecoration: BoxDecoration(
            color: Theme.of(context).shadowColor, // Цвет выделения сегодняшнего дня
            shape: BoxShape.rectangle,
          ),
          defaultDecoration: const BoxDecoration(
            shape: BoxShape.rectangle, // Форма обычных дней
          ),
          defaultTextStyle: GoogleFonts.mulish(
            textStyle: const TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.normal,
              height: 1.3,
            ),
          ),
          selectedTextStyle: GoogleFonts.mulish(
            textStyle: const TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.normal,
              height: 1.3,
            ),
          ),
          todayTextStyle: GoogleFonts.mulish(
            textStyle: const TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.normal,
              height: 1.3,
            ),
          ),
          weekendTextStyle: GoogleFonts.mulish(
            textStyle: const TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.normal,
              height: 1.3,
            ),
          ),
          weekendDecoration: const BoxDecoration(
            shape: BoxShape.rectangle, // Форма выходных дней
          ),
        ),
      ),
    );
  }
}

class HomeNotes extends StatefulWidget {
  const HomeNotes(
      {super.key,
      required this.selectedDay,
      required this.onDayChanged,
      required this.notes,
      required this.isLoading,
      required this.error});

  final DateTime selectedDay;
  final Function(DateTime) onDayChanged;
  final List<Note> notes;
  final bool isLoading;
  final String error;

  @override
  State<HomeNotes> createState() => _HomeNotesState();
}

class _HomeNotesState extends State<HomeNotes> {
  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 20),
        child: Container(
          decoration: BoxDecoration(
            color: Theme.of(context).primaryColorDark,
            borderRadius: BorderRadius.circular(20),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                    child: Text(
                      'Заметки',
                      style: GoogleFonts.mulish(
                        textStyle: TextStyle(
                          fontSize: 30,
                          letterSpacing: 2,
                          fontWeight: FontWeight.w100,
                          color: Theme.of(context).primaryColorLight,
                        ),
                      ),
                    ),
                  ),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 20),
                    child: Text(
                      '${'0' * (widget.selectedDay.day < 10 ? 1 : 0)}${widget.selectedDay.day}.${'0' * (widget.selectedDay.month < 10 ? 1 : 0)}${widget.selectedDay.month}',
                      style: GoogleFonts.mulish(
                        textStyle: TextStyle(
                          fontSize: 30,
                          fontWeight: FontWeight.normal,
                          color: Theme.of(context).primaryColorLight,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
              Expanded(
                child: Padding(
                  padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 20),
                  child: widget.isLoading
                      ? Center(
                          child: CircularProgressIndicator(
                            color: Theme.of(context).primaryColorLight,
                          ),
                        )
                      : widget.notes.isEmpty
                          ? Center(
                              child: Text(
                                widget.error.isEmpty ? 'Нет заметок на этот день' : widget.error,
                                style: GoogleFonts.mulish(
                                    textStyle: TextStyle(
                                        fontSize: 20,
                                        fontWeight: FontWeight.normal,
                                        color: Theme.of(context).primaryColorLight)),
                              ),
                            )
                          : ListView.builder(
                              itemCount: widget.notes.length,
                              itemBuilder: (context, index) {
                                return Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      widget.notes[index].title,
                                      style: GoogleFonts.mulish(
                                          textStyle: TextStyle(
                                              fontSize: 20,
                                              fontWeight: FontWeight.normal,
                                              color: Theme.of(context).primaryColorLight)),
                                    ),
                                    Text(
                                      widget.notes[index].text,
                                      style: GoogleFonts.mulish(
                                          textStyle: TextStyle(
                                              fontSize: 15,
                                              fontWeight: FontWeight.normal,
                                              color: Theme.of(context).primaryColorLight)),
                                    ),
                                    if (widget.notes[index].plantId != null)
                                      Text(
                                        widget.notes[index].plantId.toString(),
                                        style: GoogleFonts.mulish(
                                            textStyle: TextStyle(
                                                fontSize: 15,
                                                fontWeight: FontWeight.normal,
                                                color: Theme.of(context).primaryColorLight)),
                                      ),
                                  ],
                                );
                              },
                            ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
