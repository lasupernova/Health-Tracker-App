# import libraries and modules
import psycopg2
from dotenv import load_dotenv 
import os

# load environmental variables required for connection
load_dotenv()
database_pw = os.environ["DATABASE_PASSWORD"]
print(database_pw)

s = ""
s += "SELECT"
s += " table_schema"
s += ", table_name"
s += " FROM information_schema.tables"
# s += " WHERE"
# s += " ("
# s += " table_schema = 'public'"
# s += " )"
s += " ORDER BY table_schema, table_name;"


def create_db(user='postgres', host='localhost', port='5432', database='health_tracker', password='postgres'):

    connection = None

    # connect to server
    try:
        connection = psycopg2.connect(f"user={user} host={host} password={password} port={port}")
        print(f'Connected to database named {database}.')

    except:
        print('Database not connected.')

    # create database if it does not yet exist
    if connection is not None:
        connection.autocommit = True

        # postgreSQL does not have an 'IF NOT EXISTS' statement for 'CREATE DATABASE <db_name>'
        cur = connection.cursor()

        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{database}';")

        exists = cur.fetchone()

        if not exists:
            cur.execute(f'CREATE DATABASE {database}')
        else:
            print(f"Database with name {database} already exists.")

        connection.close()
        print('Done')

def connect_db(user='postgres', host='localhost', port='5432', database='health_tracker', password='postgres'):
    return psycopg2.connect(f"user={user} host={host} dbname={database} password={password} port={port}")

def create_table(table_name, user='postgres', host='localhost', port='5432', database='health_tracker', password='postgres'):

    # connect to db or create db if it does not exist
    try:
        connection = psycopg2.connect(f"user={user} host={host} dbname={database} password={password} port={port}")
        print(f'Connected to database named {database}.')
    except:
        create_db()
        connection = psycopg2.connect(f"user={user} host={host} dbname={database} password={password} port={port}")

    # query to create table only if it doesn't exist yet
    query = f"""CREATE TABLE IF NOT EXISTS {table_name} (
        user_id serial PRIMARY KEY,
        username VARCHAR ( 50 ) UNIQUE NOT NULL,
        password VARCHAR ( 50 ) NOT NULL,
        created_on TIMESTAMPTZ NOT NULL default CURRENT_TIMESTAMP
        );"""

    # create cursor, run query, commit and close connection
    cur = connection.cursor()
    cur.execute(query)
    print(f"Created table named {table_name} in database named 'health_tracker'")
    connection.commit()
    connection.close()

def add_user(user, password):
    connection = connect_db(password=database_pw)
    cur = connection.cursor()
    query = f"""INSERT INTO users (username, password) VALUES (%s, %s);"""
    cur.execute(query, (user, password))
    connection.commit()    
    print("New user signed up!")
    print(f"\t username: {user}; password: {password}")


# add_user('tester','pw123')


# connection = psycopg2.connect(f"user='postgres' host='localhost' dbname='health_tracker' password={database_pw} port='5432'")
# print('\n\nHealth Tracker connected.')

# cur = connection.cursor()

# cur.execute("""SELECT table_name FROM information_schema.tables
#        WHERE table_schema = 'public'""")

# if cur.fetchall():
#     for table in cur.fetchall():
#         print(table)
# else:
#     print('No tables in database yet')
#     create_user_table = """CREATE TABLE IF NOT EXISTS user_table (
#                                         username varchar(80) NOT NULL,
#                                         password varchar(450) NOT NULL,
#                                         PRIMARY KEY (username)
#                                     );"""
#     cur.execute(create_user_table)
#     connection.commit()
#     print("""Table names 'user_table' created.
#             This table stores username and password.""")
# connection.close()
