
import pytest
import re
import time
import random
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import desire_caps, appium_server
from pages.weather_page import MainPage
from appium.options.android import UiAutomator2Options
from appium import webdriver


@pytest.fixture(scope="module")
def driver():
    options = UiAutomator2Options().load_capabilities(desire_caps)
    driver = webdriver.Remote(command_executor=appium_server, options=options)
    yield driver
    time.sleep(3)
    driver.quit()


@pytest.mark.dependency()
def test_homepage_tab(driver):
    main_page = MainPage(driver)
    main_page.click_menu_tab()


@pytest.mark.dependency(depends=["test_homepage_tab"])
def test_service_tab(driver):
    main_page = MainPage(driver)
    main_page.click_service_tab()


@pytest.mark.dependency(depends=["test_service_tab"])
def test_weather_tab(driver):
    # main task is to check this tab page
    main_page = MainPage(driver)
    main_page.click_weather_tab()

    # Check the header is Forecast
    current_tab_text = driver.find_element(By.ACCESSIBILITY_ID, 'Weather Forecast')
    assert current_tab_text is not None, f'cannot open the weather forecast page'

    # simply check the summary is about forecast
    element = driver.find_element(
        By.IOS_PREDICATE,
        'label CONTAINS "will" OR label CONTAINS "next week"'
    )
    assert element is not None, f'error introduction about Forecast'

    # Check the 9-Day Forecast tab
    element = driver.find_element(
        By.IOS_PREDICATE,
        'label CONTAINS "9-Day Forecast"'  # iOS
    )
    assert element is not None, f'error tab'

    # confirm the tab is selected
    is_selected = element.get_attribute('selected')
    assert bool(is_selected) is True, f"Expected Tab to be selected, but got '{is_selected}'"

    # check the other tabs is available
    tab_element_local = driver.find_element(By.ACCESSIBILITY_ID, "Local Forecast")
    tab_element_extend = driver.find_element(By.ACCESSIBILITY_ID, "Extended Outlook")

    # pick one randomly to check if it's unselected and enabled
    tab_element = random.choice([tab_element_extend, tab_element_local])
    if tab_element.get_attribute("selected") == "false" and tab_element.is_enabled():
        print("The function of the other tab is fine")
    else:
        print("error tab function")

    # find the element of single-day temperature
    temperature_elements = driver.find_elements(
        By.XPATH, "//XCUIElementTypeStaticText[contains(@label, '℃')]"
    )
    # confirm if the temperature is within normal range
    pattern = r'\d{1,2}\s*-\s*\d{1,2}℃\s*\d{1,3}\s*-\s*\d{1,3}%'
    for element in temperature_elements:
        assert bool(re.match(pattern, element.get_attribute('label')))

    assert len(temperature_elements) == 9, f'error days'

    # check date
    for n in range(9):
        select_date = get_future_date(n+1)
        print(select_date)
        xpath = f"//XCUIElementTypeStaticText[contains(@label, '{select_date}')]"
        temperature_elements = driver.find_element(By.XPATH, xpath)
        print(temperature_elements.text)
        assert is_xpath_exists(driver, xpath), f"No elements found for XPath: {xpath}"


@pytest.mark.dependency(depends=["test_weather_tab"])
def test_remark_tab(driver):
    main_page = MainPage(driver)
    main_page.click_remark_tab()

    wait = WebDriverWait(driver, 10)
    remark_header = wait.until(
        EC.presence_of_element_located((By.XPATH, "//XCUIElementTypeStaticText[@label='Remark']"))
    )

    # check if the remark is opened
    assert remark_header.text == "Remark", "弹窗的 header 不是 'Remark'"


def is_xpath_exists(driver, xpath, timeout=10):
    try:
        wait = WebDriverWait(driver, timeout)
        elements = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
        return len(elements) > 0
    except:
        return False


def get_future_date(days_later):
    now = datetime.now()
    future_date = now + timedelta(days=days_later)
    return future_date.strftime('%d %b (%a)')