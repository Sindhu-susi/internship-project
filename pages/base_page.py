from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, WebDriverException
import time
import allure


class Page:
    def __init__(self,driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    @allure.step("Open URL: {url}")
    def open_url(self,url):
        self.driver.get(url)

    @allure.step("Find element: {locator}")
    def find_element(self,*locator):
        return self.driver.find_element(*locator)
    def find_elements(self,*locator):
        return self.driver.find_elements(*locator)

    @allure.step("Click element: {locator}")
    def click(self, *locator):
        wait = WebDriverWait(self.driver, 25)  # longer wait for slow BrowserStack / popups

        # optional: wait for main container first
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dashboard-container")))
        except:
            pass

        # wait for element presence
        element = wait.until(EC.presence_of_element_located(locator))

        # scroll into view
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)

        try:
            element.click()
        except (ElementClickInterceptedException, WebDriverException):
            try:
                self.driver.execute_script("arguments[0].click();", element)
            except Exception as e:
                import time
                timestamp = int(time.time())
                self.driver.save_screenshot(f"screenshot_fail_{timestamp}.png")
                raise e

    @allure.step("Input text '{text}' into element: {locator}")
    def input_text(self,  locator,text,):
       #self.wait.until(EC.visibility_of_element_located(locator)).send_keys(text)
       element = self.wait.until(EC.visibility_of_element_located(locator))
       self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
       element.clear()
       element.send_keys(text)

    @allure.step("Verify partial text '{expected_partial_text}' in element: {locator}")
    def verify_partial_text(self, expected_partial_text, *locator):
        actual_text = self.find_element(*locator).text
        assert expected_partial_text in actual_text, \
            f"Expected {expected_partial_text} not in actual {actual_text}"

    @allure.step("Get text from element: {locator}")
    def get_text(self, *locator):
           # return self.wait.until(EC.visibility_of_element_located(*locator)).text
           element = self.wait.until(EC.visibility_of_element_located(locator))
           self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
           return element.text

    @allure.step("Check if element is visible: {locator}")
    def is_visible(self, locator,timeout=20):
            #return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()
            """
               Waits for element to be visible, scrolls it into view for headless, and returns True/False
               """
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located(locator)
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
                return element.is_displayed()
            except (TimeoutException, NoSuchElementException):
                return False
