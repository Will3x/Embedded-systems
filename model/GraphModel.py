class GraphModel:

    @staticmethod
    def calculate(value, sensor):
        try:
            return [((32 - float(value)) * 12.5) + 50 if sensor == 't' else 450 - (int(value)/10*40)]
        except ValueError as e:
            print('GraphModel.calculate(): {}'.format(e))

    @staticmethod
    def calc(value, sensor):
        if GraphModel.check_value(value, sensor):
            return ((32 - int(value)) * 12.5) + 50 if sensor == 't' else 450 - (int(value) / 10 * 40)
        return None

    @staticmethod
    def check_value(value, sensor):
        min_light = 0
        max_light = 100

        max_temp = 32
        min_temp = 0


        try:
            int(value)
        except ValueError:
            print('Error: {} is not an integer.'.format(value))
            return False

        if sensor == 't':
            if not min_temp <= int(value) <= max_temp:
                return False

        elif sensor == 'l':
            if not min_light <= int(value) <= max_light:
                return False

        return True

