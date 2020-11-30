# Импорт библиотеки tkinter для работы с GUI
from pprint import pprint
from tkinter import *
from tkinter import filedialog as fd

from route import Route
from route_place import RoutePlace


# Функция, которая считывает таблицу с данными
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
def convert_lines_to_places(lines):
    converted_places = []
    for line in lines:
        converted_places.append(
            RoutePlace(name=line[0], description=line[1], kind=line[2], address=line[3], working_hours=line[4]))
    return converted_places


# Функция, которая принимает список и возвращает список объектов-мест
def convert_lines_to_routes(lines, places):
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


def find_route_according_to_personal_preferences(routes_to_search_in, personal_preferences):
    for route_to_check in routes_to_search_in:
        if route_to_check.is_valid_to_personal_preferences(personal_preferences):
            personalized_route = []

            for place_to_check in route_to_check.route:
                if place_to_check.is_valid_to_personal_preferences(personal_preferences):
                    personalized_route.append(place_to_check)
            route_to_check.route = personalized_route
            return route_to_check
    return None


# Функция закрытия программы
def close_program():
    exit()


# Главное Приложение, запуск стартового экрана
# root = Tk()

route_places = convert_lines_to_places(read_database('places.csv'))
all_places = {}
for place in route_places:
    all_places[place.name] = place

routes = convert_lines_to_routes(read_database('routes.csv'), places=all_places)

for route in routes:
    print(route, len(route.route))

print('-'*100)
for route_place in route_places:
    print(route_place, '\n')

    # Главный цикл
# root.mainloop()
