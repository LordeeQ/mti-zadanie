import sys

from PyQt6.QtWidgets import QApplication

from containers.showroom import Showroom, UserRegistry
from models.people import UserSession
from services.seed import DataSeeder
from ui.dialogs import LoginWindow
from ui.main_window import MainWindow
from ui.style import AppStyle


class AutoShowroomApp:

    def __init__(self, argv):
        self._app = QApplication(argv)
        AppStyle.apply(self._app)
        self._registry = UserRegistry(DataSeeder.users())
        self._showroom = Showroom(DataSeeder.vehicles())
        self._window = None

    def run(self):
        login = LoginWindow(self._registry)
        if not login.exec():
            return 0
        session = UserSession(login.user.login)
        self._window = MainWindow(login.user, session, self._showroom, DataSeeder.vehicle_types())
        self._window.show()
        return self._app.exec()


if __name__ == "__main__":
    sys.exit(AutoShowroomApp(sys.argv).run())
