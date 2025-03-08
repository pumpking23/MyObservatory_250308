from .homepage import HomePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class MainPage(HomePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.menu_tab = (By.ACCESSIBILITY_ID, "Menu, left side panel")
        self.service_tab = (By.ACCESSIBILITY_ID, "Forecast & Warning Services")
        self.weather_tab = (By.ACCESSIBILITY_ID, "9-Day Forecast")
        self.remark_tab = (By.XPATH, "//XCUIElementTypeButton[@label='Remark']")

    def click_menu_tab(self):
        # wait for loading
        WebDriverWait(self.driver, 100).until(
            EC.presence_of_element_located((By.ACCESSIBILITY_ID, "MyObservatory"))
        )
        self.driver.find_element(*self.menu_tab).click()

    # open the Forecast & Warning Services
    def click_service_tab(self):
        self.driver.find_element(*self.service_tab).click()

    # open the 9-Day Forecast
    def click_weather_tab(self):
        self.driver.find_element(*self.weather_tab).click()

    # check the remark
    def click_remark_tab(self):
        self.driver.find_element(*self.remark_tab).click()
