from pages.dashboard_page import DashboardPage
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.my_clients_page import MyClientsPage


class Application:

    def __init__(self, driver):

        self.main_page = MainPage(driver)
        self.login_page = LoginPage(driver)
        self.dashboard_page = DashboardPage(driver)
        self.my_clients_page = MyClientsPage(driver)
