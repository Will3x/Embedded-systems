from tkinter import *
from functools import partial
from controller import DashboardController
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
        self.mainloop()

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

    def show_window(self):
        self.deiconify()

    def create_instance(self, index):
        if self.mainview[index] == '':
            self.mainview[index] = MainView.MainView(self)
        else:
            self.mainview.get(index).show_window()

    def open_btn(self, value):
        self.controller.btn_event(value)

    def refresh_btn(self, num):
        # if self.controller.check_if_connected():
        self.change_btn_state('normal', num)

    def change_btn_state(self, state, num):
        color_blue = "dodger blue"
        color_red = '#D60000'

        if state == 'normal':
            exec(f'self.button{num}.config(state=NORMAL, bg=color_blue, text="Open")')

        elif state == 'disabled':
            exec(f'self.button{num}.config(state=DISABLED, bg=color_red, text="Not connected")')
            # btn.config(state=DISABLED, bg=color_red, text='Not connected')


    def make_panels(self):
        x_position = .2  # start position x
        y_position = .27  # start position y

        color_grey_ = '#444D5F'

        entries = []
        count = 0

        for x in range(1, 6):
            count += 1
            if count == 4:
                x_position = .2
                y_position = .72

            entries.insert(0, f'self.labelframe{x} = LabelFrame(self, background="#2B323F", '
                              f'highlightbackground="#1F242D" ,highlightcolor="#1F242D", highlightthickness=1, '
                              f'borderwidth=0, height=350, width=400)')
            entries.insert(1, f'self.labelframe{x}.place(relx={x_position:.2f}, rely={y_position}, anchor=CENTER)')
            entries.insert(2, f'self.button{x} = Button(self, text="Not connected", width=30, height=2,'
                              f'bg="#D60000", fg="white", borderwidth=0, state=DISABLED, '
                              f'command=partial(self.open_btn,{x}))')
            entries.insert(3, f'self.button{x}.place(relx={x_position+.03:.2f}, rely={y_position+.15}, anchor=CENTER)')
            entries.insert(4, f'self.refresh{x} = Button(self, text="Refresh", width=10, height=2,'
                              f'bg="#444D5F", fg="white", borderwidth=0, state=NORMAL, '
                              f'command=partial(self.refresh_btn, {x}))')
            entries.insert(5, f'self.refresh{x}.place(relx={x_position-.08:.2f}, rely={y_position+.15}, anchor=CENTER)')
            entries.insert(6, f'self.label{x} = Label(self, text="Temperatuur: ", background="#2B323F", fg="white")')
            entries.insert(7, f'self.label{x}.place(relx={x_position-.07:.2f}, rely={y_position-.08}, anchor=CENTER)')
            entries.insert(8, f'self.label{x} = Label(self, text="{x*3} °C", background="#2B323F", fg="dodger blue")')
            entries.insert(9, f'self.label{x}.place(relx={x_position-.03:.2f}, rely={y_position-.08}, anchor=CENTER)')
            entries.insert(10, f'self.label{x} = Label(self, text="Licht: ", background="#2B323F", fg="white")')
            entries.insert(11, f'self.label{x}.place(relx={x_position-.07:.2f}, rely={y_position-.03}, anchor=CENTER)')
            entries.insert(12, f'self.label{x} = Label(self, text="Status: ", background="#2B323F", fg="white")')
            entries.insert(13, f'self.label{x}.place(relx={x_position-.07:.2f}, rely={y_position+.04}, anchor=CENTER)')
            entries.insert(14, f'self.label{x} = Label(self, text="Device {x}", background="#2B323F", fg="white")')
            entries.insert(15, f'self.label{x}.place(relx={x_position:.2f}, rely={y_position-.16}, anchor=CENTER)')

            x_position += .3

            for items in entries:
                exec(items)


    def make_background(self):
        Canvas(self)
        filename = PhotoImage(file="C:/Users/iiwil/Desktop/bg.png")
        background_label = Label(self, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        return filename

    def center_window(self):
        window_width = self.winfo_screenwidth()-500
        window_height = self.winfo_screenheight()-230

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = screen_width / 2 - window_width / 2
        y = screen_height / 2 - window_height / 2
        self.geometry("%dx%d+%d+%d" % (window_width, window_height, x, y))
