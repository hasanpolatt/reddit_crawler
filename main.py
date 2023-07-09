from playwright.sync_api import sync_playwright, Page
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.reddit.com/r/"
SUBREDDIT_NAME = "midjourney/new"
LOGIN_URL = "https://www.reddit.com/login"
USERNAME = "gwynbleiddww"
PASSWORD = "Hasan134679258."

def login_to_reddit(page: Page) -> Page:
    page.goto(f"{LOGIN_URL}")

    page.fill('input[name="username"]', USERNAME)
    page.fill('input[name="password"]', PASSWORD)
    page.click('button[type="submit"]')

    return page

def crawl_subreddit():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()

        login_to_reddit(page)

        page.goto(f"{BASE_URL}{SUBREDDIT_NAME}")
        content = page.content()

        soup = BeautifulSoup(content, 'html.parser')

        titles = soup.findAll("h3")
        authors = soup.findAll(attrs={"data-testid": "post_author_link"})
        posts = soup.findAll(attrs={"data-click-id": "media"})

        while True:
            for title, author, post in zip(titles, authors, posts):
                print(f"author: ", author.text)
                print(f"title: ", title.text)
                print(f"post: ", post.text)

            time.sleep(4)
            page.reload()

        browser.close()

crawl_subreddit()
