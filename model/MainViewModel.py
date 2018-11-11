import Base_values as ba


class MainViewModel:

    @classmethod
    def setup(cls):
        cls.errors = []

    @staticmethod
    def get_status(index, values):
        """ Returns 'Open' or 'Closed' based on distance sensor data. """
        try:
            if not all(x == () for x in values.values()):
                return ''.join(['Closed' if int(values[index]['a']) < 10 else 'Open {}cm'.format(values[index]['a'])])
        except TypeError:
            return

    @classmethod
    def check_value(cls, instruction, value):
        """ Checks input value from entry fields after clicking the 'Set' button. """
        if not cls.check_if_int(value):
            return cls.print_errors()

        if len(value) > 1 and any(int(x) < 0 for x in value) or int(value[0]) < 0:
            cls.errors.append('All values must be greater than 0.')

        if instruction == 3:
            roll_out_t = int(value[0])
            roll_in_t = int(value[1])
            roll_out_l = int(value[2])
            roll_in_l = int(value[3])

            if any(len(x) > 2 for x in value):
                cls.errors.append('All values must be 1 or 2 characters long.')

            if roll_in_t > roll_out_t or roll_in_l > roll_out_l:
                cls.errors.append('Roll up value can\'t be bigger than roll out value')

            if not ba.min_temp < roll_in_t < ba.max_temp or not ba.min_temp < roll_out_t < ba.max_temp:
                cls.errors.append('Temperature must be between {} and {}'.format(ba.min_temp, ba.max_temp))

            if not ba.min_light < roll_in_l < ba.max_light or not ba.min_light < roll_out_l < ba.max_light:
                cls.errors.append('Light intensity must be between {} and {}'.format(ba.min_light, ba.max_light))

        if instruction == 7:
            man_roll = int(value[0])

            if not ba.manual_min <= man_roll <= ba.manual_max:
                cls.errors.append('Value must be between {} and {}'.format(ba.manual_min, ba.manual_max))

        return cls.print_errors()

    @classmethod
    def check_if_int(cls, value):
        if not all(x.lstrip('-').isdigit() for x in value):
            cls.errors.append('Please enter integers only.')
            return False
        return True

    @classmethod
    def print_errors(cls):
        if len(cls.errors) > 0:
            for num, error in enumerate(cls.errors, 1):
                print('Error {}: {}'.format(num, error))
            cls.errors.clear()
            return False
        return True

