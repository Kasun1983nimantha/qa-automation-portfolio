from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage, data_test, money


class CartPage(BasePage):
    @property
    def items(self):
        self.visible(data_test("cart-list"))
        return [
            {
                "name": row.find_element(*data_test("inventory-item-name")).text,
                "price": money(row.find_element(*data_test("inventory-item-price")).text),
                "quantity": int(row.find_element(*data_test("item-quantity")).text),
            }
            for row in self.driver.find_elements(*data_test("inventory-item"))
        ]

    def remove(self, product_slug):
        locator = data_test(f"remove-{product_slug}")
        self.click(locator)
        self.wait.until(EC.invisibility_of_element_located(locator))
        return self

    def checkout(self):
        from pages.checkout_page import CheckoutPage

        self.click(data_test("checkout"))
        page = CheckoutPage(self.driver, self.base_url)
        page.visible(data_test("firstName"))
        return page
