from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def get_items(self):
        return self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item")))

    def get_items_amount(self):
        return len(self.get_items())

    def all_items_are_displayed(self):
        return all(item.is_displayed() for item in self.get_items())

    def get_item_names(self):
        return [item.text for item in self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item_name")))]

    def all_items_names_are_displayed(self):
        return all(name.strip() != "" for name in self.get_item_names())

    def all_item_names_are_not_empty(self):
        return all(bool(name.strip()) for name in self.get_item_names())

    def all_item_names_contains_sauce_labs(self):
        return all(name.startswith("Sauce Labs") for name in self.get_item_names())

    def get_item_price(self, item_name):
        """Получает цену товара по его названию (в формате строки с $)"""
        item_xpath = f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//div[@class='inventory_item_price']"
        return self.wait.until(EC.presence_of_element_located((By.XPATH, item_xpath))).text

    def add_item_to_cart(self, item_name):
        """Добавляет товар в корзину по названию"""
        button_xpath = f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, button_xpath))).click()

    def go_to_cart(self):
        """Переход в корзину"""
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))).click()




