import Base_values as ba


class GraphModel:

    @classmethod
    def setup(cls):
        cls.mean_t = []
        cls.mean_l = []

    @staticmethod
    def calculate_y_pos(value, sensor):
        """ Calculates and returns Y position to draw the graph or the border lines on canvas. Correct calculation
        is based on given sensor. """
        if GraphModel.check_value(value, sensor):
            return ((32 - int(value)) * 12.5) + 50 if sensor == 't' else 450 - (int(value) / 10 * 40)
        return

    @classmethod
    def calculate_mean(cls, sensor):
        """ Returns mean value for values in mean_t or mean_l list based on sensor. """
        if sensor == 't':
            print('Average temperature: {}'.format(sum(cls.mean_t) / len(cls.mean_t)))
            return cls.calculate_y_pos(sum(cls.mean_t) / len(cls.mean_t), sensor)
        if sensor == 'l':
            print('Average light intensity: {}'.format(sum(cls.mean_l) / len(cls.mean_l)))
            return cls.calculate_y_pos(sum(cls.mean_l) / len(cls.mean_l), sensor)

    @classmethod
    def add_value_mean(cls, sensor, values, device_id):
        """ Adds read value to mean. Called every tick. These values are used to get the mean value. """
        if values[device_id] is not None:
            if sensor == 't':
                cls.mean_t.append(int(values[device_id][sensor]))
            if sensor == 'l':
                cls.mean_l.append(int(values[device_id][sensor]))

    @classmethod
    def reset_mean(cls, sensor):
        """ Resets list of read values. Called once graph has used previous values to calculate mean. """
        if sensor == 't':
            cls.mean_t.clear()
            return cls.mean_t == []
        if sensor == 'l':
            cls.mean_l.clear()
            return cls.mean_l == []

    @staticmethod
    def check_value(value, sensor):
        """ Checks if value is an integer and if value is in range. Returns True or False. """
        if not GraphModel.check_if_int(value):
            return False

        return (sensor == 't' and ba.min_temp < int(value) < ba.max_temp) or \
               (sensor == 'l' and ba.min_light < int(value) < ba.max_light)

    @staticmethod
    def check_if_int(value):
        try:
            return isinstance(int(value), int)
        except ValueError:
            return False
