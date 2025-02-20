import 'package:flutter/material.dart';
import 'styles/app_theme.dart';
import 'package:table_calendar/table_calendar.dart';
import 'package:intl/date_symbol_data_local.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await initializeDateFormatting('ru_RU', null);

  runApp(MaterialApp(home: Home(), title: 'Flutter App', theme: appTheme()));
}

class Home extends StatefulWidget {
  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  DateTime _focusedDay = DateTime.now(); // Текущий фокусированный день
  DateTime? _selectedDay; // Выбранный пользователем день

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
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
                      onPressed: () {},
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
                padding: EdgeInsets.symmetric(horizontal: 16.0, vertical: 0.0),
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
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: Padding(
        padding: EdgeInsets.symmetric(horizontal: 16.0, vertical: 30.0),
        child: Container(
          decoration: BoxDecoration(
            color: Theme.of(context).cardColor,
            borderRadius: BorderRadius.circular(20),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              IconButton(
                onPressed: () {},
                icon: Icon(Icons.camera_enhance_outlined),
                style: IconButton.styleFrom(
                  foregroundColor: Theme.of(context).focusColor,
                  iconSize: 50,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(20),
                  ),
                ),
              ),
              IconButton(
                onPressed: () {},
                icon: Icon(Icons.calendar_month_outlined),
                style: IconButton.styleFrom(
                  foregroundColor: Theme.of(context).focusColor,
                  iconSize: 50,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(20),
                  ),
                ),
              ),
              IconButton(
                onPressed: () {},
                icon: Icon(Icons.eco_outlined),
                style: IconButton.styleFrom(
                  foregroundColor: Theme.of(context).focusColor,
                  iconSize: 50,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(20),
                  ),
                ),
              ),
              IconButton(
                onPressed: () {},
                icon: Icon(Icons.book_outlined),
                style: IconButton.styleFrom(
                  foregroundColor: Theme.of(context).focusColor,
                  iconSize: 50,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(20),
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
