import psycopg2
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, Page
import time

BASE_URL = "https://www.reddit.com/r/"
SUBREDDIT_NAME = "midjourney/new"
LOGIN_URL = "https://www.reddit.com/login"
USERNAME = "gwynbleiddww"
PASSWORD = "Anotherreddit6547."

class RedditCrawler:

    def connect_to_database(self):
        connection = psycopg2.connect(
            host="127.0.0.1",
            database="postgres",
            user="hasan",
            password="123123"
        )
        return connection

    def save_post_to_database(self, connection, title, author, post):
        cursor = connection.cursor()

        query = "INSERT INTO posts (title, author, post) VALUES (%s, %s, %s)"
        values = (title, author, post)

        cursor.execute(query, values)
        connection.commit()

        cursor.close()

    def login(self, page: Page):
        page.goto(f"{LOGIN_URL}", wait_until="load")

        page.fill('input[name="username"]', USERNAME)
        page.fill('input[name="password"]', PASSWORD)
        page.click('button[type="submit"]')

        return page

    def crawl(self, content: str):
        soup = BeautifulSoup(content, 'html.parser')

        connection = self.connect_to_database()

        titles = soup.findAll("h3")
        authors = soup.findAll(attrs={"data-testid": "post_author_link"})
        posts = soup.findAll(attrs={"data-click-id": "media"})

        for title, author, post in zip(titles, authors, posts):
            print(f"author: ", author.text)
            print(f"title: ", title.text)
            print(f"post: ", post.text, "\n")
            # print("--------------------------------------------------------------------")
            self.save_post_to_database(connection, title.text, author.text, post.text)

    def run(self):
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=False, slow_mo=3000)
            page = browser.new_page()

            self.login(page)

            page.goto(f"{BASE_URL}{SUBREDDIT_NAME}", wait_until="load")

            self.crawl(page.content())

RedditCrawler().run()