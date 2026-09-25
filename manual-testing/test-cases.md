# Manual and automated test cases

Target: Sauce Demo. Start each case in a fresh browser session. Valid account: `standard_user` / `secret_sauce`. Unless testing login itself, sign in before executing the steps. Product assumptions: Backpack = $29.99, Bike Light = $9.99. All customer details are fictional.

The cases below are designed and automated. **Manual execution status: not run.** See [validation](../docs/validation.md) for automated execution evidence; do not treat the table as a manual test result.

| ID | Priority | Steps / data | Expected result | Automated test |
| --- | --- | --- | --- | --- |
| AUTH-01 | P0 | Sign in with valid account | Products page, 6 products, empty cart | `test_valid_login` |
| AUTH-02 | P1 | Valid username, wrong password | Credential error; remain on login | `test_rejected_login[wrong-password]` |
| AUTH-03 | P1 | Unknown username, demo password | Credential error; remain on login | `test_rejected_login[unknown-user]` |
| AUTH-04 | P1 | `locked_out_user`, demo password | Locked-account error; remain on login | `test_rejected_login[locked-account]` |
| AUTH-05 | P1 | Empty username, demo password | Username-required error | `test_rejected_login[missing-username]` |
| AUTH-06 | P1 | Valid username, empty password | Password-required error | `test_rejected_login[missing-password]` |
| AUTH-07 | P1 | Log out, then visit `/inventory.html` | Login page and protected-page error | `test_logout_blocks_protected_page` |
| SORT-01 | P2 | Select Name A to Z | All original product names in ascending order | `test_product_sorting[name-ascending]` |
| SORT-02 | P2 | Select Name Z to A | All original product names in descending order | `test_product_sorting[name-descending]` |
| SORT-03 | P2 | Select Price low to high | All original prices in ascending order | `test_product_sorting[price-ascending]` |
| SORT-04 | P2 | Select Price high to low | All original prices in descending order | `test_product_sorting[price-descending]` |
| CART-01 | P0 | Add Backpack + Bike Light; open cart; remove Backpack | Exact names/prices, quantity 1 each; badge 2 → 1; Bike Light remains | `test_cart_preserves_selected_products` |
| CART-02 | P1 | Add then remove Backpack from inventory; open cart | Badge absent; cart empty | `test_remove_last_product_clears_cart` |
| CART-03 | P1 | Add Bike Light; open cart; refresh | Same item and quantity remain; badge 1 | `test_cart_survives_refresh` |
| BUY-01 | P0 | Add both products; checkout with Alex / Tester / 5000; finish | Exact items; subtotal 39.98, tax 3.20, total 43.18; confirmation; cart empty | `test_complete_purchase` |
| BUY-02 | P1 | Checkout both products with empty first name | First-name-required error; cart retained | `test_customer_fields_are_required[missing-first-name]` |
| BUY-03 | P1 | Checkout both products with empty last name | Last-name-required error; cart retained | `test_customer_fields_are_required[missing-last-name]` |
| BUY-04 | P1 | Checkout both products with empty postal code | Postal-code-required error; cart retained | `test_customer_fields_are_required[missing-postal-code]` |
| BUY-05 | P1 | Complete customer details, then cancel overview | Products page; both items remain in cart | `test_cancel_overview_preserves_cart` |

## Exploratory charter (not automated)

Timebox 20 minutes to keyboard navigation, focus visibility, product details, back navigation, and error recovery. Record observations before deciding whether behavior is a defect. Product behavior alone does not establish a requirement. Use the [defect template](bug-report-template.md) for reproducible findings.
