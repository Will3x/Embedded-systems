from view import GraphView as view
from model import GraphModel as model
from controller import SerialController as ser
from tkinter import *
import re


class GraphController:

    def __init__(self, canvas, sensor, device):
        self.sensor = sensor
        self.canvas = canvas
        self.device = int(re.findall('(\d)', device)[0])
        self.model = model.GraphModel()
        self.model.setup()
        self.view = view.GraphView(canvas, sensor, self)
        self.count = 0

    def hide_canvas(self):
        self.canvas.place_forget()

    def show_canvas(self):
        self.canvas.place(relx=0.5, rely=0.37, anchor=CENTER)

    def update_graph(self):
        """ Called by MainView.tick() """
        self.count += 1
        self.model.add_value_mean(self.sensor, self.get_values(), self.device)

        self.view.draw_graph() if self.sensor == 't' and self.count % 9 == 0 else None
        self.view.draw_graph() if self.sensor == 'l' and self.count % 6 == 0 else None

        self.model.reset_mean(self.sensor)

    def get_mean(self):
        return self.model.calculate_mean(self.sensor)

    def draw_borders(self, roll_out, roll_in):
        roll_out = self.model.calculate(roll_out, self.sensor)
        roll_in = self.model.calculate(roll_in, self.sensor)

        if roll_in is not None and roll_out is not None and roll_in < roll_out:
            self.view.draw_borders(roll_in, roll_out)

    def calculate_graph_line(self):
        values = self.get_values()
        try:
            return self.model.calculate(values[self.device][self.sensor], self.sensor)
        except TypeError:
            pass

    @staticmethod
    def get_values():
        return ser.SerialController.current_values()
