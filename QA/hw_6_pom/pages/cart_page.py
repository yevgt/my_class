from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def get_cart_item_price(self, item_name):
        item_xpath = f"//div[text()='{item_name}']/ancestor::div[@class='cart_item']//div[@class='inventory_item_price']"
        return self.wait.until(EC.presence_of_element_located((By.XPATH, item_xpath))).text

    def get_items_prices_dict(self):
        # Убедимся, что заголовок корзины действительно прогрузился
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "title")))

        # Дожидаемся наличия хотя бы одного товара
        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "cart_item")))

        prices = {}
        for item in items:
            try:
                name = item.find_element(By.CLASS_NAME, "inventory_item_name").text.strip()
                price = item.find_element(By.CLASS_NAME, "inventory_item_price").text.strip()
                prices[name] = price
            except Exception as e:
                print(f"⚠️ Ошибка при чтении товара: {e}")
        return prices

    def remove_item_from_cart(self, item_name):
        button_xpath = f"//div[text()='{item_name}']/ancestor::div[@class='cart_item']//button"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, button_xpath))).click()

    def proceed_to_checkout(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()
