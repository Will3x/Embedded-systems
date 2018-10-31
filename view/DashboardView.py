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

    def start(self):
        imageref = self.make_background()  # don't delete reference
        self.make_panels()
        self.tick()
        self.mainloop()

    def tick(self):
        self.controller.get_values()
        self.refresh()
        self.after(2000, self.tick)

    def set_controller_instance(self, controller):
        self.controller = controller

    def close_all(self):
        for key, value in self.mainview.items():
            try:
                self.mainview.get(key).destroy()
                print('Destroyed instance')
            except:
                pass
        self.destroy()

    def hide_window(self):
        self.wm_withdraw()

    def create_instance(self, index):
        """ Creates class instances and saves these in a dictionary """
        if self.mainview[index] == '':
            name = 'Device {}'.format(index)
            self.mainview[index] = MainView.MainView(self, name)
        else:
            self.mainview.get(index).show_window()

    def open_btn(self, value):
        self.create_instance(value)

    def refresh(self):
        """ Called from tick. Will check every 2 seconds if an Arduino connection has been made. """
        devices = self.controller.check_if_connected()

        for key, device in devices.items():
            if not device == '':
                self.change_btn_state('normal', key)
            else:
                self.change_btn_state('disabled', key)

        for x in devices:
            devices[x] = ''

    def change_btn_state(self, state, num):
        color_blue = "dodger blue"
        color_red = '#D60000'
        color_grey = '#444D5F'

        if state == 'normal':
            exec(f'self.button{num}.config(state=NORMAL, bg=color_blue, text="Settings / Expand")')
            exec(f'self.btnopen{num}.config(state=NORMAL, bg=color_blue)')

        elif state == 'disabled':
            exec(f'self.button{num}.config(state=DISABLED, bg=color_red, text="Not connected", fg="white")')
            exec(f'self.btnopen{num}.config(state=DISABLED, bg=color_grey)')

    def change_label(self, value):
        for x in range(1, 6):
            self.labeltemp1.config(text='{} °C'.format(value-1))
            self.labeltemp2.config(text='{} °C'.format(value))
            self.labeltemp3.config(text='{} °C'.format(value-2))
            self.labeltemp4.config(text='{} °C'.format(value+1))
            self.labeltemp5.config(text='{} °C'.format(value+2))

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
            entries.insert(1, f'self.labelframe{x}.place(relx={x_position:.2f}, rely={y_position}, anchor=CENTER)')
            entries.insert(2, f'self.button{x} = Button(self, text="Not connected", width=20, height=2,'
                              f'bg="#D60000", fg="white", disabledforeground="white", borderwidth=0, state=DISABLED, '
                              f'command=partial(self.open_btn,{x}))')
            entries.insert(3, f'self.button{x}.place(relx={x_position+.06:.2f}, rely={y_position+.12}, anchor=CENTER)')
            entries.insert(2, f'self.btnopen{x} = Button(self, text="Open", width=10, height=2,'
                              f'bg=color_grey, fg="white", disabledforeground="white", borderwidth=0, state=DISABLED)')
            entries.insert(3, f'self.btnopen{x}.place(relx={x_position-.03:.2f}, rely={y_position+.12}, anchor=CENTER)')
            entries.insert(2, f'self.btnclose{x} = Button(self, text="Close", width=10, height=2,'
                              f'bg=color_grey, fg="white", disabledforeground="white", borderwidth=0, state=DISABLED)')
            entries.insert(3, f'self.btnclose{x}.place(relx={x_position-.09:.2f}, rely={y_position+.12}, anchor=CENTER)')
            entries.insert(4, f'self.label{x} = Label(self, text="Temperature: ", background="#2B323F", fg="white")')
            entries.insert(5, f'self.label{x}.place(relx={x_position-.07:.2f}, rely={y_position-.08}, anchor=CENTER)')
            entries.insert(6, f'self.labeltemp{x} = Label(self, text="{x*3} °C", background="#2B323F", fg="dodger blue")')
            entries.insert(7, f'self.labeltemp{x}.place(relx={x_position-.03:.2f}, rely={y_position-.08}, anchor=CENTER)')
            entries.insert(8, f'self.label{x} = Label(self, text="Light intesity: ", background="#2B323F", fg="white")')
            entries.insert(9, f'self.label{x}.place(relx={x_position-.07:.2f}, rely={y_position-.03}, anchor=CENTER)')
            entries.insert(10, f'self.label{x} = Label(self, text="Status: ", background="#2B323F", fg="white")')
            entries.insert(11, f'self.label{x}.place(relx={x_position-.07:.2f}, rely={y_position+.04}, anchor=CENTER)')
            entries.insert(12, f'self.label{x} = Label(self, text="Device {x}", background="#2B323F", fg="white")')
            entries.insert(13, f'self.label{x}.place(relx={x_position:.2f}, rely={y_position-.14}, anchor=CENTER)')

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
