from tkinter import *
from controller import GraphController, EventController


class MainView(Toplevel):

    def __init__(self, dashboard, name):
        Toplevel.__init__(self)
        self.title(name)
        self.resizable(False, False)
        self.make_topmost()

        self.dashboard = dashboard

        # Styling
        self.bg_color = '#2E3643'
        self.fg_color = 'grey90'
        self.btn_color = 'dodger blue'

        self.config(bg=self.bg_color)

        self.canv_temp = self.create_canvas()
        self.canv_light = self.create_canvas()

        self.graph_controller = GraphController.GraphController(self.canv_temp, 't', name)
        self.graph_controller2 = GraphController.GraphController(self.canv_light, 'l', name)

        self.center_window()

        self.event_controller = EventController.EventController(self)
        self.addwidgets()
        self.start()

    def tick(self):
        """ Gets called from Dashboardview.tick() """
        self.graph_controller.updategraph()
        self.graph_controller2.updategraph()

    def minimize_window(self):
        self.iconify()

    def hide_window(self):
        self.wm_withdraw()

    def close(self):
        self.destroy()

    def show_window(self):
        self.deiconify()

    def start(self):
        self.protocol("WM_DELETE_WINDOW", self.hide_window)
        # self.wm_withdraw()

    def make_topmost(self):
        """Makes this window the topmost window"""
        self.lift()
        self.attributes("-topmost", 1)
        self.attributes("-topmost", 0)

    def create_canvas(self):
        """ Creates and adds a canvas. This canvas is used to display a graph, hence two canvases are made in the
        constructor """
        canvas = Canvas(self, height=480, width=1100, bg='#242A36', highlightthickness=0)
        canvas.create_line(50, 450, 1050, 450, width=2, fill='#525D6D')  # x-axis
        canvas.create_line(50, 450, 50, 50, width=2, fill='#525D6D')  # y-axis
        canvas.place(relx=0.5, rely=0.37, anchor=CENTER)
        return canvas

    def addwidgets(self):
        """ Creates and adds widgets to the frame, such as buttons, labels, and input fields. """
        var1 = IntVar(self, 1)
        var2 = IntVar(self, 4)

        LabelFrame(self, text='Settings', height=200, width=1065, fg=self.fg_color,
                   bg=self.bg_color).place(relx=0.5, rely=0.85, anchor=CENTER)

        LabelFrame(self, text='Status', height=55, width=800, fg=self.fg_color,
                   bg=self.bg_color).place(relx=0.38, rely=0.695, anchor=CENTER)

        LabelFrame(self, text='Manual', height=55, width=250, fg=self.fg_color,
                   bg=self.bg_color).place(relx=0.87, rely=0.695, anchor=CENTER)

        radio1 = Radiobutton(self, text="Light sensor", indicatoron=False, variable=var1, borderwidth=0,
                             fg='white',
                             command=lambda: self.event_controller.buttonclick_event(var1), height=2,
                             selectcolor=self.btn_color,
                             value=1, width=20, bg="#444D5F")
        radio1.place(relx=0.435, rely=0.05, anchor=CENTER)

        radio2 = Radiobutton(self, text="Temperature sensor", indicatoron=False, variable=var1, borderwidth=0,
                             command=lambda: self.event_controller.buttonclick_event(var1), height=2,
                             selectcolor=self.btn_color,
                             value=2, width=20, bg="#444D5F", fg='white')
        radio2.place(relx=0.565, rely=0.05, anchor=CENTER)

        self.manual1 = Radiobutton(self, text="AAN", indicatoron=False, variable=var2,
                                   command=lambda: self.event_controller.buttonclick_event(var2), borderwidth=0,
                                   selectcolor=self.btn_color, bg="#444D5F", height=2,
                                   value=3, width=10)
        self.manual1.place(relx=0.865, rely=0.7, anchor=E)

        self.manual2 = Radiobutton(self, text="UIT", indicatoron=False, variable=var2,
                                   command=lambda: self.event_controller.buttonclick_event(var2), borderwidth=0,
                                   bg="#444D5F", height=2, value=4, width=10)
        self.manual2.place(relx=0.94, rely=0.7, anchor=E)

        y_pos = .778  # start position

        entries = []
        labels_text = ['Uitrol buitentemperatuur', 'Oprol buitentemperatuur', 'Uitrol lichtintensiteit',
                       'Oprol lichtintensiteit']

        # Adding buttons dynamically.
        for x in range(1, 5):
            entries.insert(0, f'self.entry{x} = Entry(self, width=40)')
            entries.insert(1, f'self.entry{x}.place(relx=0.18, rely={y_pos:.2f}, anchor=W)')
            entries.insert(2, f'self.label{x} = Label(self, text="{labels_text[x-1]}", bg=self.bg_color, '
                              f'fg=self.fg_color)')
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

        self. manual_btn1 = Button(self, text='Uitrollen', width=button_width, height=2, borderwidth=0, state=DISABLED)
        self.manual_btn1.place(relx=0.8, rely=y_pos + .12, anchor=E)

        self.manual_btn2 = Button(self, text='Oprollen', width=button_width, height=2, borderwidth=0, state=DISABLED)
        self.manual_btn2.place(relx=.942, rely=y_pos + .12, anchor=E)

        self.setbtn2 = Button(self, text='Set', width=button_width, fg='black', bg='gray90', state=DISABLED,
                         borderwidth=0)
        self.setbtn2.place(relx=0.873, rely=y_pos + .04, anchor=CENTER)

        self.setbtn1 = Button(self, text='Set', width=button_width, bg='dodger blue', fg=self.fg_color, borderwidth=0)
        self.setbtn1.place(relx=0.265, rely=y_pos + .16, anchor=W)

        status_label = Label(self, text='ROLLUIK IS OPGEROLD', font='Roboto 12 bold', fg='green',
                             bg=self.bg_color).place(relx=0.4, rely=0.7, anchor=CENTER)

        btn_return = Button(self, text="Go back",
                            width=button_width, command=self.hide_window,
                            bg='#444D5F', fg=self.fg_color, borderwidth=0, height=2)
        btn_return.place(relx=0, rely=0.05, anchor=W)

    @property
    def canvas(self):
        return self.canv_light, self.canv_temp

    def make_background(self):
        filename = PhotoImage(file="images/bg-device.png")
        background_label = Label(self, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        return filename

    def center_window(self):
        """ Centers the application according to current screen width and height when opening this program. """
        window_width = 1100
        window_height = 850

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = screen_width / 2 - window_width / 2
        y = (screen_height / 2 - window_height / 2) - 40
        self.geometry("%dx%d+%d+%d" % (window_width, window_height, x, y))
        #test