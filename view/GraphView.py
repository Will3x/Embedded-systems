import tkinter
import Style as st


class GraphView:

    def __init__(self, canvas, sensor, controller):
        self.canvas = canvas
        self.s = 0
        self.x2 = 50
        self.y2 = None
        self.line_t, self.line_l, self.txt_l, self.txt_t = None, None, None, None
        self.sensor = sensor
        self.controller = controller
        self.add_to_canvas(sensor, 50, 450)
        self.mean = []

    def add_to_canvas(self, sensor, min, max):
        if sensor == 'l':
            count = 100
            self.canvas.create_text((int(self.canvas['width'])/2, 25), text="Light intensity in %",
                                    fill=st.label_white)
            for y in range(min, max+25, 40):
                self.canvas.create_line(50, y, 1050, y, width=1, fill=st.guide_lines)  # y-axis
                self.canvas.create_text(30, y, text=count, fill=st.label_white)
                count -= 10

        elif sensor == 't':
            count = 32
            self.canvas.create_text((int(self.canvas['width'])/2, 25), text="Temperature in °C",
                                    fill=st.label_white)
            for y in range(min, max+25, 25):
                self.canvas.create_line(50, y, 1050, y, width=1, fill=st.guide_lines)  # y-axis
                self.canvas.create_text(30, y, text=count, fill=st.label_white)
                count -= 2

        self.draw_guidelines()

    def draw_borders(self, sensor, min, max):
        if self.line_l is not None and self.txt_l is not None:
            [self.canvas.delete(x) for x in self.line_l]
            [self.canvas.delete(x) for x in self.txt_l]
        if self.line_t is not None and self.txt_t is not None:
            [self.canvas.delete(x) for x in self.line_t]
            [self.canvas.delete(x) for x in self.txt_t]

        border = {'Roll in': min, 'Roll out': max}

        if sensor == 'l':
            self.line_l = [self.canvas.create_line(50, x, 1050, x, width=1, fill=st.border_blue) for x in border.values()]
            self.txt_l = [self.canvas.create_text(1020, y-10, text=x, fill=st.border_blue) for x, y in border.items()]
        elif sensor == 't':
            self.line_t = [self.canvas.create_line(50, x, 1050, x, width=1, fill=st.border_blue) for x in border.values()]
            self.txt_t = [self.canvas.create_text(1020, y - 10, text=x, fill=st.border_blue) for x, y in border.items()]

    def hide_borders(self):
        if self.sensor == 'l':
            [self.canvas.itemconfigure(x, state='hidden') for x in self.line_l]
            [self.canvas.itemconfigure(x, state='hidden') for x in self.txt_l]
        if self.sensor == 't':
            [self.canvas.itemconfigure(x, state='hidden') for x in self.line_t]
            [self.canvas.itemconfigure(x, state='hidden') for x in self.txt_t]

    def show_borders(self):
        if self.sensor == 'l':
            [self.canvas.itemconfigure(x, state='normal') for x in self.line_l]
            [self.canvas.itemconfigure(x, state='normal') for x in self.txt_l]
        if self.sensor == 't':
            [self.canvas.itemconfigure(x, state='normal') for x in self.line_t]
            [self.canvas.itemconfigure(x, state='normal') for x in self.txt_t]

    def draw_guidelines(self):
        [self.canvas.create_line(50 + x * 50, 450, 50 + x * 50, 50, width=1, fill=st.guide_lines) for x in range(21)]

    def drawGraph(self):
        try:
            if self.s == 21:
                # new frame
                self.s = 1
                self.x2 = 50
                self.canvas.delete('t')  # only delete items tagged as temp
            x1 = self.x2
            y1 = self.y2 if self.y2 is not None else self.controller.get_value()
            self.x2 = 50 + self.s * 50
            self.y2 = self.controller.get_value()
            self.canvas.create_line(x1, y1, self.x2, [self.y2], fill=st.orange, width=2, tags='t')
            self.s += 1

            # if self.sensor == 't':
            #     self.mean.append(int(self.controller.get_raw_values()[1]['t']))
            #     print('Temperature mean: {0:.2f}'.format(sum(self.mean)/len(self.mean)))
            # if self.sensor == 'l':
            #     self.mean.append(int(self.controller.get_raw_values()[1]['l']))
            #     print('Light intensity mean: {0:.2f}'.format(sum(self.mean)/len(self.mean)))

        except tkinter.TclError:
            pass
