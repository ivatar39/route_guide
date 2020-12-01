# Импорт библиотеки tkinter для работы с GUI
from tkinter import *

from personal_preferences import PersonalPreferences
from route import Route
from route_place import RoutePlace

# Функция, которая считывает таблицу с данными и возвращает список строк
from scrollable_frame import ScrollableFrame


def read_database(filename):
    try:
        file = open(filename, encoding='UTF-8')
        file_lines = file.readlines()
        # Удаление заголовков
        file_lines.pop(0)
        processed_lines = []
        # Форматирование csv-файла
        for line in file_lines:
            processed_lines.append(line.replace('\n', '').rsplit(';'))
        file.close()
        return processed_lines
    except FileNotFoundError:
        print('Файл не найден')


# Функция, которая принимает список и возвращает список объектов-мест
def convert_lines_into_places(lines):
    converted_places = []
    for line in lines:
        converted_places.append(
            RoutePlace(name=line[0], description=line[1], kind=line[2], address=line[3], working_hours=line[4]))
    return converted_places


# Функция, которая принимает список и возвращает список объектов-маршрутов
def convert_lines_into_routes(lines, places):
    converted_routes = []
    for line in lines:
        converted_route = []
        for i in range(5, len(line)):
            if len(line[i]) != 0:
                converted_route.append(places[line[i]])
        converted_routes.append(
            Route(point_a=line[0], point_b=line[1], distance=line[2], time=line[3], kind=line[4],
                  route=converted_route))
    return converted_routes


# Функция, которая принимает маршруты и персональные предпочтения.
# Возвращает маршрут, соответствующий персональным предпочтениям
def find_route_according_to_personal_preferences(routes_to_search_in, personal_preferences):
    for route_to_check in routes_to_search_in:
        if route_to_check.is_valid_to_personal_preferences(personal_preferences):
            personalized_route = []

            for place_to_check in route_to_check.route:
                if place_to_check.is_valid_to_personal_preferences(personal_preferences):
                    print(place_to_check)
                    personalized_route.append(place_to_check)
            route_to_check.route = list(dict.fromkeys(personalized_route))
            return route_to_check
    return None


def ask_personal_preferences(destinations_to_ask, routes_to_ask):
    # Окно спрашивания предпочтений
    main_window = Toplevel(root)
    main_window.minsize(width=450, height=700)
    # Точка A
    point_a_frame = Frame(main_window)
    point_a_frame.pack()
    a_variable = StringVar(point_a_frame)
    point_a_lst = destinations_to_ask
    a_variable.set(point_a_lst[0])  # default value
    point_a_option_menu = OptionMenu(point_a_frame, a_variable, *point_a_lst)
    point_a_option_menu.pack(side=RIGHT)
    point_a_text_label = Label(point_a_frame, text='Начало маршрута: ', font='Roboto 12')
    point_a_text_label.pack(side=LEFT)
    # Точка B
    point_b_frame = Frame(main_window)
    point_b_frame.pack()
    b_variable = StringVar(point_a_frame)
    point_b_lst = destinations_to_ask
    b_variable.set(point_b_lst[0])  # default value
    point_b_option_menu = OptionMenu(point_b_frame, b_variable, *point_b_lst)
    point_b_option_menu.pack(side=RIGHT)
    point_b_text_label = Label(point_b_frame, text='Конец маршрута: ', font='Roboto 12')
    point_b_text_label.pack(side=LEFT)
    # Вид транспорта
    type_of_transport_frame = Frame(main_window, highlightbackground="#c7c7c7", highlightthickness=1)
    type_of_transport_frame.pack(pady=24)
    type_of_transport_text_label = Label(type_of_transport_frame, text='Какой вид маршрута вы предпочитаете?',
                                         font='Roboto 12')
    type_of_transport_text_label.pack()
    is_pedestrian_variable = BooleanVar()
    is_pedestrian_variable.set(1)
    is_pedestrian_radio_button = Radiobutton(type_of_transport_frame, text='🚶 ‍Пеший',
                                             variable=is_pedestrian_variable, value=1, font='Roboto 11')
    is_pedestrian_radio_button.pack()
    is_cyclist_radio_button = Radiobutton(type_of_transport_frame, text='🚲 Велосипед',
                                          variable=is_pedestrian_variable, value=0, font='Roboto 11')
    is_cyclist_radio_button.pack()
    # Время суток
    times_of_day_frame = Frame(main_window, highlightbackground="#c7c7c7", highlightthickness=1)
    times_of_day_frame.pack(pady=16)
    times_of_day_text_label = Label(times_of_day_frame, text='Какое время суток вам по душе?',
                                    font='Roboto 12')
    times_of_day_text_label.pack()

    is_morning = BooleanVar()
    is_morning.set(0)
    is_morning_check_button = Checkbutton(times_of_day_frame, text="🌅 Утро",
                                          variable=is_morning,
                                          onvalue=1, offvalue=0, font='Roboto 11'
                                          )
    is_morning_check_button.pack(anchor=W, padx=10)

    is_day = BooleanVar()
    is_day.set(0)
    is_day_check_button = Checkbutton(times_of_day_frame, text="☀ День",
                                      variable=is_day,
                                      onvalue=1, offvalue=0, font='Roboto 11'
                                      )
    is_day_check_button.pack(anchor=W, padx=10)
    is_night = BooleanVar()
    is_night.set(0)

    is_night_check_button = Checkbutton(times_of_day_frame, text="🌑 Ночь",
                                        variable=is_night,
                                        onvalue=1, offvalue=0, font='Roboto 11'
                                        )
    is_night_check_button.pack(anchor=W, padx=10)
    # Места для посещения
    places_to_visit_frame = Frame(main_window, highlightbackground="#c7c7c7", highlightthickness=1)
    places_to_visit_frame.pack(pady=20)
    places_to_visit_frame_text_label = Label(places_to_visit_frame, text='Какие места вы бы хотели посетить?',
                                             font='Roboto 12')
    places_to_visit_frame_text_label.pack()

    is_bars = BooleanVar()
    is_bars.set(0)
    is_bars_check_button = Checkbutton(places_to_visit_frame, text="🍸 Бары",
                                       variable=is_bars,
                                       onvalue=1, offvalue=0, font='Roboto 11'
                                       )
    is_bars_check_button.pack(anchor=W, padx=10)

    is_cafes = BooleanVar()
    is_cafes.set(0)
    is_cafes_check_button = Checkbutton(places_to_visit_frame, text="☕ Кафе",
                                        variable=is_cafes,
                                        onvalue=1, offvalue=0, font='Roboto 11'
                                        )
    is_cafes_check_button.pack(anchor=W, padx=10)

    is_restaurants = BooleanVar()
    is_restaurants.set(0)
    is_restaurants_check_button = Checkbutton(places_to_visit_frame, text="🍽 Рестораны",
                                              variable=is_restaurants,
                                              onvalue=1, offvalue=0, font='Roboto 11'
                                              )
    is_restaurants_check_button.pack(anchor=W, padx=10)

    is_active_rest = BooleanVar()
    is_active_rest.set(0)
    is_active_rest_check_button = Checkbutton(places_to_visit_frame, text="⚽ Места активного отдыха",
                                              variable=is_active_rest,
                                              onvalue=1, offvalue=0, font='Roboto 11'
                                              )
    is_active_rest_check_button.pack(anchor=W, padx=10)

    is_sights = BooleanVar()
    is_sights.set(0)
    is_sights_check_button = Checkbutton(places_to_visit_frame, text="🏰 Достопримечательности",
                                         variable=is_sights,
                                         onvalue=1, offvalue=0, font='Roboto 11'
                                         )
    is_sights_check_button.pack(anchor=W, padx=10)

    # Составить маршрут

    make_route_frame = Frame(main_window)
    make_route_frame.pack(pady=24)
    make_route_button = Button(make_route_frame, text='Составить маршрут', width=30, height=5, font='Roboto 12',
                               bg='#fafafa',
                               command=lambda: make_personal_preferences(a_variable.get(), b_variable.get(),
                                                                         get_type_of_route(
                                                                             is_pedestrian_variable.get()),
                                                                         get_times_of_day(is_morning.get(),
                                                                                          is_day.get(),
                                                                                          is_night.get()),
                                                                         get_kinds_of_places(is_bars.get(),
                                                                                             is_cafes.get(),
                                                                                             is_restaurants.get(),
                                                                                             is_active_rest.get(),
                                                                                             is_sights.get()),
                                                                         routes_to_ask),
                               )
    make_route_button.pack()


def get_type_of_route(is_pedestrian):
    if is_pedestrian:
        route_kind = "Пеший"
    else:
        route_kind = "Велосипед"
    return route_kind


def get_times_of_day(is_morning, is_day, is_night):
    times_of_day = []
    if is_morning:
        times_of_day.append("Утро")
    if is_day:
        times_of_day.append("День")
    if is_night:
        times_of_day.append("Ночь")
    return times_of_day


def get_kinds_of_places(is_bars, is_cafes, is_restaurants, is_active_rest, is_sights):
    kinds_of_places = []
    if is_bars:
        kinds_of_places.append("Бар")
    if is_cafes:
        kinds_of_places.append("Кафе")
    if is_restaurants:
        kinds_of_places.append("Ресторан")
    if is_active_rest:
        kinds_of_places.append("Место активного отдыха")
    if is_sights:
        kinds_of_places.append("Достопримечательность")
    return kinds_of_places


def make_personal_preferences(make_point_a, make_point_b, make_route_kind, make_times_of_day, make_kinds_of_places,
                              routes_to_search_in):
    personal_preferences = PersonalPreferences(point_a=make_point_a[2:-3], point_b=make_point_b[2:-3],
                                               route_kind=make_route_kind,
                                               times_of_day=make_times_of_day, kinds_of_places=make_kinds_of_places)
    personalized_route = find_route_according_to_personal_preferences(routes_to_search_in, personal_preferences)
    if personalized_route is not None and len(personalized_route.route) > 0:
        draw_personal_route(personalized_route)
    else:
        draw_no_route()


def draw_no_route():
    # Окно с информацией о том, что нет маршрута
    main_window = Toplevel(root)
    main_window.minsize(width=250, height=100)
    no_result_label = Label(main_window, text='Извините, но по Вашим предпочтениям не удалось найти маршрут.',
                            font='Roboto 12', bg='#ab000d', fg='#fafafa')
    no_result_label.pack()


def draw_personal_route(personalized_route):
    # Окно персонализированного маршрута
    main_window = Toplevel(root)
    main_window.minsize(width=550, height=700)
    route_header_frame = Frame(main_window, highlightbackground="#c7c7c7", highlightthickness=1)
    route_header_frame.pack(side=TOP, pady=4)
    destinations_text_label = Label(route_header_frame,
                                    text='{} - {}'.format(personalized_route.point_a, personalized_route.point_b),
                                    font='Roboto 14 bold')
    destinations_text_label.pack(side=TOP)

    distance_text_label = Label(route_header_frame,
                                text='Дистанция - {}'.format(personalized_route.distance),
                                font='Roboto 12 underline')
    distance_text_label.pack()

    time_text_label = Label(route_header_frame,
                            text='Время - {}'.format(personalized_route.time),
                            font='Roboto 12')
    time_text_label.pack()

    route_type_text_label = Label(route_header_frame,
                                  text='Тип маршрута - {}'.format(personalized_route.kind),
                                  font='Roboto 12')
    route_type_text_label.pack()

    route_frame = Frame(main_window, highlightbackground="#c7c7c7", highlightthickness=2)
    route_frame.pack(expand=1, fill=BOTH, pady=4, padx=4)
    frame = ScrollableFrame(route_frame)
    for place_to_draw in personalized_route.route:
        place_frame = Frame(frame.scrollable_frame, highlightbackground="#0093c4", highlightthickness=2)
        place_frame.pack()
        name_text_label = Label(frame.scrollable_frame, text=place_to_draw.name, font='Roboto 13 bold', justify=LEFT)
        name_text_label.pack()
        description_text_label = Message(frame.scrollable_frame, text=place_to_draw.description, font='Roboto 11')
        description_text_label.pack()
        kind_text_label = Label(frame.scrollable_frame, text=place_to_draw.kind, font='Roboto 11 underline',
                                justify=LEFT)
        kind_text_label.pack()
        address_text_label = Message(frame.scrollable_frame, text=place_to_draw.address, font='Roboto 12', justify=LEFT)
        address_text_label.pack()
        working_hours_text_label = Label(frame.scrollable_frame,
                                         text='Работает: {}'.format(place_to_draw.working_hours),
                                         font='Roboto 11', justify=LEFT)
        working_hours_text_label.pack()
    frame.pack(expand=1, fill=BOTH)


# Функция закрытия программы
def close_program():
    exit()


# Главное Приложение, подготовка нужных данных

route_places = convert_lines_into_places(read_database('places.csv'))
# Словарь всех мест
all_places = {}
for place in route_places:
    all_places[place.name] = place

# Список всех маршрутов
routes = convert_lines_into_routes(read_database('routes.csv'), places=all_places)
# Список точек назначения (точки A и B)
destinations = read_database('destinations.csv')

# Лэндинг
root = Tk()

# Фрейм - шапка экрана
start_bar_frame = Frame(root)
start_bar_frame.pack(side=TOP, padx=80, pady=14)
# Заголовок
route_guide_text_label = Label(start_bar_frame, text='Составитель маршрутов по персональным предпочтениям',
                               font='Roboto 14', bg='#3f51b5', fg='#fafafa')
route_guide_text_label.pack(side=TOP)
# Фрейм тело экрана
start_frame = Frame(root)
start_frame.pack(side=BOTTOM, pady=40, expand=1)
# Кнопка начала составления предпочтений
start_button = Button(start_frame, text='Начать', width=30, height=5,
                      command=lambda: ask_personal_preferences(destinations, routes),
                      font='Roboto 12', bg='#fafafa')
start_button.pack(side=TOP, expand=1, anchor=S)
# Кнопка начала составления предпочтений
about_author_button = Button(start_frame, text='Выход', width=30, height=5,
                             command=lambda: close_program(),
                             font='Roboto 12', bg='#fafafa')
about_author_button.pack(side=BOTTOM, expand=1, anchor=S)

# Главный цикл
root.mainloop()
