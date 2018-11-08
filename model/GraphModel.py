import Base_values as ba


class GraphModel:

    @staticmethod
    def calculate(value, sensor):
        if GraphModel.check_value(value, sensor):
            return ((32 - int(value)) * 12.5) + 50 if sensor == 't' else 450 - (int(value) / 10 * 40)
        return None

    @staticmethod
    def check_value(value, sensor):
        if not GraphModel.check_if_int(value):
            return False

        if sensor == 't':
            if not ba.min_temp < int(value) < ba.max_temp:
                return False

        if sensor == 'l':
            if not ba.min_light < int(value) < ba.max_light:
                return False

        return True

    @staticmethod
    def check_if_int(value):
        try:
            return isinstance(int(value), int)
        except ValueError:
            return False
