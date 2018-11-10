from view import DashboardView as dv
from controller import DashboardController as dc, SerialController as se
from model import DashboardModel as dm
import sys
try:
    import pyfiglet
    import tkinter
    import functools
    import serial
    import re
except ImportError:
    sys.exit('You need the following modules: pyfiglet, tkinter, serial, re and functools.\n'
             'Try running pip install for the missing module(s).')


if __name__ == '__main__':

    print(pyfiglet.figlet_format("POWERED BY\nIT WORKS"))

    while 1:
        try:
            speed = int(input('Set speed in seconds (1 - 5): '))
        except ValueError:
            print('Error: please enter an integer.')
            continue

        if 1 <= speed <= 10:
            break

        print('Error: speed should be between 1 and 5.\n')

    print('Speed set to: {}s\n\nStarting program.\nAttempting to connect...\n'.format(speed))

    dashboard_view = dv.DashboardView()
    dashboard_model = dm.DashboardModel()
    dashboard_controller = dc.DashboardController(dashboard_view, dashboard_model)

    dashboard_model.setup()
    se.SerialController.setup()

    dashboard_view.setup(speed*1000)
    dashboard_view.start()

