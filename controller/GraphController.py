from view import GraphView as view
from model import GraphModel as model
from controller import SerialController as ser
from tkinter import CENTER
import Base_values as ba
import re


class GraphController:

    def __init__(self, canvas, sensor, device):
        self.view = view.GraphView(canvas, sensor, self)
        self.model = model.GraphModel()
        self.sensor = sensor
        self.canvas = canvas
        self.device = int(re.findall('(\d)', device)[0])
        self.count = 0

        self.model.setup()

    def update_graph(self):
        """ Called by MainView.tick(). Counts every tick and draws on canvas after count has reached certain value.
        This function will also add new read values every tick to calculate the mean. Draw_graph() uses the mean
        value to draw the graph. Added values are deleted afterwards. Rinse and repeat. """
        self.count += 1
        self.model.add_value_mean(self.sensor, ser.SerialController.current_values(), self.device)

        if self.count % ba.graph_update == 0:
            self.view.draw_graph()
            self.model.reset_mean(self.sensor)

    def get_mean(self):
        """ Returns mean of values read. """
        return self.model.calculate_mean(self.sensor)

    def draw_borders(self, roll_out, roll_in):
        """ Gets the calculated Y position and calls view.draw_borders(): Deletes the old and draws the new blue
        border lines and texts on both graphs that indicate when the shutter should roll out or roll back in. """
        roll_out = self.model.calculate_y_pos(roll_out, self.sensor)
        roll_in = self.model.calculate_y_pos(roll_in, self.sensor)

        if roll_in is not None and roll_out is not None and roll_in < roll_out:
            self.view.draw_borders(roll_in, roll_out)

    def calculate_graph_line(self):
        """ Directly calculates Y position for value read from serial. """
        try:
            values = ser.SerialController.current_values()
            return self.model.calculate_y_pos(values[self.device][self.sensor], self.sensor)
        except TypeError:
            pass

    def hide_canvas(self):
        self.canvas.place_forget()

    def show_canvas(self):
        self.canvas.place(relx=0.5, rely=0.37, anchor=CENTER)
