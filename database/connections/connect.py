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


connection = None
try:
    # In PostgreSQL, default username is 'postgres' and password is 'postgres'.
    # And also there is a default database exist named as 'postgres'.
    # Default host is 'localhost' or '127.0.0.1'
    # And default port is '54322'.
    connection = psycopg2.connect(f"user='postgres' host='localhost' database ='health_tracker' password={database_pw} port='5432'")
    print('Database connected.')

except:
    print('Database not connected.')

if connection is not None:
    connection.autocommit = True

    cur = connection.cursor()

    cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'health_tracker';")

    exists = cur.fetchone()
    if not exists:
        cur.execute('CREATE DATABASE health_tracker')
    else:
        print(f"Database with name {exists} already exists.")

    # list_database = cur.fetchall()
    # print(list_database)

    # database_name = input('Enter database name to check exist or not: ')

    # if (database_name,) in list_database:
    #     print("'{}' Database already exist".format(database_name))
    # else:
    #     print("'{}' Database not exist.".format(database_name))
    connection.close()
    print('Done')

connection = psycopg2.connect(f"user='postgres' host='localhost' dbname='health_tracker' password={database_pw} port='5432'")
print('\n\nHealth Tracker connected.')

cur = connection.cursor()

cur.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")

if cur.fetchall():
    for table in cur.fetchall():
        print(table)
else:
    print('No tables in database yet')
    create_user_table = """CREATE TABLE IF NOT EXISTS user_table (
                                        username varchar(80) NOT NULL,
                                        password varchar(450) NOT NULL,
                                        PRIMARY KEY (username)
                                    );"""
    cur.execute(create_user_table)
    connection.commit()
    print("""Table names 'user_table' created.
            This table stores username and password.""")
connection.close()
