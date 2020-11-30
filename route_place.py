class RoutePlace:
    def __init__(self, name, description, kind, address, working_hours):
        self.name = name
        self.description = description
        self.kind = kind
        self.address = address
        self.working_hours = working_hours

    def __str__(self):
        return '{} \n{} \n{} \nАдрес: {} \n{}'.format(self.name, self.description,
                                                      self.kind, self.address,
                                                      self.working_hours)

    def is_valid_to_personal_preferences(self, personal_preferences):
        if self.kind in personal_preferences.self.kinds_of_places:
            for time_of_day in personal_preferences.times_of_day:
                if self.working_hours in time_of_day:
                    return True
        return False
