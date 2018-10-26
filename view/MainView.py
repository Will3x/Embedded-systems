from tkinter import *
from controller import GraphController


class MainView:

    def __init__(self):
        root = Tk()
        root.title('GUI Test')
        root.resizable(False, False)
        canvas = self.create_canvas(root)
        self.center_window(root)
        self.graph_controller = GraphController.GraphController(canvas)
        self.addwidgets(root)
        self.start(root)

    def start(self, root):
        self.graph_controller.updateview()
        root.mainloop()

    def create_canvas(self, root):
        canvas = Canvas(root, bg='white', height=500, width=1100)
        canvas.create_line(50, 450, 1050, 450, width=1)  # x-axis
        canvas.create_line(50, 450, 50, 50, width=1)  # y-axis
        canvas.create_text((1150 / 2, 570), text="time/steps")
        canvas.create_text((50, 30), text="value")
        canvas.place(relx=0.5, rely=0.39, anchor=CENTER)
        return canvas

    def addwidgets(self, root):
        var1 = StringVar()
        var2 = StringVar()

        var1.set(0)
        var2.set(0)

        Radiobutton(root, text="Lichtsensor", indicatoron=False, variable='var1', state=ACTIVE, value=1, width=17).place(relx=0.440, rely=0.05, anchor=CENTER)
        Radiobutton(root, text="Temperatuursensor", indicatoron=False, variable='var1', value=0, width=17).place(relx=0.56, rely=0.05, anchor=CENTER)

        Radiobutton(root, text="ON", indicatoron=False, variable='var2', value=1, width=8).place(relx=0.837, rely=0.75, anchor=CENTER)
        Radiobutton(root, text="OFF", indicatoron=False, variable='var2', value=0, width=8).place(relx=0.9, rely=0.75, anchor=CENTER)
        Button(root, text='Set').place(relx=0.9, rely=0.9, anchor=CENTER)
        pass

    def center_window(self, mainview):
        window_width = 1100
        window_height = 800

        screen_width = mainview.winfo_screenwidth()
        screen_height = mainview.winfo_screenheight()

        x = screen_width / 2 - window_width / 2
        y = screen_height / 2 - window_height / 2
        mainview.geometry("%dx%d+%d+%d" % (window_width, window_height, x, y))

