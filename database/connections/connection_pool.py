from psycopg2.pool import SimpleConnectionPool
import os
from dotenv import load_dotenv 
from contextlib import contextmanager

# prompt message 
DATABASE_PROMPT = "Enter a DATABASE_URI value or leave empty to load from .env file: "

# prompt user for custom database URI
database_uri = input(DATABASE_PROMPT)

# if no custom URI was passed:
if not database_uri:
    load_dotenv() #load URI info from .env-file
    database_uri = os.environ["DATABASE_URL"]


# create data connection pool (here: i)
pool = SimpleConnectionPool(minconn=1,
                            maxconn=10,
                            dsn=database_uri)

# create a function into a contextmanager
@contextmanager
def get_connection():
    connection = pool.getconn()

    try:
        yield connection
    finally:
        pool.putconn(connection)