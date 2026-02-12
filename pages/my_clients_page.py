from selenium.webdriver.common.by import By
from pages.base_page import Page

class MyClientsPage(Page):

    PAGE_HEADER= (By.XPATH,"//a[@class='menu-text-link-leaderboard w--current']")

    OPTIONS = [(By.XPATH,"//div[contains(text(),'History')]"),
               (By.XPATH,"//div[contains(text(),'Waiting')]"),
               (By.XPATH,"//div[contains(text(),'Confirmed')]"),
               (By.XPATH,"//div[contains(text(),'Request')]"),
               (By.XPATH,"//div[contains(text(),'Booked')]"),
               (By.XPATH,"//div[contains(text(),'Successful')]"),
               (By.XPATH,"//div[contains(text(),'Commission paid')]")
               ]

    def verify_page_opened(self):
      return self.is_visible(self.PAGE_HEADER)

    def verify_all_options_present(self):
        for option in self.OPTIONS:
            if not self.is_visible(option):
                return False
        return True


