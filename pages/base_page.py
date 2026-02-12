from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Page:
    def __init__(self,driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
    def open_url(self,url):
        self.driver.get(url)
    def find_element(self,*locator):
        return self.driver.find_element(*locator)
    def find_elements(self,*locator):
        return self.driver.find_elements(*locator)
    def click(self,*locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def input_text(self,  locator,text,):
        self.wait.until(EC.visibility_of_element_located(locator)).send_keys(text)

    def verify_partial_text(self, expected_partial_text, *locator):
        actual_text = self.find_element(*locator).text
        assert expected_partial_text in actual_text, \
            f"Expected {expected_partial_text} not in actual {actual_text}"

    def get_text(self, *locator):
            return self.wait.until(EC.visibility_of_element_located(*locator)).text

    def is_visible(self, locator):
            return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()
