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
        return ser.SerialController.isOpen

    def btn_event(self, value):
        pass

    def get_values(self):
        value = randint(-10, 30)
        self.view.change_label(value)




