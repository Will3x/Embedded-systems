from tkinter import *
from controller import GraphController


class MainView:

    def __init__(self):
        root = Tk()
        root.title('GUI Test')
        root.resizable(False, False)
        self.canv_tempsen = self.create_canvas(root)
        self.canv_lightsen = self.create_canvas(root)

        self.center_window(root)
        self.graph_controller = GraphController.GraphController(self.canv_tempsen)
        self.graph_controller2 = GraphController.GraphController(self.canv_lightsen)
        self.addwidgets(root)
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

    def addwidgets(self, root):
        self.var1 = IntVar(root, 1)
        self.var2 = IntVar(root, 4)

        label_settings = LabelFrame(root, text='Instellingen', height=200, width=1065).place(relx=0.5, rely=0.85, anchor=CENTER)
        label_status = LabelFrame(root, text='Status', height=50, width=800).place(relx=0.38, rely=0.7, anchor=CENTER)
        label_manual = LabelFrame(root, text='Handmatig', height=50, width=250).place(relx=0.87, rely=0.7, anchor=CENTER)

        Radiobutton(root, text="Lichtsensor", indicatoron=False, variable=self.var1, offrelief=GROOVE, command=lambda: self.btnselect(self.var1), value=1, width=17).place(relx=0.440, rely=0.04, anchor=CENTER)
        Radiobutton(root, text="Temperatuursensor", indicatoron=False, variable=self.var1, offrelief=GROOVE, command=lambda: self.btnselect(self.var1), value=2, width=17).place(relx=0.56, rely=0.04, anchor=CENTER)

        Radiobutton(label_manual, text="AAN", indicatoron=False, variable=self.var2, command=lambda: self.btnselect(self.var2), offrelief=GROOVE, value=3, width=8).place(relx=0.867, rely=0.705, anchor=E)
        Radiobutton(label_manual, text="UIT", indicatoron=False, variable=self.var2, command=lambda: self.btnselect(self.var2), offrelief=GROOVE, value=4, width=8).place(relx=0.93, rely=0.705, anchor=E)

        entry_width = .79  # start position

        # self.entries = {}
        #
        # for x in range(1, 5):
        #     self.entries[f'entry{x}'] = 'Entry(self.label_settings, state=NORMAL, width=40).place(relx=0.30, rely=self.entry_width, anchor=CENTER)'
        #     exec(self.entries[f'entry{x}'])
        #     self.entry_width += .04
        #
        #
        # self.entry_width = .79  # start position

        """ TODO: CLEAN THIS MESS """
        self.entry1 = Entry(label_settings, width=40)
        self.entry1.place(relx=0.30, rely=entry_width, anchor=CENTER)

        self.entry2 = Entry(label_settings, width=40)
        self.entry2.place(relx=0.30, rely=entry_width+.04, anchor=CENTER)

        self.entry3 = Entry(label_settings, width=40)
        self.entry3.place(relx=0.30, rely=entry_width+.08, anchor=CENTER)

        self.entry4 = Entry(label_settings, width=40)
        self.entry4.place(relx=0.30, rely=entry_width+.12, anchor=CENTER)

        self.label1 = Label(label_settings, text='Uitrol buitentemperatuur')
        self.label1.place(relx=0.17, rely=entry_width, anchor=E)

        self.label2 = Label(label_settings, text='Oprol buitentemperatuur')
        self.label2.place(relx=0.17, rely=entry_width+.04, anchor=E)

        self.label3 = Label(label_settings, text='Uitrol lichtintensiteit')
        self.label3.place(relx=0.17, rely=entry_width+.08, anchor=E)

        self.label4 = Label(label_settings, text='Oprol lichtintensiteit')
        self.label4.place(relx=0.17, rely=entry_width+.12, anchor=E)

        self.manual1 = Label(label_settings, text='Uitrol afstand', state=DISABLED)
        self.manual1.place(relx=0.7, rely=entry_width, anchor=E)

        self.manual2 = Entry(label_settings, width=40, state=DISABLED)
        self.manual2.place(relx=0.83, rely=entry_width, anchor=CENTER)

        Button(root, text='Set', width=20).place(relx=0.873, rely=entry_width+.12, anchor=CENTER)

    def btnselect(self, var):
        if var.get() == 1:
            print('hiding canv2')
            if 'in' not in self.canv_lightsen.place_info():
                self.canv_lightsen.place(relx=0.5, rely=0.36, anchor=CENTER)
            self.canv_tempsen.place_forget()

        if var.get() == 2:
            print('hiding canv1')
            if 'in' not in self.canv_tempsen.place_info():
                self.canv_tempsen.place(relx=0.5, rely=0.36, anchor=CENTER)
            self.canv_lightsen.place_forget()

        if var.get() == 3:
            """ TODO: CLEAN THIS MESS """
            self.manual1.config(state=NORMAL)
            self.manual2.config(state=NORMAL)

            self.label1.config(state=DISABLED)
            self.label2.config(state=DISABLED)
            self.label3.config(state=DISABLED)
            self.label4.config(state=DISABLED)

            self.entry1.config(state=DISABLED)
            self.entry2.config(state=DISABLED)
            self.entry3.config(state=DISABLED)
            self.entry4.config(state=DISABLED)
            # for x, item in self.entries.items():
            #     exec(item.replace('state=NORMAL', 'state=DISABLED'))
            #     self.entry_width += .04


        if var.get() == 4:
            """ TODO: CLEAN THIS MESS """
            self.manual1.config(state=DISABLED)
            self.manual2.config(state=DISABLED)

            self.label1.config(state=NORMAL)
            self.label2.config(state=NORMAL)
            self.label3.config(state=NORMAL)
            self.label4.config(state=NORMAL)

            self.entry1.config(state=NORMAL)
            self.entry2.config(state=NORMAL)
            self.entry3.config(state=NORMAL)
            self.entry4.config(state=NORMAL)

            # for x, item in self.entries.items():
            #     exec(item.replace('state=NORMAL', 'state=DISABLED'))
            #     self.entry_width += .04


    def center_window(self, mainview):
        window_width = 1100
        window_height = 850

        screen_width = mainview.winfo_screenwidth()
        screen_height = mainview.winfo_screenheight()

        x = screen_width / 2 - window_width / 2
        y = screen_height / 2 - window_height / 2
        mainview.geometry("%dx%d+%d+%d" % (window_width, window_height, x, y))

