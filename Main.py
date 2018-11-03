from view import DashboardView
from controller import DashboardController
from model import SensordataModel

if __name__ == '__main__':
    dashboard_view = DashboardView.DashboardView()
    dashboard_controller = DashboardController.DashboardController(dashboard_view, SensordataModel.SensordataModel())

    dashboard_view.start()
