from tkinter import *


class EventController:

    def __init__(self, view):
        self.view = view
        self.canv_light, self.canv_temp = view.canvas

    def buttonclick_event(self, var):
        if var.get() == 1:
            print('Showing light sensor canvas')
            self.view.radio1.config(fg="white")
            self.view.radio2.config(fg="black")
            self.canv_light.place(relx=0.5, rely=0.37, anchor=CENTER)
            self.canv_temp.place_forget()

        elif var.get() == 2:
            print('Showing temperature sensor canvas')
            self.view.radio1.config(fg="black")
            self.view.radio2.config(fg="white")
            self.canv_temp.place(relx=0.5, rely=0.37, anchor=CENTER)
            self.canv_light.place_forget()

        elif var.get() == 3:
            """ TODO: CLEAN THIS MESS """
            self.view.manual1.config(state=NORMAL)
            self.view.manual2.config(state=NORMAL)

            self.view.manual_btn1.config(state=NORMAL)
            self.view.manual_btn2.config(state=NORMAL)

            self.view.setbtn2.config(state=NORMAL, fg='white')
            self.view.setbtn1.config(state=DISABLED, fg='black', bg='gray90')

            self.view.label1.config(state=DISABLED)
            self.view.label2.config(state=DISABLED)
            self.view.label3.config(state=DISABLED)
            self.view.label4.config(state=DISABLED)

            self.view.entry1.config(state=DISABLED)
            self.view.entry2.config(state=DISABLED)
            self.view.entry3.config(state=DISABLED)
            self.view.entry4.config(state=DISABLED)

        elif var.get() == 4:
            """ TODO: CLEAN THIS MESS """
            self.view.manual1.config(state=DISABLED)
            self.view.manual2.config(state=DISABLED)

            self.view.manual_btn1.config(state=DISABLED)
            self.view.manual_btn2.config(state=DISABLED)

            self.view.setbtn2.config(state=DISABLED, fg='black', bg='gray90')
            self.view.setbtn1.config(state=NORMAL, fg='white')

            self.view.label1.config(state=NORMAL)
            self.view.label2.config(state=NORMAL)
            self.view.label3.config(state=NORMAL)
            self.view.label4.config(state=NORMAL)

            self.view.entry1.config(state=NORMAL)
            self.view.entry2.config(state=NORMAL)
            self.view.entry3.config(state=NORMAL)
            self.view.entry4.config(state=NORMAL)

