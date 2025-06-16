from time import sleep
import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


# Фикстура для WebDriver
@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

# Тест загрузки файла
class TestIframeText:
    def test_find_text_in_iframe(self, browser):
        url = "https://bonigarcia.dev/selenium-webdriver-java/iframes.html"
        browser.get(url)

        # Переключаемся в iframe
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "my-iframe"))
        )
        browser.switch_to.frame(iframe)

        # Находим параграф
        # lead_paragraph = browser.find_element(By.CSS_SELECTOR, "p.lead")
        # sleep(5)
        lead_paragraph = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p.lead"))
        )

        # Проверяем, что нужный текст содержится в параграфе
        target_text = "Lorem ipsum dolor sit amet consectetur adipiscing elit habitant metus"
        assert target_text in lead_paragraph.text, "Текст не найден в параграфе"

        # Проверяем, что параграф отображается
        assert lead_paragraph.is_displayed(), "Параграф с текстом не отображается"

        print("Текст найден и отображается!")


class TestDragAndDrop:
    def test_drag_and_drop_photo(self, browser):
        url = "https://www.globalsqa.com/demo-site/draganddrop/"
        browser.get(url)

        try:
            consent_button = WebDriverWait(browser, 7).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".fc-cta-consent > p:nth-child(2)"))
        )
            consent_button.click()
        except Exception:
            pass

        # Страница с drag&drop находится во вложенном iframe!
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.demo-frame"))
        )
        browser.switch_to.frame(iframe)

        # Находим все изображения для перетаскивания (основная область)
        images = WebDriverWait(browser, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#gallery > li"))
        )
        assert len(images) == 4, "Ожидалось 4 фотографии в галерее до перетаскивания"

        # Захватываем первую фотографию (верхний левый элемент)
        first_image = images[0]

        # Находим область корзины
        trash = browser.find_element(By.CSS_SELECTOR, "#trash")

        # Перетаскиваем изображение в корзину
        action = ActionChains(browser)
        action.drag_and_drop(first_image, trash).pause(2).perform()

        # Проверяем, что в корзине появилась одна фотография
        trash_items = browser.find_elements(By.CSS_SELECTOR, "#trash li")
        assert len(trash_items) == 1, "В корзине должна быть 1 фотография после перетаскивания"

        # Проверяем, что в основной области осталось 3 фотографии
        gallery_items = browser.find_elements(By.CSS_SELECTOR, "#gallery > li")
        assert len(gallery_items) == 3, "В галерее должно остаться 3 фотографии после перетаскивания"

        print("Фотография успешно перемещается в корзину. В галерее осталось 3 фотографии.")


class TestFillForm:
    def test_fill_form_and_check_alert(self,browser):
        url = "http://suninjuly.github.io/huge_form.html"
        browser.get(url)

        # Решение
        input_text = browser.find_elements(By.TAG_NAME, "input")
        for string in input_text:
            string.send_keys("test")
        # time.sleep(5)
        button = browser.find_element(By.CLASS_NAME, "btn-default")
        button.click()

        wait = WebDriverWait(browser, 10)
        alert = wait.until(EC.alert_is_present())
        alert_text = Alert(browser).text
        expected_substring = "Congrats, you've passed the task!"
        assert expected_substring in alert_text, f"Ожидаемая строка '{expected_substring}' отсутствует в alert: '{alert_text}'"

        alert.accept()