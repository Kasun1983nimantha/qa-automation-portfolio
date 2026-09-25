from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage, data_test, money


class InventoryPage(BasePage):
    @property
    def names(self):
        self.visible(data_test("inventory-list"))
        return [e.text for e in self.driver.find_elements(*data_test("inventory-item-name"))]

    @property
    def prices(self):
        self.visible(data_test("inventory-list"))
        return [
            money(e.text) for e in self.driver.find_elements(*data_test("inventory-item-price"))
        ]

    def sort(self, value):
        Select(self.visible(data_test("product-sort-container"))).select_by_value(value)
        self.wait.until(
            lambda _: (
                Select(
                    self.visible(data_test("product-sort-container"))
                ).first_selected_option.get_attribute("value")
                == value
            )
        )
        return self

    def add(self, product_slug):
        self.click(data_test(f"add-to-cart-{product_slug}"))
        self.visible(data_test(f"remove-{product_slug}"))
        return self

    def remove(self, product_slug):
        self.click(data_test(f"remove-{product_slug}"))
        self.visible(data_test(f"add-to-cart-{product_slug}"))
        return self

    def logout(self):
        from pages.login_page import LoginPage

        self.click((By.ID, "react-burger-menu-btn"))
        self.click(data_test("logout-sidebar-link"))
        page = LoginPage(self.driver, self.base_url)
        page.visible(data_test("login-button"))
        return page
