from pages.base_page import data_test, money
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage


class CheckoutPage(CartPage):
    def submit_customer(self, first_name, last_name, postal_code):
        self.fill(data_test("firstName"), first_name)
        self.fill(data_test("lastName"), last_name)
        self.fill(data_test("postalCode"), postal_code)
        self.click(data_test("continue"))
        return self

    @property
    def subtotal(self):
        return money(self.text(data_test("subtotal-label")))

    @property
    def tax(self):
        return money(self.text(data_test("tax-label")))

    @property
    def total(self):
        return money(self.text(data_test("total-label")))

    def finish(self):
        self.click(data_test("finish"))
        return self.text(data_test("complete-header"))

    def cancel_overview(self):
        self.click(data_test("cancel"))
        page = InventoryPage(self.driver, self.base_url)
        page.visible(data_test("inventory-list"))
        return page
