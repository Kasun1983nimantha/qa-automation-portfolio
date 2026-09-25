# Test strategy

## Objective and target

Verify that a demo shopper can authenticate, choose products, manage a cart, and complete a simulated purchase. Target: https://www.saucedemo.com/. Credentials are published by the demo itself: `standard_user` / `secret_sauce`; `locked_out_user` is a negative test account. Customer information is fictional.

## Risk-based scope

The highest priority is the successful purchase path and correct selected items/totals. Three smoke tests cover successful login, cart selection/removal, and purchase completion. The full 19-case regression set also tests rejected access, four sort modes, empty cart state, refresh persistence, required customer fields, and checkout cancellation.

See [manual cases](../manual-testing/test-cases.md) for the full mapping. A green suite only supports these checks; it is not proof that the whole application is defect-free.

## Test design techniques

- **Equivalence partitions:** accepted user, unknown user, incorrect password, locked account; present and absent required customer fields.
- **State transitions:** logged out → logged in → logged out; empty → populated → reduced cart; cart → customer details → overview → confirmation.
- **Ordering oracle:** preserve the unsorted inventory and compare with an independently sorted expected list in each direction.
- **Monetary oracle:** known catalog prices of 29.99 and 9.99 produce a 39.98 subtotal, 3.20 demo tax, and 43.18 total. Verify both the fixed values and the sum.

No unsupported maximum-length or postal-format rules are invented. Boundary-value tests require a documented boundary; exploratory findings can inform later cases.

## Architecture decisions

Page classes own selectors and explicit waits. Tests own assertions, test data, and expected outcomes. A fresh driver per test costs startup time but avoids hidden dependencies from cookies, local storage, or an earlier failed checkout. Driver teardown is registered immediately after creation.

Prefer the application's `data-test` attributes over styling classes or absolute XPath. A small shared base class provides waits and common cart controls. Checkout reuses cart item reading because both pages expose the same item structure. Split that into a component if the structures diverge.

Chrome is the default local browser; CI exercises Chrome and Firefox separately. Headless mode is the default; `--headed` supports debugging. `--base-url` is for an equivalent demo deployment with the same contract, not arbitrary websites.

## Execution and exit criteria

1. Lint and formatting checks pass.
2. All 19 cases pass for each supported browser in CI.
3. Any failure is triaged using assertion output, screenshot, DOM, and environment context.
4. A UI/catalog change is evaluated against expected behavior before changing an assertion.

External site outages are environment failures, not automatic product defects. Re-run only after investigating. No hidden retries make an unstable run appear green.

## Evidence and data handling

HTML and JUnit reports are generated on request and by CI. Failure captures are best-effort: a browser startup failure cannot provide a screenshot, and a capture failure must preserve the original error. Reports are ignored locally and retained as CI artifacts for 14 days. This suite uses public demo data; if adapted to a private application, review and redact screenshots/DOM before uploading them.

## Out of scope

Real payments, real customer data, security penetration testing, backend correctness, accessibility conformance, load testing, visual pixel comparison, and physical mobile devices. API/Postman/SQL directories are reserved for future work.
