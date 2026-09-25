from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def data_test(value):
    return By.CSS_SELECTOR, f'[data-test="{value}"]'


def money(text):
    return Decimal(text.rsplit("$", 1)[-1])


class BasePage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, 10)

    def visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def fill(self, locator, value):
        element = self.visible(locator)
        element.clear()
        element.send_keys(value)

    def text(self, locator):
        return self.visible(locator).text

    @property
    def title(self):
        return self.text(data_test("title"))

    @property
    def error(self):
        return self.text(data_test("error"))

    @property
    def cart_count(self):
        badges = self.driver.find_elements(*data_test("shopping-cart-badge"))
        return int(badges[0].text) if badges else 0

    def open_cart(self):
        from pages.cart_page import CartPage

        self.click(data_test("shopping-cart-link"))
        page = CartPage(self.driver, self.base_url)
        page.visible(data_test("cart-list"))
        return page
