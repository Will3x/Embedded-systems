from random import randint


class GraphModel:

    def __init__(self):
        pass

    def calculate(self, value, sensor):
        if sensor == 'temp':
            return (-((int(value)) ** 1.8)) + 400
        else:
            return (-(int(value) / 200) * 100) + 425


