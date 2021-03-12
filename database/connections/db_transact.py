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
    connection.close() #TO DO: modify code to use "with connection:" instead


