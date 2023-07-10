import psycopg2
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, Page
import time
from database import DatabaseOperations

BASE_URL = "https://www.reddit.com/r/"
SUBREDDIT_NAME = "midjourney/new"
LOGIN_URL = "https://www.reddit.com/login"
USERNAME = "username"
PASSWORD = "password"

class RedditCrawler:
    def login(self, page: Page):
        page.goto(f"{LOGIN_URL}", wait_until="load")

        page.fill('input[name="username"]', USERNAME)
        page.fill('input[name="password"]', PASSWORD)
        page.click('button[type="submit"]')

        return page

    def crawl(self, content: str, database: DatabaseOperations):
        soup = BeautifulSoup(content, 'html.parser')

        database.create_table()

        titles = soup.findAll("h3")
        authors = soup.findAll(attrs={"data-testid": "post_author_link"})
        posts = soup.findAll(attrs={"data-click-id": "media"})

        for title, author, post in zip(titles, authors, posts):
            print(f"author: ", author.text)
            print(f"title: ", title.text)
            print(f"post: ", post.text, "\n")
            database.save_post_to_database(title.text, author.text, post.text)

if __name__ == "__main__":
    database = DatabaseOperations()
    database.create_table()

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False, slow_mo=3000)
        page = browser.new_page()

        reddit_crawler = RedditCrawler()
        reddit_crawler.login(page)

        page.goto(f"{BASE_URL}{SUBREDDIT_NAME}", wait_until="load")

        reddit_crawler.crawl(page.content(), database)

# RedditCrawler().run()