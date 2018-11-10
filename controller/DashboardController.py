from controller import SerialController as ser
from view import MainView as mv


class DashboardController:

    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.view.set_controller_instance(self)

    def refresh(self):
        """ Called from tick every x ms. Checks for new values and devices after reading the devices. Updates the
        dashboard and model. """
        values = ser.SerialController.current_values()
        devices = ser.SerialController.current_connections()

        self.view.update_label(devices, values)
        self.view.update_btn_state(devices)
        self.model.update_instances(devices)
        self.model.set_prev_devices(devices)

        devices.update(devices.fromkeys(devices, ''))

        [view.tick() for view in self.model.get_mv_dict().values() if view is not None]

    def create_mv_instance(self, index):
        """ Creates class instances and saves these in a dictionary """
        if self.model.mv_empty(index):
            name = 'Device {}'.format(index)
            self.model.add_mv(index, mv.MainView(name))

    def show_mv(self, index):
        """ Show specific MainView called from button: View. """
        self.model.get_mv_dict(index).show_window()

    def close_all(self):
        """ Closes all open MainView instances and the Dashboard. Called when the close button (X) of Dashboard
        is clicked"""
        [view.close() for view in self.model.get_mv_dict().values() if view is not None]
        self.view.close()

    def change_manual_on(self, index):
        """ Switches manual button of specific MainView object to ON. Called after pressing a button with a manual
        action on Dashboard. """
        if not self.model.mv_empty(index):
            self.model.get_mv_dict(index).controllers[1].btn_click(3)

    def get_status(self, device, values):
        """ Returns 'Open' or 'Closed' based on distance sensor data if values are valid. """
        if self.model.get_status(device, values) is not None:
            return self.model.get_status(device, values)

    def btn_click(self, var, index=None):
        """ Called after button press. Each button have a unique variable ID: [var].

         [4] = 'view' button. Opens MainView object.
         [5] = 'Roll out' button. Rolls out specific shutter indicated with index / device ID.
         [6] = 'Roll in' button. Rolls in specific shutter indicated with index / device ID.
         [7] = 'Roll all out' button. Rolls all connected shutters out.
         [8] = 'Roll all in' button. Rolls all connected shutter in.

         """

        if var == 4:
            self.show_mv(index)

        if var == 5:
            self.change_manual_on(index)
            ser.SerialController.write(index, 1)

        # Roll in.
        if var == 6:
            self.change_manual_on(index)
            ser.SerialController.write(index, 2)

        if var == 7:
            [self.btn_click(6, device) for device, instance in self.model.get_mv_dict().items() if instance is not None]

        # Roll in.
        if var == 8:
            [self.btn_click(5, device) for device, instance in self.model.get_mv_dict().items() if instance is not None]




