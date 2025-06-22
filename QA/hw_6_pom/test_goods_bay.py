from base_tests import BaseTest
from dotenv import load_dotenv
import os

load_dotenv()

class TestAllItemsCost(BaseTest):
    # авторизация
    def open_and_login(self):
        self.login_page.open()
        self.login_page.success_login(
            os.getenv("LOGIN"),
            os.getenv("PASSWORD")
        )
        assert self.driver.current_url == "https://www.saucedemo.com/inventory.html", \
            "URL страницы после входа неверен."

    # добавление товара в корзину
    def add_items_to_cart(self, items):
        for item in items:
            self.inventory_page.add_item_to_cart(item)

    # заполнение формы
    def go_to_checkout(self):
        self.inventory_page.go_to_cart()
        self.cart_page.proceed_to_checkout()

    # данные для заполнения
    def fill_checkout_info(self):
        self.checkout_page.fill_user_info("Test", "User", "12345")

    # итоговая сумма
    def assert_total_sum(self, expected_total):
        total = self.overview_page.get_total_amount()
        print(f"Итоговая сумма: ${total}")
        assert total == expected_total, f"Ожидалась сумма ${expected_total}, но получено ${total}"

    # перечень товаров
    def test_all_items_cost_are_correct(self):
        items = [
            "Sauce Labs Backpack",
            "Sauce Labs Onesie",
            "Sauce Labs Bolt T-Shirt"
        ]

        self.open_and_login()
        self.add_items_to_cart(items)
        self.go_to_checkout()
        self.fill_checkout_info()
        self.assert_total_sum("58.29")


        # items_cost_from_inventory = {
        #     "Sauce Labs Backpack": self.inventory_page.get_item_price("Sauce Labs Backpack"),
        #     "Sauce Labs Onesie": self.inventory_page.get_item_price("Sauce Labs Onesie"),
        #     "Sauce Labs Bolt T-Shirt": self.inventory_page.get_item_price("Sauce Labs Bolt T-Shirt"),
        # }
        #
        # # 4. Вывод цен в консоль
        # for name, price in items_cost_from_inventory.items():
        #     print(f"Цена товара: {name} — {price}")
        #
        # # 5. Добавление товаров в корзину
        # self.inventory_page.add_item_to_cart("Sauce Labs Backpack")
        # self.inventory_page.add_item_to_cart("Sauce Labs Onesie")
        # self.inventory_page.add_item_to_cart("Sauce Labs Bolt T-Shirt")
        #
        # # 6. Переход в корзину
        # self.inventory_page.go_to_cart()
        #
        # # 7. Запоминание цен товаров в корзине
        # items_cost_from_cart = self.cart_page.get_items_prices_dict()
        #
        # # 8. Проверка, что цены в корзине соответствуют ценам на странице Inventory
        # assert items_cost_from_inventory == items_cost_from_cart, \
        #     "Цены в корзине не совпадают с ценами на странице Inventory."