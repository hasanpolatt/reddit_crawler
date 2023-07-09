from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.reddit.com/r/"
SUBREDDIT_NAME = "midjourney/new"

def crawl_subreddit():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(f"{BASE_URL}{SUBREDDIT_NAME}")
        content = page.content()

        soup = BeautifulSoup(content, 'html.parser')

        titles = soup.findAll("h3")
        authors = soup.findAll(attrs={"data-testid": "post_author_link"})
        posts = soup.findAll(attrs={"data-click-id": "text"})

        while True:
            for title, author, post in zip(titles, authors, posts):
                print(f"author: ", author.text.encode('utf-8').decode('utf-8'), flush=True)
                print(f"title: ",title.text.encode('utf-8').decode('utf-8'), flush=True)
                print("post: ", post.text.encode('utf-8').decode('utf-8'), flush=True)

            time.sleep(5)
            page.reload()

        browser.close()

crawl_subreddit()