import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Ожидание до 10 секунд

    user_name_field = '//*[@data-test="username"]'
    password_field = '//*[@data-test="password"]'
    login_button = '//*[@data-test="login-button"]'
    error_message_container = '//*[@data-test="error"]'

    def open(self):
        self.driver.get("https://www.saucedemo.com/")

    def get_username_input(self):
        return self.wait.until(EC.presence_of_element_located((By.XPATH, self.user_name_field)))

    def get_password_input(self):
        return self.wait.until(EC.presence_of_element_located((By.XPATH, self.password_field)))

    def get_login_button(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, self.login_button)))

    def error_message(self):
        return self.driver.find_element(By.XPATH, self.error_message_container)

    def enter_username(self, username):
        username_field = self.get_username_input()
        username_field.clear()
        username_field.send_keys(username)

    def enter_password(self, password):
        password_field = self.get_password_input()
        password_field.clear()
        password_field.send_keys(password)

    def click_on_login_button(self):
        self.get_login_button().click()

    def success_login(self, login, password):
        self.enter_username(login)
        self.enter_password(password)
        self.click_on_login_button()

        # # Ожидаем alert от сайта и нажимаем OK
        # WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        # self.driver.switch_to.alert.accept()
