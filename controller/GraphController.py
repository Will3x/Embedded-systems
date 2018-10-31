from view import GraphView as view
from model import GraphModel as model


class GraphController:

    def __init__(self, canvas):
        self.view = view.GraphView(canvas)
        self.model = model.GraphModel()

    def startgraph(self):
        self.view.drawGraph()
