from controller import SerialController as ser


class DashboardController:

    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.view.set_controller_instance(self)

    @staticmethod
    def check_if_connected():
        connections = ser.SerialController.current_connections()
        return connections

    def read_from_serial(self):
        ser.SerialController.read()
        self.get_values()

    def get_values(self):
        values = ser.SerialController.current_values()
        devices = self.check_if_connected()
        self.view.change_label(devices, values)

    def status_open_closed(self, device, values):
        if self.model.status_open_closed(device, values) is not None:
            return self.model.status_open_closed(device, values)

    def buttonclick_event(self, var, device=None):
        # Roll out.
        if var == 5:
            self.view.change_manual_on(device)
            ser.SerialController.write(device, 1)

        # Roll in.
        if var == 6:
            self.view.change_manual_on(device)
            ser.SerialController.write(device, 2)

        if var == 7:
            [self.buttonclick_event(6, device) for device, instance in self.view.mainview.items() if instance != '']

        # Roll in.
        if var == 8:
            [self.buttonclick_event(5, device) for device, instance in self.view.mainview.items() if instance != '']




