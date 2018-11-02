class GraphModel:

    @staticmethod
    def calculate(value, sensor):
        try:
            return [((32 - float(value)) * 12.5) + 50 if sensor == 'temp' else 450 - (int(value)/10*40)]
        except ValueError as e:
            print('GraphModel.calculate(): {}'.format(e))


