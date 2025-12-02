import pytest
from playwright.sync_api import sync_playwright
import random
import os

BASE_URL = "http://127.0.0.1:5000"

if os.environ.get("CI") == "true":
    pytest.skip("Skipping E2E tests in CI environment", allow_module_level=True)

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        yield browser
        browser.close()


def add_new_book(page, title, author, isbn, copies):
    page.goto(f"{BASE_URL}/add_book")

    page.fill("input[name='title']", title)
    page.fill("input[name='author']", author)
    page.fill("input[name='isbn']", isbn)
    page.fill("input[name='total_copies']", str(copies))

    page.click("button[type='submit']")

    page.wait_for_url("**/catalog")

    content = page.content()
    assert title in content
    assert author in content
    assert isbn in content

def verify_book(page, title):
    page.goto(f"{BASE_URL}/catalog")
    assert title in page.content()

def to_borrow_book_page(page):
    page.goto(f"{BASE_URL}/catalog")
    assert "Book Catalog" in page.content()

def borrow_book(page, book_id, patron_id):
    page.goto(f"{BASE_URL}/catalog")

    row_selector = f"tr:has(td:text('{book_id}'))"

    page.fill(f"{row_selector} input[name='patron_id']", patron_id)

    page.click(f"{row_selector} button.btn-success")

    page.wait_for_url("**/catalog")

def verify_confirmation(page):
    page.goto(f"{BASE_URL}/catalog")
    text = page.content().lower()
    assert "successfully borrowed" in text or "success" in text

def test_e2e(browser):
    page = browser.new_page()

    title = "Harry Potter"
    author = "JK Rowlings"
    isbn = str(1000000000000 + random.randint(1000, 9999))
    copies = 67


    add_new_book(page, title, author, isbn, copies)
    verify_book(page, title)
    to_borrow_book_page(page)

    page.goto(f"{BASE_URL}/catalog")
    row = page.locator(f"tr:has(td:text('{title}'))")
    book_id = row.locator("td").first.inner_text()

    borrow_book(page, book_id=book_id, patron_id="123456")

    verify_confirmation(page)