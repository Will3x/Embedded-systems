import tkinter
import Style as st


class GraphView:

    def __init__(self, canvas, sensor, controller):
        self.canvas = canvas
        self.s, self.x2, self.y2 = 0, 50, None
        self.line_t, self.line_l, self.txt_l, self.txt_t = None, None, None, None
        self.sensor = sensor
        self.controller = controller
        self.add_to_canvas(sensor, 50, 450)

    def add_to_canvas(self, sensor, roll_in, roll_out):
        center_canvas = (int(self.canvas['width']) / 2, 25)

        if sensor == 'l':
            count = 100
            self.canvas.create_text(center_canvas, text="Light intensity in %", fill=st.label_white)
            for y in range(roll_in, roll_out + 25, 40):
                self.canvas.create_line(50, y, 1050, y, width=1, fill=st.guide_lines)
                self.canvas.create_text(30, y, text=count, fill=st.label_white)
                count -= 10

        if sensor == 't':
            count = 32
            self.canvas.create_text(center_canvas, text="Temperature in °C", fill=st.label_white)
            for y in range(roll_in, roll_out + 25, 25):
                self.canvas.create_line(50, y, 1050, y, width=1, fill=st.guide_lines)
                self.canvas.create_text(30, y, text=count, fill=st.label_white)
                count -= 2

        self.draw_guidelines()

    def draw_borders(self, roll_out, roll_in):
        if self.line_l is not None and self.txt_l is not None:
            [self.canvas.delete(x) for x in self.line_l]
            [self.canvas.delete(x) for x in self.txt_l]
        if self.line_t is not None and self.txt_t is not None:
            [self.canvas.delete(x) for x in self.line_t]
            [self.canvas.delete(x) for x in self.txt_t]

        border = {'Roll in': roll_in, 'Roll out': roll_out}

        if self.sensor == 'l':
            self.line_l = [self.canvas.create_line(50, y, 1050, y, width=1, fill=st.border_blue)
                           for x, y in border.items()]
            self.txt_l = [self.canvas.create_text(1020, y-10, text=x, fill=st.border_blue)
                          for x, y in border.items()]

        if self.sensor == 't':
            self.line_t = [self.canvas.create_line(50, y, 1050, y, width=1, fill=st.border_blue)
                           for x, y in border.items()]
            self.txt_t = [self.canvas.create_text(1020, y - 10, text=x, fill=st.border_blue)
                          for x, y in border.items()]

    def change_border_state(self, state):
        for x in range(2):
            if self.sensor == 'l':
                self.canvas.itemconfigure(self.line_l[x], state=state)
                self.canvas.itemconfigure(self.txt_l[x], state=state)

            if self.sensor == 't':
                self.canvas.itemconfigure(self.line_t[x], state=state)
                self.canvas.itemconfigure(self.txt_t[x], state=state)

    def draw_guidelines(self):
        [self.canvas.create_line(50 + x * 50, 450, 50 + x * 50, 50, width=1, fill=st.guide_lines) for x in range(21)]

    def draw_graph(self):
        try:
            if self.s == 21:
                self.s = 1
                self.x2 = 50
                self.canvas.delete('t')
            x1 = self.x2
            y1 = self.y2 if self.y2 is not None else self.controller.get_mean()
            self.x2 = 50 + self.s * 50
            self.y2 = self.controller.get_mean()
            self.canvas.create_line(x1, y1, self.x2, [self.y2], fill=st.orange, width=2, tags='t')
            self.s += 1
        except tkinter.TclError:
            pass
