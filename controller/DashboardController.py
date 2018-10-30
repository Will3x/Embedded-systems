from controller import SerialController as ser


class DashboardController:

    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.giveinstance()

    def giveinstance(self):
        self.view.set_controller_instance(self)
        print('giving instance')
        # self.model.getControllerinstance(self)

    def check_if_connected(self):
        return ser.SerialController.isOpen

    def btn_event(self, value):
        self.view.create_instance(value)





