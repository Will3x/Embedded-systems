from tkinter import *
from controller import GraphController, EventController


class MainView(Tk):

    def __init__(self, dashboard):
        Tk.__init__(self)
        self.title('GUI Test')
        self.resizable(False, False)
        self.make_topmost()
        self.dashboard = dashboard

        self.canv_tempsen = self.create_canvas()
        self.canv_lightsen = self.create_canvas()

        self.center_window()

        self.graph_controller = GraphController.GraphController(self.canv_tempsen)
        self.graph_controller2 = GraphController.GraphController(self.canv_lightsen)

        self.event_controller = EventController.EventController(self)
        self.addwidgets()
        self.start()

    def on_exit(self):
        self.wm_withdraw()

    def close(self):
        self.wm_withdraw()

    def go_back(self):
        self.on_exit()
        self.dashboard.show_window()

    def show_window(self):
        print('opening again :)')
        self.deiconify()

    def start(self):
        self.graph_controller.startgraph()
        self.graph_controller2.startgraph()
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        # self.wm_withdraw()


    def make_topmost(self):
        """Makes this window the topmost window"""
        self.lift()
        self.attributes("-topmost", 1)
        self.attributes("-topmost", 0)

    def create_canvas(self):
        """ Creates and adds a canvas. This canvas is used to display a graph, hence two canvases are made in the
        constructor """
        canvas = Canvas(self, bg='grey90', height=500, width=1100)
        canvas.create_line(50, 450, 1050, 450, width=1)  # x-axis
        canvas.create_line(50, 450, 50, 50, width=1)  # y-axis
        canvas.create_text((1150 / 2, 570), text="time/steps")
        canvas.create_text((50, 30), text="value")
        canvas.place(relx=0.5, rely=0.36, anchor=CENTER)
        return canvas

    def addwidgets(self):
        """ Creates and adds widgets to the frame, such as buttons, labels, and input fields. """
        var1 = IntVar(self, 1)
        var2 = IntVar(self, 4)

        LabelFrame(self, text='Instellingen', height=200, width=1065).place(relx=0.5, rely=0.85, anchor=CENTER)

        label_status = LabelFrame(self, text='Status', height=55, width=800).place(relx=0.38, rely=0.695, anchor=CENTER)

        LabelFrame(self, text='Handmatig', height=55, width=250).place(relx=0.87, rely=0.695, anchor=CENTER)

        Radiobutton(self, text="Lichtsensor", indicatoron=False, variable=var1, offrelief=GROOVE,
                    command=lambda: self.event_controller.buttonclick_event(var1),
                    value=1, width=17).place(relx=0.440, rely=0.04, anchor=CENTER)

        Radiobutton(self, text="Temperatuursensor", indicatoron=False, variable=var1, offrelief=GROOVE,
                    command=lambda: self.event_controller.buttonclick_event(var1),
                    value=2, width=17).place(relx=0.56, rely=0.04, anchor=CENTER)

        Radiobutton(self, text="AAN", indicatoron=False, variable=var2,
                    command=lambda: self.event_controller.buttonclick_event(var2), offrelief=GROOVE,
                    value=3, width=10).place(relx=0.865, rely=0.7, anchor=E)

        Radiobutton(self, text="UIT", indicatoron=False, variable=var2,
                    command=lambda: self.event_controller.buttonclick_event(var2), offrelief=GROOVE,
                    value=4, width=10).place(relx=0.94, rely=0.7, anchor=E)

        y_pos = .778  # start position

        entries = []
        labels_text = ['Uitrol buitentemperatuur', 'Oprol buitentemperatuur', 'Uitrol lichtintensiteit', 'Oprol lichtintensiteit']

        # Adding buttons dynamically.
        for x in range(1, 5):
            entries.insert(0, f'self.entry{x} = Entry(self, width=40)')
            entries.insert(1, f'self.entry{x}.place(relx=0.18, rely={y_pos:.2f}, anchor=W)')
            entries.insert(2, f'self.label{x} = Label(self, text="{labels_text[x-1]}")')
            entries.insert(3, f'self.label{x}.place(relx=0.17, rely={y_pos:.2f}, anchor=E)')
            for i in range(4):
                exec(entries[i])
            y_pos += .04

        y_pos = .778  # reset start position
        button_width = 20

        self.manual1 = Label(self, text='Uitrol afstand', state=DISABLED)
        self.manual1.place(relx=0.7, rely=y_pos, anchor=E)

        self.manual2 = Entry(self, width=40, state=DISABLED)
        self.manual2.place(relx=0.83, rely=y_pos, anchor=CENTER)

        self.manual_btn1 = Button(self, text='Uitrollen', width=button_width, relief=GROOVE, state=DISABLED)
        self.manual_btn1.place(relx=0.8, rely=y_pos+.12, anchor=E)

        self.manual_btn2 = Button(self, text='Oprollen', width=button_width, relief=GROOVE, state=DISABLED)
        self.manual_btn2.place(relx=.942, rely=y_pos+.12, anchor=E)

        self.setbtn2 = Button(self, text='Set', width=button_width, fg='black', bg='gray90', state=DISABLED, relief=GROOVE)
        self.setbtn2.place(relx=0.873, rely=y_pos+.04, anchor=CENTER)

        self.setbtn1 = Button(self, text='Set', width=button_width, bg='dodger blue', fg='white', relief=GROOVE)
        self.setbtn1.place(relx=0.265, rely=y_pos + .16, anchor=W)

        self.status_label = Label(self, text='ROLLUIK IS OPGEROLD', font='Roboto 12 bold' ,fg='green').place(relx=0.4, rely=0.7, anchor=CENTER)

        self.btn_return = Button(self, text="Return",
                            width=button_width, command=self.go_back,
                            bg='dodger blue', fg='white', relief=GROOVE)
        self.btn_return.place(relx=0.03, rely=0.04, anchor=W)

    @property
    def canvas(self):
        return self.canv_lightsen, self.canv_tempsen

    def center_window(self):
        """ Centers the application according to current screen width and height when opening this program. """
        window_width = 1100
        window_height = 850

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = screen_width / 2 - window_width / 2
        y = screen_height / 2 - window_height / 2
        self.geometry("%dx%d+%d+%d" % (window_width, window_height, x, y))

