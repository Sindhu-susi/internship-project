from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from app.application import Application


def browser_init(context):
    """
    :param context: Behave context
      """

    #
    # driver_path = ChromeDriverManager().install()
    # context.driver = webdriver.Chrome(service=service)
    #
    # context.driver.maximize_window()
    # context.driver.implicitly_wait(4)
    # context.app = Application(context.driver)

    browser = context.config.userdata.get("browser", "chrome")
    headless = context.config.userdata.get("headless", "true")

    # ---------- CHROME ----------
    if browser == "chrome":
        chrome_options = ChromeOptions()

        if headless.lower() == "true":
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")

        driver_path = ChromeDriverManager().install()
        service = ChromeService(driver_path)
        context.driver = webdriver.Chrome(service=service, options=chrome_options)

    # ---------- FIREFOX ----------
    elif browser == "firefox":
        options = FirefoxOptions()

        if headless.lower() == "true":
            options.add_argument("--headless")

        service = FirefoxService(GeckoDriverManager().install())
        context.driver = webdriver.Firefox(service=service, options=options)
        context.driver.set_window_size(1920, 1080)


    else:
        raise Exception("Browser not supported!")

    context.driver.implicitly_wait(15)
    context.driver.maximize_window()
    context.app = Application(context.driver)

def before_scenario(context, scenario):
    print('\nStarted scenario: ', scenario.name)
    browser_init(context)


def before_step(context, step):
    print('\nStarted step: ', step)


def after_step(context, step):
    if step.status == 'failed':
        print('\nStep failed: ', step)


def after_scenario(context, feature):
    context.driver.quit()
