import pytest

pytestmark = pytest.mark.regression


@pytest.mark.smoke
def test_valid_login(login_page):
    inventory = login_page.login()
    assert inventory.title == "Products"
    assert len(inventory.names) == 6
    assert inventory.cart_count == 0


@pytest.mark.parametrize(
    "username,password,message",
    [
        pytest.param(
            "standard_user",
            "wrong-password",
            "Username and password do not match",
            id="wrong-password",
        ),
        pytest.param(
            "unknown_user", "secret_sauce", "Username and password do not match", id="unknown-user"
        ),
        pytest.param(
            "locked_out_user",
            "secret_sauce",
            "Sorry, this user has been locked out",
            id="locked-account",
        ),
        pytest.param("", "secret_sauce", "Username is required", id="missing-username"),
        pytest.param("standard_user", "", "Password is required", id="missing-password"),
    ],
)
def test_rejected_login(login_page, username, password, message):
    login_page.submit(username, password)
    assert message in login_page.error
    assert login_page.is_displayed
    assert "/inventory.html" not in login_page.driver.current_url


def test_logout_blocks_protected_page(inventory):
    login_page = inventory.logout()
    assert login_page.is_displayed
    inventory.driver.get(inventory.base_url + "/inventory.html")
    assert login_page.is_displayed
    assert "You can only access '/inventory.html' when you are logged in" in login_page.error
