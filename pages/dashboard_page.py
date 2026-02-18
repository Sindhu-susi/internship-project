from selenium.webdriver.common.by import By
from pages.base_page import Page

class  DashboardPage(Page):

 #SETTINGS=(By.XPATH,"//div[normalize-space()='Settings']")
 #SETTINGS=(By.XPATH,"//div[contains(text(),'Settings')]")
 SETTINGS = (By.XPATH, "//*[normalize-space(text())='Settings']")

 MY_CLIENTS=(By.XPATH,"//a[@href='/my-fixations']")

 def open_settings(self):
    self.click(*self.SETTINGS)
 def open_my_clients(self):
     self.click(*self.MY_CLIENTS)
