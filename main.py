from bs4 import BeautifulSoup
from playwright.sync_api import Page, sync_playwright

from database import DatabaseOperations

URL = "https://www.reddit.com/"
BASE_URL = "https://www.reddit.com/r/"
SUBREDDIT_NAME = "midjourney/new"
LOGIN_URL = "https://www.reddit.com/login"
USERNAME = "username"
PASSWORD = "password"

class RedditCrawler:

    def login(self, page: Page):
        # Navigate to the login page
        page.goto(f"{LOGIN_URL}", wait_until="load")

        # Fill in the username and password fields
        page.fill('input[name="username"]', USERNAME)
        page.fill('input[name="password"]', PASSWORD)

        # Click the submit button to log in
        page.click('button[type="submit"]')

        return page

    def crawl(self, content: str, database: DatabaseOperations):
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')

        # Find all the post titles, authors, and contents
        titles = soup.findAll("h3")
        authors = soup.findAll(attrs={"data-testid": "post_author_link"})
        posts = soup.findAll(attrs={"data-click-id": "media"})

        # Print the author, title, and post content
        for title, author, post in zip(titles, authors, posts):
            print(f"author: ", author.text)
            print(f"title: ", title.text)
            print(f"post: ", post.text, "\n")

            # Save the post information to the database
            database.save_post_to_database(title.text, author.text, post.text)

    def run(self):
        with sync_playwright() as pw:
            # Launch a new Chromium browser instance
            browser = pw.chromium.launch(headless=False, slow_mo=3000)
            page = browser.new_page()

            # Create a new instance of DatabaseOperations
            database = DatabaseOperations()

            # Create the necessary table in the database
            database.create_table()

            # Log in to Reddit
            self.login(page)

            # Navigate to the specified subreddit
            page.goto(f"{BASE_URL}{SUBREDDIT_NAME}", wait_until="load")

            # Crawl the page content and save the posts to the database
            self.crawl(page.content(), database)

RedditCrawler().run()