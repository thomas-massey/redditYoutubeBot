import os
import sqlite3

database_location = "/home/thomas/redditYoutubeBot/database/database.db"

def check_if_database_exists():
    """
    Checks if the database exists.
    """
    if os.path.isfile(database_location):
        return True
    else:
        create_database()

def create_database():
    """
    Creates the database.
    """
    if not os.path.exists("/home/thomas/redditYoutubeBot/database"):
        os.system("mkdir /home/thomas/redditYoutubeBot/database")
    conn = sqlite3.connect(database_location)
    c = conn.cursor()
    c.execute("CREATE TABLE posts (id text)")
    conn.commit()
    conn.close()

def add_post(id):
    check_if_database_exists()
    """
    Adds a post to the database.
    """
    conn = sqlite3.connect(database_location)
    c = conn.cursor()
    c.execute("INSERT INTO posts VALUES (?)", (id,))
    conn.commit()
    conn.close()

def check_if_post_exists(id):
    check_if_database_exists()
    """
    Checks if a post exists in the database.
    """
    conn = sqlite3.connect(database_location)
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id=?", (id,))
    if c.fetchone():
        return True
    else:
        return False