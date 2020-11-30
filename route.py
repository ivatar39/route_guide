class Route:
    def __init__(self, point_a, point_b, distance, time, kind, route):
        self.point_a = point_a
        self.point_b = point_b
        self.distance = distance
        self.time = time
        self.kind = kind
        self.route = route

    def __str__(self):
        return '{} - {}. Дист: {}. Время: {}. Тип - {}\n'.format(self.point_a, self.point_b, self.distance, self.time,
                                                                 self.kind)

    def is_valid_to_personal_preferences(self, personal_preferences):
        return self.point_a == personal_preferences.point_a and \
               self.point_b == personal_preferences.point_b and \
               self.kind == personal_preferences.route_kind
