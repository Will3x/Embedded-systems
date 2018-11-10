from controller import SerialController as ser
import Style as st
from tkinter import *
from functools import partial


class DashboardView(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title('Dashboard')
        self.resizable(False, False)
        self.center_window()
        self.make_background()

        self.controller = None

    def setup(self, speed):
        """ Called once from Main. Must be set up in this order. """
        self.protocol("WM_DELETE_WINDOW", self.controller.close_all)
        self.make_panels()
        self.tick(speed)
        self.make_topmost()

    def start(self):
        self.mainloop()

    def tick(self, speed):
        ser.SerialController.read()
        self.controller.refresh()
        self.after(speed, lambda: self.tick(speed))

    def close(self):
        self.destroy()

    def hide_window(self):
        self.wm_withdraw()

    def update_btn_state(self, devices):
        for index, device in devices.items():
            if device is not None:
                self.controller.create_mv_instance(index)
                exec(f'self.button{index}.config(state=NORMAL, bg=st.btn_bg_blue, text="View")')
                exec(f'self.btnopen{index}.config(state=NORMAL)')
                exec(f'self.btnclose{index}.config(state=NORMAL)')
            else:
                exec(f'self.button{index}.config(state=DISABLED, bg=st.btn_bg_red, text="Not connected", '
                     f'fg=st.fg_white)')
                exec(f'self.btnopen{index}.config(state=DISABLED, bg=st.btn_bg_grey)')
                exec(f'self.btnclose{index}.config(state=DISABLED)')

    def update_label(self, devices, values):
        """ Change temperature and light sensor values on Dashboard """
        for index in values:
            if devices[index] is not None and values[index] is None:
                exec(f'self.temp{index}.config(text="FETCHING DATA...", fg=st.btn_bg_blue)')
                exec(f'self.light{index}.config(text="FETCHING DATA...", fg=st.btn_bg_blue)')
                exec(f'self.status{index}.config(text="FETCHING DATA...", fg=st.btn_bg_blue)')
            elif devices[index] is not None and values[index] is not None:
                temp = values[index]['t']
                light = values[index]['l']
                status = self.controller.get_status(index, values)

                exec(f'self.temp{index}.config(text="{temp}°C", fg=st.btn_bg_blue)')
                exec(f'self.light{index}.config(text="{light} / 100", fg=st.btn_bg_blue)')
                exec(f'self.status{index}.config(text="{status}", fg=st.btn_bg_blue)')
                if status == 'Closed':
                    exec(f'self.status{index}.config(fg=st.btn_bg_red)')

            else:
                exec(f'self.temp{index}.config(text="NO DATA", fg=st.btn_bg_grey)')
                exec(f'self.light{index}.config(text="NO DATA", fg=st.btn_bg_grey)')
                exec(f'self.status{index}.config(text="NO DATA", fg=st.btn_bg_grey)')

    def make_panels(self):
        x_position = .2  # start position x
        y_position = .37  # start position y

        entries = []

        for x in range(1, 6):
            if x == 4:
                x_position = .2
                y_position = .77

            entries.insert(0, f'self.labelframe{x} = LabelFrame(self, background=st.panel_bg, highlightbackground='
                              f'st.highlight_bg, highlightcolor=st.highlight_bg, highlightthickness=1, borderwidth=0, '
                              f'height=300, width=400)')
            entries.insert(1, f'self.labelframe{x}.place(relx={x_position}, rely={y_position}, anchor=CENTER)')
            entries.insert(2, f'self.button{x} = Button(self, text="Not connected", width=20, height=2, bg="#D60000", '
                              f'fg=st.fg_white, disabledforeground="white", borderwidth=0, state=DISABLED, '
                              f'command=partial(partial(self.controller.btn_click, 4, {x})))')
            entries.insert(3, f'self.button{x}.place(relx={x_position+.06}, rely={y_position+.12}, anchor=CENTER)')
            entries.insert(4, f'self.btnopen{x} = Button(self, text="Roll out", width=10, height=2, bg=st.btn_bg_grey, '
                              f'fg=st.fg_white, disabledforeground="#6B7789",  borderwidth=0, state=DISABLED, '
                              f'command=partial(self.controller.btn_click, 5, {x}))')
            entries.insert(5, f'self.btnopen{x}.place(relx={x_position-.03}, rely={y_position+.12}, anchor=CENTER)')
            entries.insert(6, f'self.btnclose{x} = Button(self, text="Roll in", width=10, height=2, bg=st.btn_bg_grey, '
                              f'fg=st.fg_white, disabledforeground="#6B7789", borderwidth=0, state=DISABLED, '
                              f'command=partial(self.controller.btn_click, 6, {x}))')
            entries.insert(7, f'self.btnclose{x}.place(relx={x_position-.09}, rely={y_position+.12}, anchor=CENTER)')
            entries.insert(8, f'self.labelt{x} = Label(self, text="Temperature: ", background=st.panel_bg, '
                              f'fg=st.fg_white)')
            entries.insert(9, f'self.labelt{x}.place(relx={x_position-.02}, rely={y_position-.08}, anchor=E)')
            entries.insert(10, f'self.temp{x} = Label(self, background=st.panel_bg, text="NO DATA", fg=st.btn_bg_grey)')
            entries.insert(11, f'self.temp{x}.place(relx={x_position-.02}, rely={y_position-.079}, anchor=W)')
            entries.insert(12, f'self.labell{x} = Label(self, text="Light intensity: ", background=st.panel_bg, '
                               f'fg=st.fg_white)')
            entries.insert(13, f'self.labell{x}.place(relx={x_position-.02}, rely={y_position-.029}, anchor=E)')
            entries.insert(14, f'self.light{x} = Label(self, background=st.panel_bg, text="NO DATA", '
                               f'fg=st.btn_bg_grey)')
            entries.insert(15, f'self.light{x}.place(relx={x_position-.02}, rely={y_position-.0277}, anchor=W)')
            entries.insert(16, f'self.labels{x} = Label(self, text="Status: ", background=st.panel_bg, fg=st.fg_white)')
            entries.insert(17, f'self.labels{x}.place(relx={x_position-.02:.2f}, rely={y_position+.04}, anchor=E)')
            entries.insert(18, f'self.status{x} = Label(self, background=st.panel_bg, text="NO DATA", '
                               f'fg=st.btn_bg_grey)')
            entries.insert(19, f'self.status{x}.place(relx={x_position-.02:.2f}, rely={y_position+.0415}, anchor=W)')
            entries.insert(20, f'self.titel{x} = Label(self, text="Device {x}", background=st.panel_bg, '
                               f'fg=st.fg_white)')
            entries.insert(21, f'self.titel{x}.place(relx={x_position:.2f}, rely={y_position-.14}, anchor=CENTER)')

            x_position += .3

            for items in entries:
                exec(items)

        close_all_btn = Button(self, text="Roll all in", width=30, height=2, bg=st.btn_bg_grey, fg=st.fg_white,
                                    borderwidth=0, command=partial(self.controller.btn_click, 7), state=NORMAL)
        close_all_btn.place(relx=0.42, rely=0.14, anchor=CENTER)

        open_all_btn = Button(self, text="Roll all out", width=30, height=2, bg=st.btn_bg_grey, fg=st.fg_white,
                                   borderwidth=0, command=partial(self.controller.btn_click, 8), state=NORMAL)
        open_all_btn.place(relx=0.58, rely=0.14, anchor=CENTER)

        labelframe6 = LabelFrame(self, background=st.panel_bg, highlightbackground=st.highlight_bg,
                                      highlightcolor=st.highlight_bg, highlightthickness=1, borderwidth=0, height=300,
                                      width=400)
        labelframe6.place(relx=x_position, rely=y_position, anchor=CENTER)

        label6 = Label(self, text="Created by IT Works", background=st.panel_bg, fg=st.fg_white)
        label6.place(relx=x_position, rely=y_position, anchor=CENTER)

    def make_background(self):
        background = PhotoImage(file="images/bg.png")
        background_label = Label(self, image=background)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background  # Don't delete reference.

    def center_window(self):
        window_width = self.winfo_screenwidth() - 500
        window_height = self.winfo_screenheight() - 230

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = screen_width / 2 - window_width / 2
        y = (screen_height / 2 - window_height / 2) - 40
        self.geometry("%dx%d+%d+%d" % (window_width, window_height, x, y))

    def set_controller_instance(self, controller):
        self.controller = controller

    def make_topmost(self):
        """Makes this window the topmost window"""
        self.lift()
        self.attributes("-topmost", 1)
        self.attributes("-topmost", 0)
