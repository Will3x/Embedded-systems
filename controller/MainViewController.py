from model import MainViewModel as mm
from controller import SerialController as ser


class MainViewController:

    def __init__(self, mainview, device_id, gr_controller_t, gr_controller_l):
        self.view = mainview
        self.model = mm.MainViewModel()
        self.device_id = device_id
        self.gr_controller_t = gr_controller_t
        self.gr_controller_l = gr_controller_l

        self.model.setup()

    def refresh(self):
        """ Called from tick every x ms. Checks for new values. Updates the corresponding MainView."""
        values = ser.SerialController.current_values()

        if self.get_status(self.device_id, values) is not None:
            status = self.get_status(self.device_id, values)
            self.view.update_status_label(status)

    def get_status(self, device, values):
        """ Returns 'Open' or 'Closed' based on distance sensor data if values are valid. """
        if self.model.get_status(device, values) is not None:
            return self.model.get_status(device, values)

    def btn_click(self, var):
        """ Called after button press. Each button have a unique variable ID: [var].

         [1] = 'Light intensity' button located on top, center. Switches to canvas for light intensity data.
         [2] = 'Temperature' button located on top, center. Switches to canvas for temperature data.
         [3] = 'ON' button. Sets manual mode on.
         [4] = 'OFF' button. Sets manual mode off.
         [5] = 'Roll out' button. Manually rolls out shutter. Only available when manual mode is on.
         [6] = 'Roll in' button. Manually rolls in shutter. Only available when manual mode is on.
         [7] = 'Set' button. Writes all non-manual settings to device.
         [8] = 'Set' button. Writes all manual settings to device.

        """

        if var == 1 or not isinstance(var, int) and var.get() == 1:
            self.gr_controller_t.hide_canvas()
            self.gr_controller_l.show_canvas()

        if var == 2 or not isinstance(var, int) and var.get() == 2:
            self.gr_controller_t.show_canvas()
            self.gr_controller_l.hide_canvas()

        if var == 3 or not isinstance(var, int) and var.get() == 3:
            ser.SerialController.write(self.device_id, 8, '1')
            [controller.view.change_border_state('hidden') for controller in self.view.controllers[0]]
            self.view.change_btn_state(1)

        if var == 4 or not isinstance(var, int) and var.get() == 4:
            ser.SerialController.write(self.device_id, 8, '0')
            [x.view.change_border_state('normal') for x in self.view.controllers[0]]
            self.view.change_btn_state(0)

        if var == 5:
            ser.SerialController.write(self.device_id, 1)

        if var == 6:
            ser.SerialController.write(self.device_id, 2)

        if var == 7:
            instruction = 3
            value = (self.view.entry1.get(), self.view.entry2.get(),
                     self.view.entry3.get(), self.view.entry4.get())

            if self.check_input_value(instruction, value):
                ser.SerialController.write(self.device_id, instruction, value)
                self.gr_controller_t.draw_borders(self.view.entry2.get(), self.view.entry1.get())
                self.gr_controller_l.draw_borders(self.view.entry4.get(), self.view.entry3.get())

        if var == 8:
            instruction = 7
            value = (self.view.en_man_roll_out.get(),)

            if self.check_input_value(instruction, value):
                ser.SerialController.write(self.device_id, instruction, value)

    def check_input_value(self, instruction, value):
        return self.model.check_value(instruction, value)
