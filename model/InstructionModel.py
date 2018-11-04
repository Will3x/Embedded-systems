class InstructionModel:

    # @staticmethod
    # def getinstruction(id):
    #     """ Best function EU. I'll just leave this here for now lol """
    #     return id

    @staticmethod
    def check_value(id, *value):

        if isinstance(id, list):
            for x in range(len(id)):
                num = int(value[0][x])
                if not 0 <= num <= 150:
                    print('{} is not between 0 - 150'.format(num))
                    return False

            uitrol_temp = value[0][0]
            uitrol_licht = value[0][1]
            oprol_temp = value[0][2]
            oprol_licht = value[0][3]

            return uitrol_temp > oprol_temp or uitrol_licht > oprol_licht

        # ===============================================================

        num = int(value[0][0])

        if id == 7:
            return 0 <= num <= 150
