import psycopg2

class DatabaseOperations:
    def __init__(self):
        self.connection = self.connect_to_database()

    def connect_to_database(self):
        connection = psycopg2.connect(
            host="127.0.0.1",
            database="postgres",
            user="hasan",
            password="123123"
        )
        return connection

    def create_table(self):
        cursor = self.connection.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            title TEXT,
            author TEXT,
            post TEXT
        );
        """

    def save_post_to_database(self, title, author, post):
        cursor = self.connection.cursor()

        query = "INSERT INTO posts (title, author, post) VALUES (%s, %s, %s)"
        values = (title, author, post)

        cursor.execute(query, values)
        self.connection.commit()

        cursor.close()