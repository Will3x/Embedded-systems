class InstructionModel:

    @classmethod
    def check_value(cls, id, value):
        min = 0
        max = 150

        min_light = 0
        max_light = 100

        max_temp = 32
        min_temp = 0

        errors = []

        try:
            if id[0] == 7:
                if not min <= int(value[0]) <= max:
                    errors.append(value[0] + ' must be between {} and {}'.format(min, max))

            if len(value) == 4:
                uitrol_temp = int(value[0])
                oprol_temp = int(value[1])
                uitrol_licht = int(value[2])
                oprol_licht = int(value[3])

                if oprol_temp > uitrol_temp or oprol_licht > uitrol_licht:
                    errors.append('Roll up value can\'t be bigger than roll out value')

                if not min_temp <= oprol_temp <= max_temp or not min_temp <= uitrol_temp <= max_temp:
                    errors.append('Temperature must be between {} and {}'.format(min_temp, max_temp))

                if not min_light <= oprol_licht <= max_light or not min_light <= uitrol_licht <= max_light:
                    errors.append('Light sensitivity must be between {} and {}'.format(min_light, max_light))

        except ValueError:
            errors.append('Please enter an integer')

        if len(errors) > 0:
            for num, error in enumerate(errors, 1):
                print('Error {}: {}'.format(num, error))
            errors.clear()
            return False

        return True
