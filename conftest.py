
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from config.config import desire_caps, appium_server


@pytest.fixture(scope="session")
def appium_driver():
    options = UiAutomator2Options().load_capabilities(desire_caps)
    driver = webdriver.Remote(command_executor=appium_server, options=options)
    yield driver
    driver.quit()
