import Base_values as ba


class InstructionModel:

    @staticmethod
    def check_value(id, value):
        errors = []

        try:
            if id[0] == 7:
                if not ba.manual_min <= int(value[0]) <= ba.manual_max:
                    errors.append(value[0] + ' must be between {} and {}'.format(min, max))

            if len(value) == 4:
                uitrol_temp = int(value[0])
                oprol_temp = int(value[1])
                uitrol_licht = int(value[2])
                oprol_licht = int(value[3])

                if oprol_temp > uitrol_temp or oprol_licht > uitrol_licht:
                    errors.append('Roll up value can\'t be bigger than roll out value')

                if not ba.min_temp <= oprol_temp <= ba.max_temp or not ba.min_temp <= uitrol_temp <= ba.max_temp:
                    errors.append('Temperature must be between {} and {}'.format(ba.min_temp, ba.max_temp))

                if not ba.min_light <= oprol_licht <= ba.max_light or not ba.min_light <= uitrol_licht <= ba.max_light:
                    errors.append('Light sensitivity must be between {} and {}'.format(ba.min_light, ba.max_light))

        except ValueError:
            errors.append('Please enter an integer')

        if len(errors) > 0:
            for num, error in enumerate(errors, 1):
                print('Error {}: {}'.format(num, error))
            errors.clear()
            return False

        return True
