from tkinter import *
from functools import partial  # This is being used. Don't delete.
from view import MainView


class DashboardView(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title('Dashboard')
        self.resizable(False, False)
        self.center_window()
        self.protocol("WM_DELETE_WINDOW", self.close_all)
        self.mainview = {1: '', 2: '', 3: '', 4: '', 5: ''}
        self.prev_devices = {1: '', 2: '', 3: '', 4: '', 5: ''}

    def start(self):
        imageref = self.make_background()  # don't delete reference
        self.make_panels()
        self.tick()
        self.mainloop()

    def tick(self):
        self.refresh()
        self.controller.get_values()
        [x.tick() for x in self.mainview.values() if x != '']
        self.after(3000, self.tick)

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

        for x in devices.keys():
            if devices[x] == '' and self.prev_devices[x] != '' and self.mainview[x] != '':
                self.mainview[x].close()
                self.mainview[x] = ''

        for key, device in devices.items():
            if not device == '':
                self.change_btn_state('normal', key)
            else:
                self.change_btn_state('disabled', key)

        self.prev_devices = devices.copy()
        devices.update(devices.fromkeys(devices, ''))

    def change_btn_state(self, state, num):
        color_blue = "dodger blue"
        color_red = '#D60000'
        color_grey = '#444D5F'

        if state == 'normal':
            exec(f'self.button{num}.config(state=NORMAL, bg=color_blue, text="View")')
            exec(f'self.btnopen{num}.config(state=NORMAL)')
            exec(f'self.btnclose{num}.config(state=NORMAL)')

        if state == 'disabled':
            exec(f'self.button{num}.config(state=DISABLED, bg=color_red, text="Not connected", fg="white")')
            exec(f'self.btnopen{num}.config(state=DISABLED, bg=color_grey)')
            exec(f'self.btnclose{num}.config(state=DISABLED)')

    def change_label(self, value):
        """ Change temperature and light sensor values on Dashboard """
        try:
            for x in value:
                if value[x] != ():
                    temp = value[x]['temp']
                    light = value[x]['ldr']

                    exec(f'self.temp{x}.config(text="{temp}°C", fg="dodger blue")')
                    exec(f'self.light{x}.config(text="{light} / 100", fg="dodger blue")')
        except TypeError:
            self.temp1.config(text='NO DATA', fg='#444D5F')
            self.light1.config(text='NO DATA', fg='#444D5F')

    def make_panels(self):
        x_position = .2  # start position x
        y_position = .37  # start position y

        color_grey = '#444D5F'

        entries = []
        count = 0

        for x in range(1, 6):
            count += 1
            if count == 4:
                x_position = .2
                y_position = .77

            entries.insert(0, f'self.labelframe{x} = LabelFrame(self, background="#2B323F", '
                              f'highlightbackground="#1F242D" ,highlightcolor="#1F242D", highlightthickness=1, '
                              f'borderwidth=0, height=300, width=400)')
            entries.insert(1, f'self.labelframe{x}.place(relx={x_position}, rely={y_position}, anchor=CENTER)')
            entries.insert(2, f'self.button{x} = Button(self, text="Not connected", width=20, height=2,'
                              f'bg="#D60000", fg="white", disabledforeground="white", borderwidth=0, state=DISABLED, '
                              f'command=partial(self.open_btn,{x}))')
            entries.insert(3, f'self.button{x}.place(relx={x_position+.06}, rely={y_position+.12}, anchor=CENTER)')
            entries.insert(2, f'self.btnopen{x} = Button(self, text="Open", width=10, height=2,'
                              f'bg=color_grey, fg="white", disabledforeground="#6B7789", borderwidth=0, state=DISABLED)')
            entries.insert(3, f'self.btnopen{x}.place(relx={x_position-.03}, rely={y_position+.12}, anchor=CENTER)')
            entries.insert(2, f'self.btnclose{x} = Button(self, text="Close", width=10, height=2,'
                              f'bg=color_grey, fg="white", disabledforeground="#6B7789", borderwidth=0, state=DISABLED)')
            entries.insert(3, f'self.btnclose{x}.place(relx={x_position-.09}, rely={y_position+.12}, anchor=CENTER)')
            entries.insert(4, f'self.labelt{x} = Label(self, text="Temperature: ", background="#2B323F", fg="white")')
            entries.insert(5, f'self.labelt{x}.place(relx={x_position-.07}, rely={y_position-.08}, anchor=CENTER)')
            entries.insert(6, f'self.temp{x} = Label(self, background="#2B323F", text="NO DATA", fg="#444D5F")')
            entries.insert(7, f'self.temp{x}.place(relx={x_position-.04}, rely={y_position-.079}, anchor=W)')
            entries.insert(8, f'self.labell{x} = Label(self, text="Light intesity: ", background="#2B323F",fg="white")')
            entries.insert(9, f'self.labell{x}.place(relx={x_position-.07}, rely={y_position-.029}, anchor=CENTER)')
            entries.insert(10, f'self.light{x} = Label(self, background="#2B323F", text="NO DATA", fg="#444D5F")')
            entries.insert(11, f'self.light{x}.place(relx={x_position-.04}, rely={y_position-.0277}, anchor=W)')
            entries.insert(12, f'self.label{x} = Label(self, text="Status: ", background="#2B323F", fg="white")')
            entries.insert(13, f'self.label{x}.place(relx={x_position-.07:.2f}, rely={y_position+.04}, anchor=CENTER)')
            entries.insert(14, f'self.label{x} = Label(self, text="Device {x}", background="#2B323F", fg="white")')
            entries.insert(15, f'self.label{x}.place(relx={x_position:.2f}, rely={y_position-.14}, anchor=CENTER)')

            x_position += .3

            for items in entries:
                exec(items)

        self.close_all_btn = Button(self, text="Close all", width=30, height=2, bg="#444D5F",
                                    fg="white", borderwidth=0, state=NORMAL)
        self.close_all_btn.place(relx=0.42, rely=0.14, anchor=CENTER)
        self.open_all_btn = Button(self, text="Open all", width=30, height=2, bg="dodger blue",
                                   fg="white", borderwidth=0, state=NORMAL)
        self.open_all_btn.place(relx=0.58, rely=0.14, anchor=CENTER)

        self.labelframe6 = LabelFrame(self, background="#2B323F", highlightbackground="#1F242D",
                                      highlightcolor="#1F242D", highlightthickness=1, borderwidth=0,
                                      height=300, width=400)
        self.labelframe6.place(relx=x_position, rely=y_position, anchor=CENTER)
        self.label6 = Label(self, text="v1.0\n\nCreated by IT Works", background="#2B323F", fg="white")
        self.label6.place(relx=x_position, rely=y_position, anchor=CENTER)

    def make_background(self):
        filename = PhotoImage(file="images/bg.png")
        background_label = Label(self, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        return filename

    def center_window(self):
        window_width = self.winfo_screenwidth()-500
        window_height = self.winfo_screenheight()-230

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = screen_width / 2 - window_width / 2
        y = (screen_height / 2 - window_height / 2) - 40
        self.geometry("%dx%d+%d+%d" % (window_width, window_height, x, y))
