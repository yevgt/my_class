import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from QA.hw_6_pom.pages.inventory_page import InventoryPage
from QA.hw_6_pom.pages.login_page import LoginPage
from QA.hw_6_pom.pages.cart_page import CartPage
from QA.hw_6_pom.pages.checkout_page import CheckoutPage
from QA.hw_6_pom.pages.overview_page import OverviewPage


class BaseTest:
    @pytest.fixture(autouse=True)
    def setup(self):
        options = Options()
        options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2
        })
        # options.add_argument("--incognito")
        options.add_argument("--guest")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        self.driver.maximize_window()
        self.driver.get("https://www.saucedemo.com/")

        self.login_page = LoginPage(self.driver)
        self.inventory_page = InventoryPage(self.driver)
        self.cart_page = CartPage(self.driver)
        self.checkout_page = CheckoutPage(self.driver)
        self.overview_page = OverviewPage(self.driver)

        yield
        self.driver.quit()

