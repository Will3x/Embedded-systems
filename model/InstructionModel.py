class InstructionModel:

    @classmethod
    def check_value(cls, id, value):
        min = 0
        max = 150
        errors = []

        try:
            if id[0] == 7:
                return min <= int(value[0]) <= max

            if len(value) == 4:
                uitrol_temp = int(value[0])
                oprol_temp = int(value[1])
                uitrol_licht = int(value[2])
                oprol_licht = int(value[3])

                if not uitrol_temp > oprol_temp or not uitrol_licht > oprol_licht:
                    errors.append('Value for Uitrol is bigger than value for Oprol.')

                for x in range(len(id)):
                    num = int(value[x])
                    if not min <= num <= max:
                        errors.append('Value not in range: {} - {}'.format(min, max))

        except ValueError:
            errors.append('Please enter an integer')

        if len(errors) > 0:
            for num, error in enumerate(errors, 1):
                print('Error {}: {}'.format(num, error))
            errors.clear()
            return False

        return True
