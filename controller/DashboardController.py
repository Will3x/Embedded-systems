from controller import SerialController as ser
from model import InstructionModel as instr


class DashboardController:

    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.giveinstance()

    def giveinstance(self):
        self.view.set_controller_instance(self)

    def check_if_connected(self):
        connections = ser.SerialController.check_connection()
        return connections

    def write(self, id, value):
        try:
            if instr.InstructionModel.check_value(id, value):
                # instruction = instr.InstructionModel.getinstruction(id)
                ser.SerialController.write(id, value)
            else:
                print('value entered not in range!')
        except ValueError:
            print('Please enter an integer')

    def get_values(self):
        values = ser.SerialController.read()
        self.view.change_label(values)




