from random import randint, choice
import tkinter


class GraphView:

    def __init__(self, canvas, sensor):
        self.canvas = canvas
        self.s = 1
        self.x2 = 50
        self.color = 'dodger blue'
        self.y2 = 450
        self.add_to_canvas(sensor, self.x2, self.y2)

    def set_controller_instance(self, controller):
        self.controller = controller

    def add_to_canvas(self, sensor, min, max):
        if sensor == 'ldr':
            self.canvas.create_text((1150 / 2, 465), text="time/steps")
            self.canvas.create_text((60, 25), text="Light sensitivity")
            for x in range(min, max+25, 25):
                self.canvas.create_line(50, x, 1050, x, width=1, fill="grey80")  # x-axis
                self.canvas.create_text(30, x, text=(-x)+max)  # x-axis

        elif sensor == 'temp':
            count = 32
            self.canvas.create_text((1150 / 2, 570), text="time/steps")
            self.canvas.create_text((65, 25), text="Temperature in °C")
            for x in range(min, max+25, 25):
                self.canvas.create_line(50, x, 1050, x, width=1, fill="grey80")  # x-axis
                self.canvas.create_text(30, x, text=count)  # x-axis
                count -= 2

    def drawGraph(self):
        try:
            if self.s == 21:
                # new frame
                self.s = 1
                self.x2 = 50
                self.canvas.delete('temp')  # only delete items tagged as temp
            x1 = self.x2
            y1 = self.y2
            self.x2 = 50 + self.s * 50
            self.y2 = self.controller.get_value()
            self.canvas.create_line(x1, y1, self.x2, self.y2, fill=self.color, width=3, tags='temp')
            self.s += 1
        except tkinter.TclError:
            pass
