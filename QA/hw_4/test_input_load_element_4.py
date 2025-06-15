from operator import contains
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    yield driver
    driver.quit()

# Задание 1: Проверка изменения текста кнопки
def test_text_input(driver):
    driver.get("http://uitestingplayground.com/textinput")
    wait = WebDriverWait(driver, 10)
    input_field = wait.until(
        EC.presence_of_element_located((By.ID, 'newButtonName'))
    )
    input_field.clear()
    input_field.send_keys("ITCH")

    blue_button = driver.find_element(By.ID, "updatingButton")
    blue_button.click()

    wait.until(EC.text_to_be_present_in_element((By.ID, "updatingButton"), "ITCH"))
    assert blue_button.text == "ITCH", "Ожидался текст кнопки 'ITCH'"

# Задание 2: Проверка загрузки изображений
def test_loading_images(driver):
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/loading-images.html")
    wait = WebDriverWait(driver, 15)  # Ожидание загрузки изображений
    third_image = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@id='image-container']/img)[3]")))
    # third_image = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#image-container img:nth-of-type(3)")))

    alt_text = third_image.get_attribute("alt")
    assert alt_text == "award", f"Ожидаемый alt 'award', но получено '{alt_text}'"

