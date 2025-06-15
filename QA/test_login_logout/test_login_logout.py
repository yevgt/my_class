from operator import contains
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

class TestLoginLogout:

    @pytest.fixture(scope="function", autouse=True)
    def setup_and_teardown(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.get("http://the-internet.herokuapp.com/login")
        yield
        self.driver.quit()

    # def test_login_logout(self):
    #     # Ввод имени пользователя
    #     username_input = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.ID, "username"))
    #     )
    #     username_input.send_keys("tomsmith")
    #
    #     # Ввод пароля
    #     password_input = self.driver.find_element(By.ID, "password")
    #     password_input.send_keys("SuperSecretPassword!")
    #
    #     # Нажатие кнопки Login
    #     login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    #     login_button.click()
    #
    #     # Проверка, что появился текст "You logged into a secure area!"
    #     success_message = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, "div.flash.success"))
    #     )
    #
    #     assert "You logged into a secure area!" in success_message.text
    #
    #     # Проверка заголовка "Secure Area"
    #     header = self.driver.find_element(By.TAG_NAME, "h2")
    #     assert header.text == "Secure Area"
    #
    #     # Проверка наличия кнопки "Logout"
    #     logout_button = self.driver.find_element(By.CSS_SELECTOR, "a.button.secondary.radius")
    #     assert logout_button.is_displayed()
    #
    #     # Нажатие кнопки Logout
    #     logout_button.click()
    #
    #     # Проверка, что пользователь вернулся на страницу авторизации
    #     login_page_header = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.TAG_NAME, "h2"))
    #     )
    #     assert login_page_header.text == "Login Page"
    #
    #     # Проверка наличия поля для ввода имени пользователя
    #     assert self.driver.find_element(By.ID, "username").is_displayed()
    #
    # def test_invalid_username(self):
    #     # Ввод неверного имени пользователя
    #     username_input = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.ID, "username"))
    #     )
    #     username_input.send_keys("wronguser")
    #
    #     # Ввод пароля
    #     password_input = self.driver.find_element(By.ID, "password")
    #     password_input.send_keys("SuperSecretPassword!")
    #
    #     # Нажатие кнопки Login
    #     login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    #     login_button.click()
    #
    #     # Проверка сообщения об ошибке
    #     error_message = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, "div.flash.error"))
    #     )
    #
    #     assert "Your username is invalid!" in error_message.text

    def test_invalid_password(self):
        # Ввод имени пользователя
        username_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        # Решение
        username_input.send_keys("tomsmith")

        # ввод пароля
        invalid_password_input = self.driver.find_element(By.ID, "password")
        invalid_password_input.send_keys("testpassword?")

        # нажатие кнопки Login
        loggin_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        loggin_button.click()

        # Проверка сообщения об ошибке
        error_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.flash.error"))
        )
        assert "Your password is invalid!" in error_message.text

    def test_invalid_username_and_password(self):
        # Ввод неверного имени пользователя
        invalid_username = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        # Решение
        invalid_username.send_keys("test")

        # Ввод пароля
        invalid_pass = self.driver.find_element(By.ID, "password")
        invalid_pass.send_keys("123asd789")

        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()


        error_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.flash.error"))
        )
        assert "Your username is invalid!" in error_message.text
