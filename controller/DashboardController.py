from controller import SerialController as ser
from controller import GraphController
from random import randint, choice

class DashboardController:

    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.giveinstance()

    def giveinstance(self):
        self.view.set_controller_instance(self)
        # self.model.getControllerinstance(self)

    def check_if_connected(self):
        connections = ser.SerialController.check_connection()
        return connections

    def get_values(self):
        values = ser.SerialController.read()
        self.view.change_label(values)




