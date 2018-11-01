from view import GraphView as view
from model import GraphModel as model
from controller import SerialController as ser


class GraphController:

    def __init__(self, canvas, sensor, device):
        self.view = view.GraphView(canvas)
        self.model = model.GraphModel()
        self.sensor = sensor
        self.device = int(device[7:])
        self.giveinstance()

    def giveinstance(self):
        self.view.set_controller_instance(self)

    def updategraph(self):
        """ Called by MainView.tick() """
        self.view.drawGraph()

    def get_value(self):
        values = ser.SerialController.dict_values
        return self.model.calculate(values[self.device][self.sensor], self.sensor)
