from tkinter import *
from controller import GraphController, EventController
import Style as st
import Base_values as ba


class MainView(Toplevel):

    def __init__(self, dashboard, name):
        Toplevel.__init__(self)
        self.title(name)
        self.resizable(False, False)
        self.make_topmost()

        self.dashboard = dashboard

        self.config(bg=st.mainview_bg)

        self.canv_temp = self.create_base_canvas()
        self.canv_light = self.create_base_canvas()

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
        self.update_label()

    def minimize_window(self):
        self.iconify()

    def hide_window(self):
        self.wm_withdraw()

    def close(self):
        self.destroy()

    def show_window(self):
        self.deiconify()

    def start(self):
        self.graph_controller.draw_borders(self.entry2.get(), self.entry1.get())
        self.graph_controller2.draw_borders(self.entry4.get(), self.entry3.get())
        self.protocol("WM_DELETE_WINDOW", self.hide_window)
        # self.wm_withdraw()

    def make_topmost(self):
        """Makes this window the topmost window"""
        self.lift()
        self.attributes("-topmost", 1)
        self.attributes("-topmost", 0)

    def create_base_canvas(self):
        """ Creates and adds a canvas. This canvas is used to display a graph, hence two canvases are made in the
        constructor """
        canvas = Canvas(self, height=480, width=1100, bg=st.canv_bg, highlightthickness=0)
        canvas.create_line(50, 450, 1050, 450, width=2, fill=st.canv_line)  # x-axis
        canvas.create_line(50, 450, 50, 50, width=2, fill=st.canv_line)  # y-axis
        canvas.place(relx=0.5, rely=0.37, anchor=CENTER)
        return canvas

    def button_click(self):
        self.event_controller.write(int(self.wm_title()[7:8]), 3, self.entry1.get(), self.entry2.get(),
                                    self.entry3.get(), self.entry4.get())
        self.graph_controller.draw_borders(self.entry2.get(), self.entry1.get())
        self.graph_controller2.draw_borders(self.entry4.get(), self.entry3.get())

    def update_label(self):
        values = self.event_controller.get_values()
        self.status_label.config(text='{}cm'.format(values[int(self.wm_title()[7:8])]['a']))

    def addwidgets(self):
        """ Creates and adds widgets to the frame, such as buttons, labels, and input fields. """
        var1 = IntVar(self, 1)
        var2 = IntVar(self, 4)

        button_width = 15

        Button(self, width=92, disabledforeground=st.fg_white, bg=st.panel_bg, state=DISABLED, borderwidth=0, height=2).place(relx=0.11, rely=0.7, anchor=W)
        Button(self, text="Status", width=button_width, disabledforeground=st.fg_white, bg=st.panel_title_bg, state=DISABLED, borderwidth=0, height=2).place(relx=0.03, rely=0.7, anchor=W)

        Button(self, text="Manual mode", width=button_width, disabledforeground=st.fg_white, bg=st.panel_title_bg, state=DISABLED, borderwidth=0, height=2).place(relx=0.831, rely=0.7, anchor=E)

        Button(self, width=63, disabledforeground=st.fg_white, bg=st.panel_bg, fg=st.fg_white, state=DISABLED, borderwidth=0, height=12).place(relx=0.11, rely=0.86, anchor=W)
        Button(self, text="Settings\nauto", width=button_width, disabledforeground=st.fg_white, bg=st.panel_title_bg, state=DISABLED, borderwidth=0, height=12).place(relx=0.03, rely=0.86, anchor=W)

        Button(self, width=50, disabledforeground=st.fg_white, bg=st.panel_bg, fg=st.fg_white, state=DISABLED, borderwidth=0, height=12).place(relx=0.97, rely=0.86, anchor=E)
        Button(self, text="Settings\nmanual", width=button_width, disabledforeground=st.fg_white, bg=st.panel_title_bg, state=DISABLED, borderwidth=0, height=12).place(relx=0.65, rely=0.86, anchor=E)

        radio1 = Radiobutton(self, text="Light sensor", indicatoron=False, variable=var1, borderwidth=0,
                             fg=st.fg_white,
                             command=lambda: self.event_controller.buttonclick_event(var1), height=2,
                             selectcolor=st.btn_bg_blue,
                             value=1, width=20, bg=st.btn_bg_grey)
        radio1.place(relx=0.435, rely=0.05, anchor=CENTER)

        radio2 = Radiobutton(self, text="Temperature sensor", indicatoron=False, variable=var1, borderwidth=0,
                             command=lambda: self.event_controller.buttonclick_event(var1), height=2,
                             selectcolor=st.btn_bg_blue,
                             value=2, width=20, bg=st.btn_bg_grey, fg=st.fg_white)
        radio2.place(relx=0.565, rely=0.05, anchor=CENTER)

        self.manual_btn_on = Radiobutton(self, text="ON", indicatoron=False, variable=var2,
                                         command=lambda: self.event_controller.buttonclick_event(var2), borderwidth=0,
                                         selectcolor=st.btn_bg_blue, fg=st.fg_white, bg=st.btn_bg_grey, height=2,
                                         value=3, width=10)
        self.manual_btn_on.place(relx=0.901, rely=0.7, anchor=E)

        self.manual_btn2 = Radiobutton(self, text="OFF", indicatoron=False, variable=var2,
                                   command=lambda: self.event_controller.buttonclick_event(var2), borderwidth=0,
                                   selectcolor=st.btn_bg_blue, fg=st.fg_white, bg=st.btn_bg_grey, height=2, value=4, width=10)
        self.manual_btn2.place(relx=0.97, rely=0.7, anchor=E)

        y_pos = .785  # start position

        entries = []
        labels_text = ['Roll out on temperature', 'Roll in on temperature', 'Roll out on lightintensity',
                       'Roll in on lightintensity']
        default_values = [ba.temp_rollo, ba.temp_rolli, ba.light_rollo, ba.temp_rolli]


        # Adding buttons dynamically.
        for x in range(1, len(labels_text)+1):
            entries.insert(0, f'self.entry{x} = Entry(self, width=33, borderwidth=0)')
            entries.insert(1, f'self.entry{x}.insert(0, default_values[{x-1}])')
            entries.insert(2, f'self.entry{x}.place(relx=0.3, rely={y_pos:.4f}, anchor=W)')
            entries.insert(3, f'self.entry{x}.config(disabledbackground=st.btn_bg_grey)')
            entries.insert(4, f'self.label{x} = Label(self, text="{labels_text[x-1]}", bg=st.panel_bg, '
                              f'fg=st.fg_white, disabledforeground=st.btn_bg_grey)')
            entries.insert(5, f'self.label{x}.place(relx=0.28, rely={y_pos:.4f}, anchor=E)')
            for i in range(len(entries)):
                exec(entries[i])

            y_pos += .035

        y_pos = .785  # reset start position

        self.manual1 = Label(self, text='Uitrol afstand', disabledforeground=st.btn_bg_grey, bg=st.panel_bg, fg=st.fg_white, state=DISABLED)
        self.manual1.place(relx=0.75, rely=y_pos, anchor=E)

        self.manual2 = Entry(self, width=33, borderwidth=0)
        self.manual2.insert(0, ba.roll_out_dist)
        self.manual2.config(disabledbackground=st.btn_bg_grey, state=DISABLED)
        self.manual2.place(relx=0.94, rely=y_pos, anchor=E)

        self.manual_btn_on = Button(self, text='Roll out', bg=st.btn_bg_grey, fg=st.fg_white, width=button_width, height=2, borderwidth=0, state=DISABLED)
        self.manual_btn_on.place(relx=0.83, rely=y_pos + .14, anchor=E)

        self.manual_btn2 = Button(self, text='Roll in', bg=st.btn_bg_grey, fg=st.fg_white, width=button_width, height=2, borderwidth=0, state=DISABLED)
        self.manual_btn2.place(relx=.94, rely=y_pos + .14, anchor=E)

        self.setbtn1 = Button(self, text='Set', width=button_width, bg=st.btn_bg_blue, fg=st.fg_white,
                              borderwidth=0, command=self.button_click)
        self.setbtn1.place(relx=0.383, rely=y_pos + .15, anchor=W)

        self.setbtn2 = Button(self, text='Set', width=button_width, bg=st.btn_bg_grey, fg=st.fg_white, state=DISABLED,
                         borderwidth=0, command=lambda: self.event_controller.write(int(self.wm_title()[7:8]), 7, self.manual2.get()))
        self.setbtn2.place(relx=0.94, rely=y_pos + .04, anchor=E)

        self.status_label = Label(self, fg=st.btn_bg_blue, bg=st.panel_bg)
        self.status_label.place(relx=0.15, rely=0.7, anchor=W)

        btn_return = Button(self, text="Go back",
                            width=button_width, command=self.hide_window,
                            bg=st.btn_bg_grey, fg=st.fg_white, borderwidth=0, height=2)
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
