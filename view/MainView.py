from tkinter import *
from controller import GraphController


class MainView:

    def __init__(self):
        root = Tk()
        root.title('GUI Test')
        root.resizable(False, False)
        canv_tempsen = self.create_canvas(root)
        canv_lightsen = self.create_canvas(root)

        self.center_window(root)
        self.graph_controller = GraphController.GraphController(canv_tempsen)
        self.graph_controller2 = GraphController.GraphController(canv_lightsen)
        self.addwidgets(root, canv_lightsen, canv_tempsen)
        self.start(root)

    def start(self, root):
        self.graph_controller.updateview()
        self.graph_controller2.updateview()
        root.mainloop()

    def create_canvas(self, root):
        canvas = Canvas(root, bg='white', height=500, width=1100)
        canvas.create_line(50, 450, 1050, 450, width=1)  # x-axis
        canvas.create_line(50, 450, 50, 50, width=1)  # y-axis
        canvas.create_text((1150 / 2, 570), text="time/steps")
        canvas.create_text((50, 30), text="value")
        canvas.place(relx=0.5, rely=0.36, anchor=CENTER)
        return canvas

    def addwidgets(self, root, canv_lightsen, canv_tempsen):
        var1 = StringVar(root, 1)
        var2 = StringVar(root, 4)

        label_settings = LabelFrame(root, text='Instellingen', height=200, width=1065).place(relx=0.5, rely=0.85, anchor=CENTER)
        label_status = LabelFrame(root, text='Status', height=50, width=800).place(relx=0.38, rely=0.7, anchor=CENTER)
        label_manual = LabelFrame(root, text='Manual mode', height=50, width=250).place(relx=0.87, rely=0.7, anchor=CENTER)

        Radiobutton(root, text="Lichtsensor", indicatoron=False, variable=var1, offrelief=GROOVE, command=lambda: self.btnselect(var1, canv_lightsen, canv_tempsen), value=1, width=17).place(relx=0.440, rely=0.04, anchor=CENTER)
        Radiobutton(root, text="Temperatuursensor", indicatoron=False, variable=var1, offrelief=GROOVE, command=lambda: self.btnselect(var1, canv_tempsen, canv_lightsen), value=2, width=17).place(relx=0.56, rely=0.04, anchor=CENTER)

        Radiobutton(label_manual, text="ON", indicatoron=False, variable=var2, offrelief=GROOVE, value=3, width=8).place(relx=0.837, rely=0.705, anchor=CENTER)
        Radiobutton(label_manual, text="OFF", indicatoron=False, variable=var2, offrelief=GROOVE, value=4, width=8).place(relx=0.9, rely=0.705, anchor=CENTER)

        entry_width = .79  # start position
        Entry(label_settings, width=40).place(relx=0.30, rely=entry_width, anchor=CENTER)
        Entry(label_settings, width=40).place(relx=0.30, rely=entry_width+.04, anchor=CENTER)
        Entry(label_settings, width=40).place(relx=0.30, rely=entry_width+.08, anchor=CENTER)
        Entry(label_settings, width=40).place(relx=0.30, rely=entry_width+.12, anchor=CENTER)

        Label(label_settings, text='Uitrol buitentemperatuur').place(relx=0.17, rely=entry_width, anchor=E)
        Label(label_settings, text='Oprol buitentemperatuur').place(relx=0.17, rely=entry_width+.04, anchor=E)
        Label(label_settings, text='Uitrol lichtintensiteit').place(relx=0.17, rely=entry_width+.08, anchor=E)
        Label(label_settings, text='Oprol lichtintensiteit').place(relx=0.17, rely=entry_width+.12, anchor=E)

        Label(label_settings, text='Uitrol afstand', state=DISABLED).place(relx=0.7, rely=entry_width, anchor=E)
        Entry(label_settings, width=40, state=DISABLED).place(relx=0.83, rely=entry_width, anchor=CENTER)

        Button(root, text='Set', width=20).place(relx=0.873, rely=entry_width+.12, anchor=CENTER)

    def btnselect(self, var, canv1, canv2):
        if int(var.get()) == 1:
            print('hiding canv2')
            if 'in' not in canv1.place_info():
                canv1.place(relx=0.5, rely=0.36, anchor=CENTER)
            canv2.place_forget()

        if int(var.get()) == 2:
            print('hiding canv1')
            if 'in' not in canv1.place_info():
                canv1.place(relx=0.5, rely=0.36, anchor=CENTER)
            canv2.place_forget()


    # def canvas_hide(self, canvas):
    #     canvas.pack_forget()

    def center_window(self, mainview):
        window_width = 1100
        window_height = 850

        screen_width = mainview.winfo_screenwidth()
        screen_height = mainview.winfo_screenheight()

        x = screen_width / 2 - window_width / 2
        y = screen_height / 2 - window_height / 2
        mainview.geometry("%dx%d+%d+%d" % (window_width, window_height, x, y))

