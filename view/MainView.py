from tkinter import *
from controller import GraphController as gc, MainViewController as mc
import Style as st
import Base_values as ba


class MainView(Toplevel):

    def __init__(self, name):
        Toplevel.__init__(self)
        self.center_window()
        self.hide_window()
        self.title(name)
        self.resizable(False, False)
        self.config(bg=st.mainview_bg)

        self.device_id = int(name[7:8])

        canv_temp = self.create_base_canvas()
        canv_light = self.create_base_canvas()

        gr_controller_t = gc.GraphController(canv_temp, 't', name)
        gr_controller_l = gc.GraphController(canv_light, 'l', name)
        mv_controller = mc.MainViewController(self, self.device_id, gr_controller_t, gr_controller_l)

        self.canvases = [canv_temp, canv_light]
        self.controllers = [[gr_controller_t, gr_controller_l], mv_controller]

        self.var1 = IntVar(self, 1)
        self.var2 = IntVar(self, 4)

        self.add_widgets()
        self.start()

    def start(self):
        self.controllers[0][0].draw_borders(self.entry2.get(), self.entry1.get())
        self.controllers[0][1].draw_borders(self.entry4.get(), self.entry3.get())
        self.protocol("WM_DELETE_WINDOW", self.hide_window)

    def tick(self):
        """ Gets called from DashboardView.tick() every x seconds. """
        [controller.update_graph() for controller in self.controllers[0]]
        self.controllers[1].refresh()

    def hide_window(self):
        self.wm_withdraw()

    def close(self):
        self.destroy()

    def show_window(self):
        self.make_topmost()
        self.deiconify()

    def update_status_label(self, status):
        self.la_status.config(text='{}'.format(status))
        self.la_status.config(fg=st.btn_bg_red) if 'Closed' in status else self.la_status.config(fg=st.btn_bg_blue)

    def change_btn_state(self, manual):
        if manual == 1:
            self.var2.set(3)

            self.la_man_roll_out.config(state=NORMAL)
            self.en_man_roll_out.config(state=NORMAL)

            self.btn_roll_out.config(state=NORMAL)
            self.btn_roll_in.config(state=NORMAL)

            self.btn_man_set.config(state=NORMAL, bg=st.btn_bg_blue)
            self.btn_set.config(state=DISABLED, bg=st.btn_bg_grey)

            self.label1.config(state=DISABLED)
            self.label2.config(state=DISABLED)
            self.label3.config(state=DISABLED)
            self.label4.config(state=DISABLED)

            self.entry1.config(state=DISABLED)
            self.entry2.config(state=DISABLED)
            self.entry3.config(state=DISABLED)
            self.entry4.config(state=DISABLED)

        if manual == 0:
            self.la_man_roll_out.config(state=DISABLED)
            self.en_man_roll_out.config(state=DISABLED)

            self.btn_roll_out.config(state=DISABLED)
            self.btn_roll_in.config(state=DISABLED)

            self.btn_man_set.config(state=DISABLED, bg=st.btn_bg_grey)
            self.btn_set.config(state=NORMAL, bg=st.btn_bg_blue)

            self.label1.config(state=NORMAL)
            self.label2.config(state=NORMAL)
            self.label3.config(state=NORMAL)
            self.label4.config(state=NORMAL)

            self.entry1.config(state=NORMAL)
            self.entry2.config(state=NORMAL)
            self.entry3.config(state=NORMAL)
            self.entry4.config(state=NORMAL)

    def add_widgets(self):
        """ Creates and adds widgets to the frame, such as buttons, labels, and input fields. """
        button_width = 15

        Button(self, width=92, disabledforeground=st.fg_white, bg=st.panel_bg, state=DISABLED, borderwidth=0,
               height=2).place(relx=0.11, rely=0.7, anchor=W)
        Button(self, text="Status", width=button_width, disabledforeground=st.fg_white, bg=st.panel_title_bg,
               state=DISABLED, borderwidth=0, height=2).place(relx=0.03, rely=0.7, anchor=W)

        Button(self, text="Manual mode", width=button_width, disabledforeground=st.fg_white, bg=st.panel_title_bg,
               state=DISABLED, borderwidth=0, height=2).place(relx=0.831, rely=0.7, anchor=E)

        Button(self, width=63, disabledforeground=st.fg_white, bg=st.panel_bg, fg=st.fg_white, state=DISABLED,
               borderwidth=0, height=12).place(relx=0.11, rely=0.86, anchor=W)
        Button(self, text="Settings\nauto", width=button_width, disabledforeground=st.fg_white, bg=st.panel_title_bg,
               state=DISABLED, borderwidth=0, height=12).place(relx=0.03, rely=0.86, anchor=W)

        Button(self, width=50, disabledforeground=st.fg_white, bg=st.panel_bg, fg=st.fg_white, state=DISABLED,
               borderwidth=0, height=12).place(relx=0.97, rely=0.86, anchor=E)
        Button(self, text="Settings\nmanual", width=button_width, disabledforeground=st.fg_white, bg=st.panel_title_bg,
               state=DISABLED, borderwidth=0, height=12).place(relx=0.65, rely=0.86, anchor=E)

        Radiobutton(self, command=lambda: self.controllers[1].btn_click(self.var1), text="Light intensity",
                    indicatoron=False, variable=self.var1, borderwidth=0, height=2, selectcolor=st.btn_bg_blue,
                    value=1, width=20, bg=st.btn_bg_grey, fg=st.fg_white).place(relx=0.435, rely=0.05, anchor=CENTER)

        Radiobutton(self, command=lambda: self.controllers[1].btn_click(self.var1), text="Temperature",
                    indicatoron=False, variable=self.var1, borderwidth=0, height=2, selectcolor=st.btn_bg_blue,
                    value=2, width=20, bg=st.btn_bg_grey, fg=st.fg_white).place(relx=0.565, rely=0.05, anchor=CENTER)

        Radiobutton(self, command=lambda: self.controllers[1].btn_click(self.var2), borderwidth=0,
                    text="ON", indicatoron=False, variable=self.var2, selectcolor=st.btn_bg_blue, fg=st.fg_white,
                    bg=st.btn_bg_grey, height=2, value=3, width=10).place(relx=0.901, rely=0.7, anchor=E)

        Radiobutton(self, command=lambda: self.controllers[1].btn_click(self.var2), borderwidth=0,
                    text="OFF", indicatoron=False, variable=self.var2, selectcolor=st.btn_bg_blue, fg=st.fg_white,
                    bg=st.btn_bg_grey, height=2, value=4, width=10).place(relx=0.97, rely=0.7, anchor=E)

        y_pos = .785  # start position

        entries = []
        labels_text = ['Roll out on temperature', 'Roll in on temperature', 'Roll out on light intensity',
                       'Roll in on light intensity']
        default_values = [ba.temp_rollo, ba.temp_rolli, ba.light_rollo, ba.temp_rolli]

        for x in range(1, len(labels_text) + 1):
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

        self.la_man_roll_out = Label(self, text='Uitrol afstand', disabledforeground=st.btn_bg_grey, bg=st.panel_bg,
                                     fg=st.fg_white, state=DISABLED)
        self.la_man_roll_out.place(relx=0.75, rely=y_pos, anchor=E)

        self.en_man_roll_out = Entry(self, width=33, borderwidth=0)
        self.en_man_roll_out.insert(0, ba.roll_out_dist)
        self.en_man_roll_out.config(disabledbackground=st.btn_bg_grey, state=DISABLED)
        self.en_man_roll_out.place(relx=0.94, rely=y_pos, anchor=E)

        self.btn_roll_out = Button(self, text='Roll out', bg=st.btn_bg_grey, fg=st.fg_white, width=button_width,
                                   command=lambda: self.controllers[1].btn_click(5), height=2, borderwidth=0,
                                   state=DISABLED)
        self.btn_roll_out.place(relx=0.83, rely=y_pos + .14, anchor=E)

        self.btn_roll_in = Button(self, text='Roll in', bg=st.btn_bg_grey, fg=st.fg_white, width=button_width,
                                  command=lambda: self.controllers[1].btn_click(6), height=2, borderwidth=0,
                                  state=DISABLED)
        self.btn_roll_in.place(relx=.94, rely=y_pos + .14, anchor=E)

        self.btn_set = Button(self, text='Set', width=button_width, bg=st.btn_bg_blue, fg=st.fg_white,
                              borderwidth=0, command=lambda: self.controllers[1].btn_click(7))
        self.btn_set.place(relx=0.383, rely=y_pos + .15, anchor=W)

        self.btn_man_set = Button(self, text='Set', width=button_width, bg=st.btn_bg_grey, fg=st.fg_white,
                                  state=DISABLED, borderwidth=0, command=lambda: self.controllers[1].btn_click(8))
        self.btn_man_set.place(relx=0.94, rely=y_pos + .04, anchor=E)

        self.la_status = Label(self, fg=st.btn_bg_blue, bg=st.panel_bg)
        self.la_status.place(relx=0.15, rely=0.7, anchor=W)

        Button(self, text="Go back", width=button_width, command=self.hide_window, bg=st.btn_bg_grey, fg=st.fg_white,
               borderwidth=0, height=2).place(relx=0, rely=0.05, anchor=W)

    def create_base_canvas(self):
        """ Creates and adds a canvas. This canvas is used to display a graph, hence two canvases are made in the
        constructor """
        canvas = Canvas(self, height=480, width=1100, bg=st.canv_bg, highlightthickness=0)
        canvas.create_line(50, 450, 1050, 450, width=2, fill=st.canv_line)  # x-axis
        canvas.create_line(50, 450, 50, 50, width=2, fill=st.canv_line)  # y-axis
        canvas.place(relx=0.5, rely=0.37, anchor=CENTER)
        return canvas

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

    def make_topmost(self):
        """Makes this window the topmost window"""
        self.lift()
        self.attributes("-topmost", 1)
        self.attributes("-topmost", 0)
