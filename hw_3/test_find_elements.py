from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import pytest

@pytest.fixture(params=["chrome"])
def driver(request):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://itcareerhub.de/ru")
    sleep(5)
    yield driver
    driver.quit()

# проверка отображения логотипа ITCareerHub
def test_logo_text(driver):
    try:
        # logo = driver.find_element(By.CSS_SELECTOR, "img[alt='ITCareerHub']")
        logo = driver.find_element(By.XPATH, '//*[@id="rec717872821"]/div/div/div[3]/a/img')
        assert logo.is_displayed()
    except NoSuchElementException:
        print("Логотип ITCareerHub не найден")


# Ссылка “Программы”#
# Ссылка “Способы оплаты”#
# Ссылка “Новости”#
# Ссылка “О нас”#
# Ссылка “Отзывы
def test_titles(driver):
    # Проверка наличия ссылок
    links_texts = ["Программы", "Способы оплаты", "Новости", "О нас", "Отзывы"]
    for text in links_texts:
        try:
            link = driver.find_element(By.LINK_TEXT, text)
            assert link.is_displayed()
        except NoSuchElementException:
            pytest.fail(f'Ссылка "{text}" не найдена')

def test_titles2(driver):
    # Проверка наличия ссылок
    links_texts = ["Программы", "Способы оплаты", "Новости", "О нас", "Отзывы"]
    for text in links_texts:
        links = driver.find_elements(By.LINK_TEXT, text)
        if len(links) == 0:
            print(f'Внимание: ссылка "{text}" не найдена')
        elif not all(link.is_displayed() for link in links):
            print(f'Внимание: ссылка "{text}" найдена, но не отображается')

# Кнопки переключения языка (ru и de)
def test_leng_ru_de(driver):
    try:
        ru_button = driver.find_element(By.XPATH, "//a[text()='ru']")
        de_button =  driver.find_element(By.XPATH, "//a[text()='de']")

        assert ru_button.is_displayed()
        assert de_button.is_displayed()
    except NoSuchElementException:
        print("Кнопки переключения языка не найдены")

# Кликнуть по иконке с телефонной трубкой
def test_phone_icon(driver):
    try:
        tel_link = driver.find_element(By.CSS_SELECTOR, ".phone-icon")
        # tel_link = driver.find_element(By.XPATH, "//a[contains(@href, 'tel:')]")
        tel_link.click()
        print("Клик выполнен")
        sleep(5)
        sms_form = driver.find_element(By.XPATH,
        "//*[contains(text(), 'Если вы не дозвонились, заполните форму на сайте. Мы свяжемся с вами')]")
        assert sms_form.is_displayed()
    except NoSuchElementException as e:
        print(f"Ошибка: {e}")

driver.quit()
