from view import DashboardView
from controller import DashboardController
from model import SensordataModel

if __name__ == '__main__':
    dashboardview = DashboardView.DashboardView()
    dashboardcontroller = DashboardController.DashboardController(dashboardview, SensordataModel.SensordataModel())

    dashboardview.start()


