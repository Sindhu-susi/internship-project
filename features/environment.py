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
    headless = context.config.userdata.get("headless", "false").lower()=="true"
    use_browserstack = context.config.userdata.get("browserstack", "false").lower() == "true"
    mobile = context.config.userdata.get("mobile", "false").lower() == "true"

    if use_browserstack:
        # ---------- BrowserStack ----------
        if use_browserstack:
            from selenium.webdriver.chrome.options import Options

            options = Options()

            build_name = f"Behave Automation Build {datetime.now().strftime('%Y%m%d_%H%M%S')}"
            session_name = context.scenario.name if hasattr(context, "scenario") else "Test Session"

            # ---------------- Desktop Chrome on BrowserStack ----------------
            bstack_options = {
                "os": "Windows",
                "osVersion": "11",
                "browserVersion": "latest",
                "buildName": build_name,
                "sessionName": session_name,
                "debug": "true",
                "networkLogs": "true",
                "video": "true"
            }

            options.set_capability("browserName", "Chrome")
            options.set_capability("bstack:options", bstack_options)

            # ---------------- Mobile Emulation ----------------
            mobile_emulation = {
                "deviceMetrics": {"width": 803, "height": 844, "pixelRatio": 3.0},
                "userAgent": (
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                    "Version/16.0 Mobile/20A534 Safari/604.1"
                )
            }

            options.add_experimental_option("mobileEmulation", mobile_emulation)

            context.driver = webdriver.Remote(
                command_executor=f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub",
                options=options
            )

            # Optional: Set window size explicitly
            context.driver.set_window_size(803, 844)

    else:
        # ---------- Local Chrome ----------
        if browser == "chrome":
            options = ChromeOptions()

            # ----------------- Mobile emulation -----------------
            if mobile:
                # Instead of named device (can hide UI), use manual iPhone 14 Pro Max size
                width, height = 803, 900 # iPhone 14 Pro Max
                # User-Agent for iPhone 14 Pro Max
                user_agent = (
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                    "Version/16.0 Mobile/20A534 Safari/604.1"
                )
                mobile_emulation = {
                    "deviceMetrics": {"width": width, "height": height, "pixelRatio": 3.0},
                    "userAgent": user_agent
                }
                options.add_experimental_option("mobileEmulation", mobile_emulation)

            # ----------------- Disable notifications -----------------
            options.add_experimental_option("prefs", {
                "profile.default_content_setting_values.notifications": 2
            })

            if headless:
                options.add_argument("--headless=new")
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")

            service = ChromeService(ChromeDriverManager().install())
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

    if not mobile:
        context.driver.maximize_window()

    context.driver.implicitly_wait(15)
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

    """
    if use_browserstack:
        from selenium.webdriver.chrome.options import Options

        options = Options()

        device = context.config.userdata.get("device", "Samsung Galaxy S23")
        os_version = context.config.userdata.get("os_version", "13.0")

        bstack_options = {
            "deviceName": device if mobile else None,
            "osVersion": os_version,
            "realMobile": "true" if mobile else None,
            "os": "OS X" if not mobile else None,
            "browserVersion": "latest",
            "buildName": f"Behave Automation Build {datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "sessionName": context.scenario.name if hasattr(context, "scenario") else "Test Session",
            "debug": "true",
            "networkLogs": "true",
            "video": "true"

        }

        # Remove None values
        bstack_options = {k: v for k, v in bstack_options.items() if v is not None}

        options.set_capability("browserName", "Chrome")
        options.set_capability("bstack:options", bstack_options)

        context.driver = webdriver.Remote(
            command_executor=f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub",
            options=options
        )
    """