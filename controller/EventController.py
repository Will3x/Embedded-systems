from tkinter import *
import Style as st
from model import InstructionModel as instr
from controller import SerialController as ser


class EventController:

    def __init__(self, view):
        self.view = view
        self.canv_light, self.canv_temp = view.canvas

    def write(self, id, *value):
        if instr.InstructionModel.check_value(id, value):
            # instruction = instr.InstructionModel.getinstruction(id)
            ser.SerialController.write(id, value)

    def buttonclick_event(self, var):
        if var.get() == 1:
            self.canv_light.place(relx=0.5, rely=0.37, anchor=CENTER)
            self.canv_temp.place_forget()

        elif var.get() == 2:
            self.canv_temp.place(relx=0.5, rely=0.37, anchor=CENTER)
            self.canv_light.place_forget()

        elif var.get() == 3:
            """ TODO: CLEAN THIS MESS """
            self.view.manual1.config(state=NORMAL)
            self.view.manual2.config(state=NORMAL)

            self.view.manual_btn_on.config(state=NORMAL)
            self.view.manual_btn2.config(state=NORMAL)

            self.view.setbtn2.config(state=NORMAL, bg=st.btn_bg_blue)
            self.view.setbtn1.config(state=DISABLED, bg="#444D5F")

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

            self.view.manual_btn_on.config(state=DISABLED)
            self.view.manual_btn2.config(state=DISABLED)

            self.view.setbtn2.config(state=DISABLED, bg="#444D5F")
            self.view.setbtn1.config(state=NORMAL, bg=st.btn_bg_blue)

            self.view.label1.config(state=NORMAL)
            self.view.label2.config(state=NORMAL)
            self.view.label3.config(state=NORMAL)
            self.view.label4.config(state=NORMAL)

            self.view.entry1.config(state=NORMAL)
            self.view.entry2.config(state=NORMAL)
            self.view.entry3.config(state=NORMAL)
            self.view.entry4.config(state=NORMAL)
