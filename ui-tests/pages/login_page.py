from pages.base_page import BasePage, data_test
from pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    def open(self):
        self.driver.get(self.base_url + "/")
        self.visible(data_test("login-button"))
        return self

    def submit(self, username, password):
        self.fill(data_test("username"), username)
        self.fill(data_test("password"), password)
        self.click(data_test("login-button"))
        return self

    def login(self, username="standard_user", password="secret_sauce"):
        self.submit(username, password)
        page = InventoryPage(self.driver, self.base_url)
        page.visible(data_test("inventory-list"))
        return page

    @property
    def is_displayed(self):
        return self.visible(data_test("login-button")).is_displayed()
