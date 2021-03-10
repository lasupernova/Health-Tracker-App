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


def connect_db(user='postgres', host='localhost', port='5432', database='health_tracker', password='postgres'):
    return psycopg2.connect(f"user={user} host={host} dbname={database} password={password} port={port}")

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
