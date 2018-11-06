from view import GraphView as view
from model import GraphModel as model
from controller import SerialController as ser
import re


class GraphController:

    def __init__(self, canvas, sensor, device):
        self.view = view.GraphView(canvas, sensor)
        self.model = model.GraphModel()
        self.sensor = sensor
        self.device = int(re.findall('(\d)', device)[0])
        self.giveinstance()

    def giveinstance(self):
        self.view.set_controller_instance(self)

    def updategraph(self):
        """ Called by MainView.tick() """
        self.view.drawGraph()

    def get_raw_values(self):
        return ser.SerialController.current_values()

    def get_value(self):
        values = self.get_raw_values()
        try:
            return self.model.calculate(values[self.device][self.sensor], self.sensor)
        except TypeError:
            print('waiting for values...')
