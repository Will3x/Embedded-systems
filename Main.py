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
    sys.exit('You need the following modules:\n\n[1] - pyfiglet\n[2] - tkinter\n[3] - serial\n[4] - re\n'
             '[5] - functools.\n\nTry running \'pip install [module]\' for the missing module(s).\nTo see a list of '
             'installed packages, run \'pip list\'')


if __name__ == '__main__':

    print(pyfiglet.figlet_format("POWERED BY\nIT - WORKS"))

    while 1:
        try:
            read_speed = int(input('Set read speed in seconds (1 - 5): '))
        except ValueError:
            print('Error: please enter an integer.\n')
            continue

        if 1 <= read_speed <= 5:
            break
        print('Error: speed should be between 1 and 5.\n')

    print('Speed set to: {} seconds.\n\nStarting program.\nAttempting to connect...\n'.format(read_speed))

    dashboard_view = dv.DashboardView()
    dashboard_model = dm.DashboardModel()
    dashboard_controller = dc.DashboardController(dashboard_view, dashboard_model)

    dashboard_model.setup()
    se.SerialController.setup()

    dashboard_view.setup(read_speed*1000)
    dashboard_view.start()

