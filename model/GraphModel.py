import Base_values as ba


class GraphModel:

    @classmethod
    def setup(cls):
        cls.mean_t = []
        cls.mean_l = []

    @staticmethod
    def calculate(value, sensor):
        if GraphModel.check_value(value, sensor):
            return ((32 - int(value)) * 12.5) + 50 if sensor == 't' else 450 - (int(value) / 10 * 40)
        return None

    @classmethod
    def calculate_mean(cls, sensor):
        if sensor == 't':
            print('Average temperature: {}'.format(sum(cls.mean_t) / len(cls.mean_t)))
            return cls.calculate(sum(cls.mean_t) / len(cls.mean_t), sensor)
        if sensor == 'l':
            print('Average light intensity: {}'.format(sum(cls.mean_l) / len(cls.mean_l)))
            return cls.calculate(sum(cls.mean_l) / len(cls.mean_l), sensor)

    @classmethod
    def add_value_mean(cls, sensor, values, device_id):
        if values[device_id] is None:
            return None

        if sensor == 't':
            cls.mean_t.append(int(values[device_id][sensor]))
        if sensor == 'l':
            cls.mean_l.append(int(values[device_id][sensor]))

    @classmethod
    def reset_mean(cls, sensor):
        if sensor == 't':
            cls.mean_t.clear()
            return cls.mean_t == []
        if sensor == 'l':
            cls.mean_l.clear()
            return cls.mean_l == []

    @staticmethod
    def check_value(value, sensor):
        if not GraphModel.check_if_int(value):
            return False

        if sensor == 't' and not ba.min_temp < int(value) < ba.max_temp or \
           sensor == 'l' and not ba.min_light < int(value) < ba.max_light:
                return False

        return True

    @staticmethod
    def check_if_int(value):
        try:
            return isinstance(int(value), int)
        except ValueError:
            return False
