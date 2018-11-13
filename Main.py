from view import DashboardView as dv
from controller import DashboardController as dc, SerialController as se
from model import DashboardModel as dm
import Base_values as ba
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
            read_speed = int(input('Set read speed in seconds (1 - 3): '))
            update_speed = int(input(f'Set update speed for the graphs in seconds (6 - 60): '))
        except ValueError:
            print('Error: please enter integers only.\n')
            continue

        if 1 <= read_speed <= 3 and 6 <= update_speed <= 60:
            break
        if not 1 <= read_speed <= 3:
            print('Error: read speed should be between 1 and 3.\n')
        if not 6 <= update_speed <= 60:
            print('Error: update speed should be between 3 and 60\n')

    print('\nRead speed: {} seconds.\nUpdate speed: {} seconds.\n\nStarting program.\nAttempting to connect...\n'
          .format(read_speed, update_speed))

    ba.graph_update = round(update_speed / read_speed)

    dashboard_view = dv.DashboardView()
    dashboard_model = dm.DashboardModel()
    dashboard_controller = dc.DashboardController(dashboard_view, dashboard_model)

    dashboard_model.setup()
    se.SerialController.setup()

    dashboard_view.setup(read_speed*1000)
    dashboard_view.start()

