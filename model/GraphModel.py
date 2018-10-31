from random import randint


class GraphModel:

    def __init__(self):
        pass

    def calculate_temperature(self, value):
        return (-((int(value)) ** 1.8)) + 400

    def calculate_light(self, value):
        return (-(int(value)/200)*100) + 425

