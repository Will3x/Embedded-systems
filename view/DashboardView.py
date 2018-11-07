from tkinter import *
from functools import partial  # This is being used. Don't delete.
from view import MainView
from controller import SerialController
import Style as st


class DashboardView(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title('Dashboard')
        self.resizable(False, False)
        self.center_window()
        self.protocol("WM_DELETE_WINDOW", self.close_all)
        self.mainview = {1: '', 2: '', 3: '', 4: '', 5: ''}
        self.prev_devices = {1: '', 2: '', 3: '', 4: '', 5: ''}
        SerialController.SerialController.setup()

    def start(self):
        imageref = self.make_background()  # don't delete reference
        self.make_panels()
        self.tick()
        self.mainloop()

    def tick(self):
        self.controller.read_from_serial()
        self.refresh()
        [x.tick() for x in self.mainview.values() if x != '']
        self.after(1500, self.tick)

    def set_controller_instance(self, controller):
        self.controller = controller

    def close_all(self):
        try:
            [exec('x.close()') for x in self.mainview.values() if x != '']
        except (TclError, AttributeError) as e:
            print(e)
        self.destroy()

    def hide_window(self):
        self.wm_withdraw()

    def create_instance(self, index):
        """ Creates class instances and saves these in a dictionary """
        if self.mainview[index] == '':
            name = 'Device {}'.format(index)
            self.mainview[index] = MainView.MainView(self, name)
        else:
            try:
                self.mainview.get(index).show_window()
            except TclError:
                name = 'Device {}'.format(index)
                self.mainview[index] = MainView.MainView(self, name)

    def open_btn(self, value):
        self.create_instance(value)

    def refresh(self):
        """ Called from tick. Will check every x seconds if an Arduino connection has been made. """
        devices = self.controller.check_if_connected()

        [self.change_btn_state('normal', key) if device != '' else self.change_btn_state('disabled', key)
         for key, device in devices.items()]

        self.update_instances(devices, self.prev_devices)

        self.prev_devices = devices.copy()
        devices.update(devices.fromkeys(devices, ''))

    def update_instances(self, devices, prev_devices):
        for x in devices.keys():
            if devices[x] == '' and prev_devices[x] != '' and self.mainview[x] != '':
                self.mainview[x].close()
                self.mainview[x] = ''

    def change_btn_state(self, state, num):
        try:
            if state == 'normal':
                exec(f"self.button{num}.config(state=NORMAL, bg=st.btn_bg_blue, text='View')")
                exec(f'self.btnopen{num}.config(state=NORMAL)')
                exec(f'self.btnclose{num}.config(state=NORMAL)')

            if state == 'disabled':
                exec(f'self.button{num}.config(state=DISABLED, bg=st.btn_bg_red, text="Not connected", fg=st.fg_white)')
                exec(f'self.btnopen{num}.config(state=DISABLED, bg=st.btn_bg_grey)')
                exec(f'self.btnclose{num}.config(state=DISABLED)')
        except AttributeError:
            print('buttons not found')
            pass

    def change_label(self, devices, value):
        """ Change temperature and light sensor values on Dashboard """
        for x in value:
            if devices[x] != '' and value[x] == ():
                exec(f'self.temp{x}.config(text="FETCHING DATA...", fg=st.btn_bg_blue)')
                exec(f'self.light{x}.config(text="FETCHING DATA...", fg=st.btn_bg_blue)')
                exec(f'self.status{x}.config(text="FETCHING DATA...", fg=st.btn_bg_blue)')
            elif devices[x] != '' and value[x] != ():
                temp = value[x]['t']
                light = value[x]['l']
                status = self.controller.status_open_closed(x, value)

                exec(f'self.temp{x}.config(text="{temp}°C", fg=st.btn_bg_blue)')
                exec(f'self.light{x}.config(text="{light} / 100", fg=st.btn_bg_blue)')
                exec(f'self.status{x}.config(text="{status}")')
                exec(f'self.status{x}.config(fg=st.btn_bg_red)') if status == 'Closed' \
                    else exec(f'self.status{x}.config(fg=st.btn_bg_blue)')

            else:
                exec(f'self.temp{x}.config(text="NO DATA", fg=st.btn_bg_grey)')
                exec(f'self.light{x}.config(text="NO DATA", fg=st.btn_bg_grey)')
                exec(f'self.status{x}.config(text="NO DATA", fg=st.btn_bg_grey)')

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
                              f'command=partial(self.open_btn,{x}))')
            entries.insert(3, f'self.button{x}.place(relx={x_position+.06}, rely={y_position+.12}, anchor=CENTER)')
            entries.insert(4, f'self.btnopen{x} = Button(self, text="Roll out", width=10, height=2, bg=st.btn_bg_grey, '
                              f'fg=st.fg_white, disabledforeground="#6B7789", borderwidth=0, state=DISABLED)')
            entries.insert(5, f'self.btnopen{x}.place(relx={x_position-.03}, rely={y_position+.12}, anchor=CENTER)')
            entries.insert(6, f'self.btnclose{x} = Button(self, text="Roll in", width=10, height=2, bg=st.btn_bg_grey, '
                              f'fg=st.fg_white, disabledforeground="#6B7789", borderwidth=0, state=DISABLED)')
            entries.insert(7, f'self.btnclose{x}.place(relx={x_position-.09}, rely={y_position+.12}, anchor=CENTER)')
            entries.insert(8, f'self.labelt{x} = Label(self, text="Temperature: ", background=st.panel_bg, '
                              f'fg=st.fg_white)')
            entries.insert(9, f'self.labelt{x}.place(relx={x_position-.04}, rely={y_position-.08}, anchor=E)')
            entries.insert(10, f'self.temp{x} = Label(self, background=st.panel_bg, text="NO DATA", fg=st.btn_bg_grey)')
            entries.insert(11, f'self.temp{x}.place(relx={x_position-.04}, rely={y_position-.079}, anchor=W)')
            entries.insert(12, f'self.labell{x} = Label(self, text="Light intesity: ", background=st.panel_bg, '
                               f'fg=st.fg_white)')
            entries.insert(13, f'self.labell{x}.place(relx={x_position-.04}, rely={y_position-.029}, anchor=E)')
            entries.insert(14, f'self.light{x} = Label(self, background=st.panel_bg, text="NO DATA", '
                               f'fg=st.btn_bg_grey)')
            entries.insert(15, f'self.light{x}.place(relx={x_position-.04}, rely={y_position-.0277}, anchor=W)')
            entries.insert(16, f'self.labels{x} = Label(self, text="Status: ", background=st.panel_bg, fg=st.fg_white)')
            entries.insert(17, f'self.labels{x}.place(relx={x_position-.04:.2f}, rely={y_position+.04}, anchor=E)')
            entries.insert(18, f'self.status{x} = Label(self, background=st.panel_bg, text="NO DATA", '
                               f'fg=st.btn_bg_grey)')
            entries.insert(19, f'self.status{x}.place(relx={x_position-.04:.2f}, rely={y_position+.0415}, anchor=W)')
            entries.insert(20, f'self.titel{x} = Label(self, text="Device {x}", background=st.panel_bg, '
                               f'fg=st.fg_white)')
            entries.insert(21, f'self.titel{x}.place(relx={x_position:.2f}, rely={y_position-.14}, anchor=CENTER)')

            x_position += .3

            for items in entries:
                exec(items)

        self.close_all_btn = Button(self, text="Roll all in", width=30, height=2, bg=st.btn_bg_grey, fg=st.fg_white,
                                    borderwidth=0, state=NORMAL)
        self.close_all_btn.place(relx=0.42, rely=0.14, anchor=CENTER)

        self.open_all_btn = Button(self, text="Roll all out", width=30, height=2, bg=st.btn_bg_grey, fg=st.fg_white,
                                   borderwidth=0, state=NORMAL)
        self.open_all_btn.place(relx=0.58, rely=0.14, anchor=CENTER)

        self.labelframe6 = LabelFrame(self, background=st.panel_bg, highlightbackground=st.highlight_bg,
                                      highlightcolor=st.highlight_bg, highlightthickness=1, borderwidth=0, height=300,
                                      width=400)
        self.labelframe6.place(relx=x_position, rely=y_position, anchor=CENTER)

        self.label6 = Label(self, text="Created by IT Works", background=st.panel_bg, fg=st.fg_white)
        self.label6.place(relx=x_position, rely=y_position, anchor=CENTER)

    def make_background(self):
        filename = PhotoImage(file="images/bg.png")
        background_label = Label(self, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        return filename

    def center_window(self):
        window_width = self.winfo_screenwidth() - 500
        window_height = self.winfo_screenheight() - 230

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = screen_width / 2 - window_width / 2
        y = (screen_height / 2 - window_height / 2) - 40
        self.geometry("%dx%d+%d+%d" % (window_width, window_height, x, y))
