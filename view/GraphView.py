from random import randint, choice


class GraphView:

    def __init__(self, canvas):
        self.canvas = canvas
        self.s = 1
        self.x2 = 50
        color = ["red", "orange", "green", "blue", "violet"]
        self.color = choice(color)
        self.y2 = self.value_to_y(randint(0, 80))

    def value_to_y(self, val):
        return 450 - 5 * val

    def drawGraph(self):
        global s, x2, y2
        if self.s == 21:
            # new frame
            self.s = 1
            self.x2 = 50
            self.canvas.delete('temp')  # only delete items tagged as temp
        x1 = self.x2
        y1 = self.y2
        self.x2 = 50 + self.s * 50
        self.y2 = self.value_to_y(randint(0, 80))
        self.canvas.create_line(x1, y1, self.x2, self.y2, fill=self.color, width=2, tags='temp')
        self.s += 1
        self.canvas.after(300, self.drawGraph)
