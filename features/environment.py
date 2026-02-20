from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from app.application import Application
import os
import allure
from datetime import datetime

BROWSERSTACK_USERNAME = os.getenv("BROWSERSTACK_USERNAME", "sindhusukumaran_wl2msu")
BROWSERSTACK_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY", "fpsYv6Usnzat7ChkVrCP")


def browser_init(context):
    browser = context.config.userdata.get("browser", "chrome").lower()
    headless = context.config.userdata.get("headless", "true").lower()
    use_browserstack = context.config.userdata.get("browserstack", "false").lower() == "true"

    if use_browserstack:
        # ---------- BrowserStack ----------
        from selenium.webdriver.safari.options import Options as SafariOptions

        options = SafariOptions()

        # BrowserStack W3C format (REQUIRED for Safari)
        bstack_options = {
            "os": "OS X",
            "osVersion": "Ventura",  # you can use: Monterey / Ventura / Sonoma
            "browserVersion": "latest",
            "buildName": "Build 1",
            "sessionName": "Behave Safari Test",
            "debug": "true",
            "networkLogs": "true"
        }

        options.set_capability("browserName", "Safari")
        options.set_capability("bstack:options", bstack_options)

        # Connect to BrowserStack
        context.driver = webdriver.Remote(
            command_executor=f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub",
            options=options
        )

    else:
        # ---------- Local Chrome ----------
        if browser == "chrome":
            options = ChromeOptions()
            options.add_experimental_option("prefs", {
                "profile.default_content_setting_values.notifications": 2
            })
            if headless == "true":
                options.add_argument("--headless=new")
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")


            driver_path = ChromeDriverManager().install()
            service = ChromeService(driver_path)
            context.driver = webdriver.Chrome(service=service, options=options)

        # ---------- Local Firefox ----------
        elif browser == "firefox":
            options = FirefoxOptions()
            if headless == "true":
                options.add_argument("--headless")
            service = FirefoxService(GeckoDriverManager().install())
            context.driver = webdriver.Firefox(service=service, options=options)
            context.driver.set_window_size(1920, 1080)
        else:
            raise Exception("Browser not supported!")

    # Common settings
    context.driver.implicitly_wait(15)
    context.driver.maximize_window()
    context.app = Application(context.driver)


# ----------------- Behave hooks -----------------
def before_scenario(context, scenario):
    print('\nStarted scenario: ', scenario.name)
    browser_init(context)
    if hasattr(context, "driver"):
        allure.dynamic.label("browser", context.driver.name)


def before_step(context, step):
    print('\nStarted step: ', step)


def after_step(context, step):
    if step.status == 'failed':
        print('\nStep failed: ', step)
        if hasattr(context, "driver"):
            screenshot_name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            context.driver.save_screenshot(screenshot_name)

            allure.attach.file(
                screenshot_name,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )


def after_scenario(context, scenario):
    if hasattr(context, "driver"):
        context.driver.quit()