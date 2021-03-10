# import libraries and modules
import psycopg2
from dotenv import load_dotenv 
import os

# load environmental variables required for connection
load_dotenv()
database_pw = os.environ["DATABASE_PASSWORD"]
print(database_pw)


def create_db(user='postgres', host='localhost', port='5432', database='health_tracker', password='postgres'):
    '''
    Create database names "health_tracker" if this does not already exist.
    '''

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
            print(f"Database named '{database}' created.")
        else:
            print(f"Database with name {database} already exists.")

        connection.close()
        print('Done')

def create_table(query, table_name, user='postgres', host='localhost', port='5432', database='health_tracker', password='postgres'):

    # connect to db or create db if it does not exist
    try:
        connection = psycopg2.connect(f"user={user} host={host} dbname={database} password={password} port={port}")
        print(f'Connected to database named {database}.')
    except:
        create_db()
        connection = psycopg2.connect(f"user={user} host={host} dbname={database} password={password} port={port}")

    # enable autocommit
    connection.autocommit = True

    # create cursor, run query, commit and close connection
    cur = connection.cursor()

    cur.execute(query)
    print(f"Created table named {table_name} in database named 'health_tracker'")

    connection.commit()
    connection.close()

queries = {
    # queries to create tables - only if they don't exist yet
    'user' : f"""CREATE TABLE IF NOT EXISTS users (
        user_id serial PRIMARY KEY,
        username VARCHAR ( 50 ) UNIQUE NOT NULL,
        password VARCHAR ( 50 ) NOT NULL,
        created_on TIMESTAMP NOT NULL default CURRENT_TIMESTAMP
        );""",

    'mood' : f"""CREATE TABLE IF NOT EXISTS mood (
        entry_id serial PRIMARY KEY,
        angry BOOLEAN NOT NULL,
        anxious BOOLEAN NOT NULL,
        calm BOOLEAN NOT NULL,
        content BOOLEAN NOT NULL,
        depressed BOOLEAN NOT NULL,
        emotional BOOLEAN NOT NULL,
        energetic BOOLEAN NOT NULL,
        excited BOOLEAN NOT NULL,
        frustrated BOOLEAN NOT NULL,
        happy BOOLEAN NOT NULL,
        hyper BOOLEAN NOT NULL,
        moody BOOLEAN NOT NULL,
        motivated BOOLEAN NOT NULL,
        relaxed BOOLEAN NOT NULL,
        sad BOOLEAN NOT NULL,
        sensitive BOOLEAN NOT NULL,
        stressed BOOLEAN NOT NULL,
        tired BOOLEAN NOT NULL,
        date TIMESTAMP NOT NULL,
        user_id INT,
        FOREIGN KEY (user_id) REFERENCES users ON DELETE CASCADE
        );""",

    'health' : f"""CREATE TABLE IF NOT EXISTS health (
        entry_id serial PRIMARY KEY,
        acidity BOOLEAN NOT NULL,
        backpain BOOLEAN NOT NULL,
        bloating BOOLEAN NOT NULL,
        breakouts BOOLEAN NOT NULL,
        chestpain BOOLEAN NOT NULL,
        constipation BOOLEAN NOT NULL,
        defecation BOOLEAN NOT NULL,
        diarrhea BOOLEAN NOT NULL,
        dizziness BOOLEAN NOT NULL,
        hard_stool BOOLEAN NOT NULL,
        headache BOOLEAN NOT NULL,
        indigestion BOOLEAN NOT NULL,
        medication TEXT,
        nausea BOOLEAN NOT NULL,
        numbness TEXT,
        other_symptoms TEXT,
        palpitations BOOLEAN NOT NULL,
        panic_attack BOOLEAN NOT NULL,
        breathlessness BOOLEAN NOT NULL,
        sick TEXT,
        stomachpain BOOLEAN NOT NULL,
        date TIMESTAMP NOT NULL,
        user_id INT,
        FOREIGN KEY (user_id) REFERENCES users ON DELETE CASCADE
        );""",

    'food' : f"""CREATE TABLE IF NOT EXISTS food (
        entry_id serial PRIMARY KEY,
        animal_products TEXT,
        cereal TEXT,
        unhealthy_food TEXT,
        enough_water BOOLEAN NOT NULL,
        fruits TEXT,
        healthy BOOLEAN NOT NULL,
        laxatives TEXT,
        supplements TEXT,
        date TIMESTAMP NOT NULL,
        user_id INT,
        FOREIGN KEY (user_id) REFERENCES users ON DELETE CASCADE
        );"""
}
    
create_db(password=database_pw)

for name, query in queries.items():
    create_table(query, name, password=database_pw)