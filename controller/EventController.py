from tkinter import *
import Style as st
from model import InstructionModel as instr, SensordataModel as se
from controller import SerialController as ser


class EventController:

    def __init__(self, view):
        self.view = view
        self.canv_light, self.canv_temp = view.canvas

    @staticmethod
    def check(device, instruction, *value):
        if instr.InstructionModel.check_value(instruction, value):
            ser.SerialController.write(device, instruction, value)

    @staticmethod
    def get_values():
        return ser.SerialController.current_values()

    @staticmethod
    def status_open_closed(device, values):
        return se.SensordataModel.status_open_closed(device, values)

    def buttonclick_event(self, var):
        # Roll out.
        if var == 5:
            device = int(self.view.wm_title()[7:8])
            ser.SerialController.write(device, 1)
            return

        # Roll in.
        if var == 6:
            device = int(self.view.wm_title()[7:8])
            ser.SerialController.write(device, 2)
            return

        elif var.get() == 1:
            self.canv_light.place(relx=0.5, rely=0.37, anchor=CENTER)
            self.canv_temp.place_forget()

        elif var.get() == 2:
            self.canv_temp.place(relx=0.5, rely=0.37, anchor=CENTER)
            self.canv_light.place_forget()

        elif var.get() == 3:
            ser.SerialController.write(int(self.view.wm_title()[7:8]), 8, '1')

            self.view.graph_controller.view.hide_borders()
            self.view.graph_controller2.view.hide_borders()

            self.view.manual1.config(state=NORMAL)
            self.view.manual2.config(state=NORMAL)

            self.view.manual_btn_on.config(state=NORMAL)
            self.view.manual_btn2.config(state=NORMAL)

            self.view.setbtn2.config(state=NORMAL, bg=st.btn_bg_blue)
            self.view.setbtn1.config(state=DISABLED, bg=st.btn_bg_grey)

            self.view.label1.config(state=DISABLED)
            self.view.label2.config(state=DISABLED)
            self.view.label3.config(state=DISABLED)
            self.view.label4.config(state=DISABLED)

            self.view.entry1.config(state=DISABLED)
            self.view.entry2.config(state=DISABLED)
            self.view.entry3.config(state=DISABLED)
            self.view.entry4.config(state=DISABLED)

        elif var.get() == 4:
            ser.SerialController.write(int(self.view.wm_title()[7:8]), 8, '0')

            self.view.graph_controller.view.show_borders()
            self.view.graph_controller2.view.show_borders()

            self.view.manual1.config(state=DISABLED)
            self.view.manual2.config(state=DISABLED)

            self.view.manual_btn_on.config(state=DISABLED)
            self.view.manual_btn2.config(state=DISABLED)

            self.view.setbtn2.config(state=DISABLED, bg=st.btn_bg_grey)
            self.view.setbtn1.config(state=NORMAL, bg=st.btn_bg_blue)

            self.view.label1.config(state=NORMAL)
            self.view.label2.config(state=NORMAL)
            self.view.label3.config(state=NORMAL)
            self.view.label4.config(state=NORMAL)

            self.view.entry1.config(state=NORMAL)
            self.view.entry2.config(state=NORMAL)
            self.view.entry3.config(state=NORMAL)
            self.view.entry4.config(state=NORMAL)
