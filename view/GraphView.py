from tkinter import TclError
import Style as st


class GraphView:

    def __init__(self, canvas, sensor, controller):
        self.canvas = canvas
        self.sensor = sensor
        self.controller = controller
        self.s, self.x2, self.y2 = 0, 50, None
        self.line_t, self.line_l, self.txt_l, self.txt_t = None, None, None, None
        self.add_to_canvas(sensor, 50, 450)

    def draw_graph(self):
        """ Draws graph on canvas. Gets called by GraphController.update_graph(). """
        try:
            if self.s == 21:
                self.s = 1
                self.x2 = 50
                self.canvas.delete('t')
            x1 = self.x2
            y1 = self.controller.calculate_graph_line() if self.y2 is None else self.y2
            self.x2 = 50 + self.s * 50
            self.y2 = self.controller.get_mean()
            self.canvas.create_line(x1, y1, self.x2, [self.y2], fill=st.orange, width=2, tags='t')
            self.s += 1
        except TclError:
            pass

    def draw_borders(self, roll_out, roll_in):
        """ Deletes the old and draws the new blue border lines and texts on both graphs that indicate when the
        shutter should roll out or roll back in. """
        border = {'Roll out': roll_out, 'Roll in': roll_in}

        # First delete existing lines and texts.
        if self.line_l is not None:
            [self.canvas.delete(x) for x in self.line_l]
            [self.canvas.delete(x) for x in self.txt_l]
        if self.line_t is not None:
            [self.canvas.delete(x) for x in self.line_t]
            [self.canvas.delete(x) for x in self.txt_t]

        # Secondly, draw the (new) lines and create new texts.
        if self.sensor == 'l':
            self.line_l = [self.canvas.create_line(50, y, 1050, y, fill=st.border_blue) for x, y in border.items()]
            self.txt_l = [self.canvas.create_text(1020, y-10, text=x, fill=st.border_blue) for x, y in border.items()]

        if self.sensor == 't':
            self.line_t = [self.canvas.create_line(50, y, 1050, y, fill=st.border_blue) for x, y in border.items()]
            self.txt_t = [self.canvas.create_text(1020, y - 10, text=x, fill=st.border_blue) for x, y in border.items()]

    def change_border_state(self, state):
        """ Changes state of current drawn border. State will either be 'normal' or 'hidden' making the border
        either visible or invisible respectively. """
        for x in range(2):
            if self.sensor == 'l':
                self.canvas.itemconfigure(self.line_l[x], state=state)
                self.canvas.itemconfigure(self.txt_l[x], state=state)

            if self.sensor == 't':
                self.canvas.itemconfigure(self.line_t[x], state=state)
                self.canvas.itemconfigure(self.txt_t[x], state=state)

    def add_to_canvas(self, sensor, roll_in, roll_out):
        """ Called once. Draws the foundation for the graph like the guidelines, scale labels and canvas title. """
        center_canvas = (int(self.canvas['width']) / 2, 25)

        if sensor == 'l':
            count = 100
            self.canvas.create_text(center_canvas, text="Light intensity in %", fill=st.label_white)
            for y in range(roll_in, roll_out + 25, 40):
                self.canvas.create_line(50, y, 1050, y, fill=st.guide_lines)
                self.canvas.create_text(30, y, text=count, fill=st.label_white)
                count -= 10

        if sensor == 't':
            count = 32
            self.canvas.create_text(center_canvas, text="Temperature in °C", fill=st.label_white)
            for y in range(roll_in, roll_out + 25, 25):
                self.canvas.create_line(50, y, 1050, y, fill=st.guide_lines)
                self.canvas.create_text(30, y, text=count, fill=st.label_white)
                count -= 2

        self.draw_guidelines()

    def draw_guidelines(self):
        [self.canvas.create_line(50 + x * 50, 450, 50 + x * 50, 50, fill=st.guide_lines) for x in range(21)]
