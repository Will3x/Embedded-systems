class GraphModel:

    def __init__(self):
        pass

    def calculate(self, value, sensor):
        try:
            if sensor == 'temp':
                return ((32 - float(value)) * 12.5) + 50

            return (-(int(value))) + 450

        except ValueError:
            print('Something went wrong with reading data')


