from view import GraphView as view
from model import GraphModel as model
from controller import SerialController as ser


class GraphController:

    def __init__(self, canvas, num):
        self.view = view.GraphView(canvas)
        self.model = model.GraphModel()
        self.num = num
        self.giveinstance()

    def giveinstance(self):
        self.view.set_controller_instance(self)

    def updategraph(self):
        """ Called by mainview.tick() """
        self.view.drawGraph()

    def get_value(self):
        values = ser.SerialController.dict_values
        if self.num == 0:
            return self.model.calculate_temperature(values[1]['temp'])
        if self.num == 1:
            return self.model.calculate_light(values[1]['ldr'])
