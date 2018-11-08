from view import GraphView as view
from model import GraphModel as model
from controller import SerialController as ser
import re


class GraphController:

    def __init__(self, canvas, sensor, device):
        self.sensor = sensor
        self.device = int(re.findall('(\d)', device)[0])
        self.model = model.GraphModel()
        self.view = view.GraphView(canvas, sensor, self)

    def updategraph(self):
        """ Called by MainView.tick() """
        self.view.drawGraph()

    def get_raw_values(self):
        return ser.SerialController.current_values()

    def draw_borders(self, min, max):
        min = self.model.calculate(min, self.sensor)
        max = self.model.calculate(max, self.sensor)

        if min is not None and max is not None:
            self.view.draw_borders(self.sensor, min, max)

    def get_value(self):
        values = self.get_raw_values()

        try:
            return self.model.calculate(values[self.device][self.sensor], self.sensor)
        except TypeError:
            pass
