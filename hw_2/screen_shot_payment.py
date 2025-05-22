from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

# Настройка драйвера для Firefox с использованием WebDriverManager
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

try:
    # Открытие страницы
    driver.get("https://itcareerhub.de")
    # Задержка для загрузки страницы
    sleep(10)
    # Поиск ссылки "Способы оплаты" и клик
    # about_link = driver.find_element(By.LINK_TEXT, "Способы оплаты")
    about_link = driver.find_element(By.LINK_TEXT, "Zahlungsarten")
    about_link.click()
    # element = driver.find_element(By.XPATH,"//*[contains(text(), 'Способы оплаты обучения')]")
    # Изменение размера окна
    # driver.set_window_size(640, 460)
    # Задержка перед скриншотом
    sleep(20)
    driver.save_screenshot("./payment.png")  # Сохранение скриншота в текущую папку
finally:
    # Закрытие браузера
    driver.quit()