from selenium.webdriver.common.by import By
from pages.base_page import Page

class LoginPage(Page):

   SIGN_IN = (By.XPATH, "//div[@class='sing-in-text']")
   EMAIL=(By.XPATH, "//input[@id='email-2']")
   PASSWORD=(By.XPATH, "//input[@id='field']")
   LOGIN_BTN=(By.XPATH,"//a[@class='login-button w-button']")

   def login(self, email, password):
        self.click(*self.SIGN_IN)
        self.input_text(self.EMAIL, email)
        self.input_text(self.PASSWORD, password)
        self.click(*self.LOGIN_BTN)
