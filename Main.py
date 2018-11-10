from view import DashboardView as dv
from controller import DashboardController as dc, SerialController as se
from model import DashboardModel as dm

if __name__ == '__main__':
    dashboard_view = dv.DashboardView()
    dashboard_model = dm.DashboardModel()
    dashboard_controller = dc.DashboardController(dashboard_view, dashboard_model)

    dashboard_model.setup()
    se.SerialController.setup()
    dashboard_view.setup(3000)

    dashboard_view.start()
