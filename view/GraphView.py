from random import choice
import tkinter


class GraphView:

    def __init__(self, canvas, sensor):
        self.canvas = canvas
        self.s = 0
        self.x2 = 50
        self.y2 = None
        self.sensor = sensor
        self.add_to_canvas(sensor, 50, 450)
        self.mean = []

    def set_controller_instance(self, controller):
        self.controller = controller

    def add_to_canvas(self, sensor, min, max):
        label_color = 'white'
        sublines_color = '#2D3542'

        if sensor == 'l':
            count = 100
            self.canvas.create_text((int(self.canvas['width'])/2, 25), text="Light sensitivity every 3s",
                                    fill=label_color)
            for y in range(min, max+25, 40):
                self.canvas.create_line(50, y, 1050, y, width=1, fill=sublines_color)  # y-axis
                self.canvas.create_text(30, y, text=count, fill=label_color)
                count -= 10

        elif sensor == 't':
            count = 32
            self.canvas.create_text((int(self.canvas['width'])/2, 25), text="Temperature in °C every 3s",
                                    fill=label_color)
            for y in range(min, max+25, 25):
                self.canvas.create_line(50, y, 1050, y, width=1, fill=sublines_color)  # y-axis
                self.canvas.create_text(30, y, text=count, fill=label_color)
                count -= 2

        self.draw_borders()

    def draw_borders(self, min=360, max=180):
        border = {'min (roll back in)': min, 'max (roll out)': max}

        [self.canvas.create_line(50 + x * 50, 450, 50 + x * 50, 50, width=1, fill='#2D3542') for x in range(21)]
        [self.canvas.create_line(50, x, 1050, x, width=1, fill="dodger blue") for x in border.values()]
        [self.canvas.create_text(1000, y-10, text=x, fill="dodger blue") for x, y in border.items()]

    def drawGraph(self):
        try:
            if self.s == 21:
                # new frame
                self.s = 1
                self.x2 = 50
                self.canvas.delete('t')  # only delete items tagged as temp
            x1 = self.x2
            y1 = self.y2
            self.x2 = 50 + self.s * 50
            self.y2 = self.controller.get_value()
            self.canvas.create_line(x1, y1, self.x2, self.y2, fill='#D85700', width=2, tags='t')
            self.s += 1

            # if self.sensor == 'temp':
            #     self.mean.append(int(self.controller.get_raw_values()[1]['temp']))
            #     print('Temperature mean: {0:.2f}'.format(sum(self.mean)/len(self.mean)))
            # if self.sensor == 'ldr':
            #     self.mean.append(int(self.controller.get_raw_values()[1]['ldr']))
            #     print('Light intensity mean: {0:.2f}'.format(sum(self.mean)/len(self.mean)))

        except tkinter.TclError as e:
            pass
