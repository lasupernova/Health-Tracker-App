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
        connection.commit()

        exists = cur.fetchone()

        if not exists:
            cur.execute(f'CREATE DATABASE {database}')
            cur.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto;')
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

# table names and queries to pass to cur.execute()
# NOTE: the key (=tablename) is not essential for creating the tables, they are only used for the print statement
queries = {
    # queries to create tables - only if they don't exist yet
    'user' : f"""CREATE TABLE IF NOT EXISTS users (
        user_id serial PRIMARY KEY,
        username VARCHAR ( 50 ) UNIQUE NOT NULL,
        password text NOT NULL,
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
        );""",

    'fitness' : f"""CREATE TABLE IF NOT EXISTS fitness (
        entry_id serial PRIMARY KEY,
        cycling BOOLEAN NOT NULL,
        cycling_time INT CHECK (cycling_time > 0),
        gym BOOLEAN NOT NULL,
        gym_time INT CHECK (gym_time > 0),
        cardio BOOLEAN NOT NULL,
        cardio_time INT CHECK (cardio_time > 0),
        stretching BOOLEAN NOT NULL,
        stretching_time INT CHECK (stretching_time > 0),
        yoga BOOLEAN NOT NULL,
        yoga_time INT CHECK (yoga_time > 0),
        other BOOLEAN NOT NULL,
        other_time INT CHECK (other_time > 0),
        user_id INT,
        FOREIGN KEY (user_id) REFERENCES users ON DELETE CASCADE
        );""",

    'period' : f"""CREATE TABLE IF NOT EXISTS period (
        entry_id serial PRIMARY KEY,
        cramps BOOLEAN NOT NULL,
        cramps_level INT CHECK ((cramps_level > 0) AND (cramps_level <5)),
        cycle_day INT NOT NULL,
        infection TEXT,
        ovulation BOOLEAN NOT NULL,
        period BOOLEAN NOT NULL,
        intercourse BOOLEAN NOT NULL,
        spotting BOOLEAN NOT NULL,
        spotting_level INT CHECK ((spotting_level > 0) AND (spotting_level <4)),
        user_id INT,
        FOREIGN KEY (user_id) REFERENCES users ON DELETE CASCADE
        );""",

    'longterm' : f"""CREATE TABLE IF NOT EXISTS longterm (
        entry_id serial PRIMARY KEY,
        anatomical TEXT,
        climate TEXT,
        hormonal TEXT,
        nutritional TEXT,
        social TEXT,
        user_id INT,
        FOREIGN KEY (user_id) REFERENCES users ON DELETE CASCADE
        );""",

    'sleep' : f"""CREATE TABLE IF NOT EXISTS sleep (
        entry_id serial PRIMARY KEY,
        sleep INT CHECK ((sleep > 0) AND (sleep < 24)),
        REM REAL CHECK ((REM > 0.0) AND (REM < 1.0)),
        awake REAL CHECK ((awake > 0.0) AND (awake < 1.0)),
        deep_sleep REAL CHECK ((deep_sleep > 0.0) AND (deep_sleep < 1.0)),
        light_sleep REAL CHECK ((light_sleep > 0.0) AND (light_sleep < 1.0)),
        sleep_score INT CHECK ((sleep_score > 0) AND (sleep_score < 100)),
        insomnia BOOLEAN NOT NULL,
        freq_wakes BOOLEAN NOT NULL,
        sleep_meds TEXT,
        tz_change BOOLEAN NOT NULL DEFAULT '0',
        user_id INT,
        FOREIGN KEY (user_id) REFERENCES users ON DELETE CASCADE
        );"""
}
    
create_db(password=database_pw)

for name, query in queries.items():
    create_table(query, name, password=database_pw)