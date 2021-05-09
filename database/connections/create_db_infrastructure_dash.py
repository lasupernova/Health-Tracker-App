## DB for use with dashboard - columns added --> later: modify tkinter app to also work with this db

# import libraries and modules
import psycopg2
from dotenv import load_dotenv 
import os

# load environmental variables required for connection
load_dotenv()
database_pw = os.environ["DATABASE_PASSWORD"]
print(database_pw)

db = 'health_tracker2'

def create_db(user='postgres', host='localhost', port='5432', database=db, password='postgres'):
    '''
    Create database names "health_tracker2" if this does not already exist.
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

def create_table(query, table_name, user='postgres', host='localhost', port='5432', database=db, password='postgres'):

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
    print(f"Created table named {table_name} in database named {db}")

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
        sex smallint,
        dob date,
        created_on TIMESTAMP NOT NULL default CURRENT_TIMESTAMP
        );""",

    'mood' : f"""CREATE TABLE IF NOT EXISTS mood (
        date TIMESTAMP NOT NULL,
        user_id INT NOT NULL,
        angry BOOLEAN NOT NULL DEFAULT '0',
        anxious BOOLEAN NOT NULL DEFAULT '0',
        calm BOOLEAN NOT NULL DEFAULT '0',
        content BOOLEAN NOT NULL DEFAULT '0',
        depressed BOOLEAN NOT NULL DEFAULT '0',
        emotional BOOLEAN NOT NULL DEFAULT '0',
        energetic BOOLEAN NOT NULL DEFAULT '0',
        excited BOOLEAN NOT NULL DEFAULT '0',
        frustrated BOOLEAN NOT NULL DEFAULT '0',
        happy BOOLEAN NOT NULL DEFAULT '0',
        hyper BOOLEAN NOT NULL DEFAULT '0',
        moody BOOLEAN NOT NULL DEFAULT '0',
        motivated BOOLEAN NOT NULL DEFAULT '0',
        relaxed BOOLEAN NOT NULL DEFAULT '0',
        sad BOOLEAN NOT NULL DEFAULT '0',
        sensitive BOOLEAN NOT NULL DEFAULT '0',
        stressed BOOLEAN NOT NULL DEFAULT '0',
        tired BOOLEAN NOT NULL DEFAULT '0',
        PRIMARY KEY (user_id, date),
        FOREIGN KEY (user_id) REFERENCES users ON DELETE CASCADE
        );""",

    'health' : f"""CREATE TABLE IF NOT EXISTS health (
        date TIMESTAMP NOT NULL,
        user_id INT NOT NULL,
        acidity BOOLEAN NOT NULL DEFAULT '0',
        backpain BOOLEAN NOT NULL DEFAULT '0',
        bloating BOOLEAN NOT NULL DEFAULT '0',
        breakouts BOOLEAN NOT NULL DEFAULT '0',
        chestpain BOOLEAN NOT NULL DEFAULT '0',
        constipation BOOLEAN NOT NULL DEFAULT '0',
        defecation BOOLEAN NOT NULL DEFAULT '0',
        diarrhea BOOLEAN NOT NULL DEFAULT '0',
        dizziness BOOLEAN NOT NULL DEFAULT '0',
        hard_stool BOOLEAN NOT NULL DEFAULT '0',
        headache BOOLEAN NOT NULL DEFAULT '0',
        indigestion BOOLEAN NOT NULL DEFAULT '0',
        medication BOOLEAN NOT NULL DEFAULT '0',
        medication_type TEXT,
        nausea BOOLEAN NOT NULL DEFAULT '0',
        numbness BOOLEAN NOT NULL DEFAULT '0',
        numbness_location TEXT,
        other BOOLEAN NOT NULL DEFAULT '0',
        other_symptoms TEXT,
        palpitations BOOLEAN NOT NULL DEFAULT '0',
        panic_attack BOOLEAN NOT NULL DEFAULT '0',
        breathless BOOLEAN NOT NULL DEFAULT '0',
        RHR INT,
        sick BOOLEAN NOT NULL DEFAULT '0',
        sick_type TEXT,
        stomachpain BOOLEAN NOT NULL DEFAULT '0',
        PRIMARY KEY (user_id, date),
        FOREIGN KEY (user_id) REFERENCES users ON DELETE CASCADE
        );""",

    'food' : f"""CREATE TABLE IF NOT EXISTS food (
        date TIMESTAMP NOT NULL,
        user_id INT NOT NULL,
        animal_products BOOLEAN NOT NULL DEFAULT '0',
        animal_products_types TEXT,
        cereal BOOLEAN NOT NULL DEFAULT '0',
        cereal_types TEXT,
        unhealthy_food BOOLEAN NOT NULL DEFAULT '0',
        unhealthy_food_types TEXT,
        enough_water BOOLEAN NOT NULL DEFAULT '0',
        fruits BOOLEAN NOT NULL DEFAULT '0',
        fruits_types TEXT,
        healthy BOOLEAN NOT NULL DEFAULT '0',
        laxatives BOOLEAN NOT NULL DEFAULT '0',
        laxatives_types TEXT,
        supplements BOOLEAN NOT NULL DEFAULT '0',
        supplements_types TEXT,
        PRIMARY KEY (user_id, date),
        FOREIGN KEY (user_id) REFERENCES users ON DELETE CASCADE
        );""",

    'fitness' : f"""CREATE TABLE IF NOT EXISTS fitness (
        date TIMESTAMP NOT NULL,
        user_id INT NOT NULL,
        cycling BOOLEAN NOT NULL DEFAULT '0',
        cycling_time INT,
        gym BOOLEAN NOT NULL DEFAULT '0',
        gym_time INT,
        cardio BOOLEAN NOT NULL DEFAULT '0',
        cardio_time INT,
        stretching BOOLEAN NOT NULL DEFAULT '0',
        stretching_time INT,
        yoga BOOLEAN NOT NULL DEFAULT '0',
        yoga_time INT,
        other BOOLEAN NOT NULL DEFAULT '0',
        other_time INT,
        PRIMARY KEY (user_id, date),
        CONSTRAINT cycling_check CHECK
            ((cycling IS NULL AND cycling_time IS NULL)
            OR(cycling = False AND cycling_time = 0)
            OR(cycling = True AND cycling_time > 0)),
        CONSTRAINT gym_check CHECK
            ((gym IS NULL AND gym_time IS NULL)
            OR(gym = False AND gym_time = 0)
            OR(gym = True AND gym_time > 0)),
        CONSTRAINT cardio_check CHECK
            ((cardio IS NULL AND cardio_time IS NULL)
            OR(cardio = False AND cardio_time = 0)
            OR(cardio = True AND cardio_time > 0)),
        CONSTRAINT stretch_check CHECK
            ((stretching IS NULL AND stretching_time IS NULL)
            OR(stretching = False AND stretching_time = 0)
            OR(stretching = True AND stretching_time > 0)),
        CONSTRAINT yoga_check CHECK
            ((yoga IS NULL AND yoga_time IS NULL)
            OR(yoga = False AND yoga_time = 0)
            OR(yoga = True AND yoga_time > 0)),
        CONSTRAINT other_check CHECK
            ((other IS NULL AND other_time IS NULL)
            OR(other = False AND other_time = 0)
            OR(other = True AND other_time > 0)),
        FOREIGN KEY (user_id) REFERENCES users ON DELETE CASCADE
        );""",

    'period' : f"""CREATE TABLE IF NOT EXISTS period (
        date TIMESTAMP NOT NULL,
        user_id INT NOT NULL,
        cramps BOOLEAN NOT NULL DEFAULT '0',
        cramps_level INT CHECK ((cramps_level > 0) AND (cramps_level <5) OR NULL),
        cycle_day INT NOT NULL,
        infection BOOLEAN NOT NULL DEFAULT '0',
        infection_type TEXT,
        ovulation BOOLEAN NOT NULL DEFAULT '0',
        period BOOLEAN NOT NULL DEFAULT '0',
        intercourse BOOLEAN NOT NULL DEFAULT '0',
        spotting BOOLEAN NOT NULL DEFAULT '0',
        spotting_level INT CHECK ((spotting_level > 0) AND (spotting_level <3) OR NULL),
        PRIMARY KEY (user_id, date),
        FOREIGN KEY (user_id) REFERENCES users ON DELETE CASCADE
        );""",

    'longterm' : f"""CREATE TABLE IF NOT EXISTS longterm (
        date TIMESTAMP NOT NULL,
        user_id INT NOT NULL,
        anatomical TEXT,
        climate TEXT,
        hormonal TEXT,
        nutritional TEXT,
        social TEXT,
        PRIMARY KEY (user_id, date),
        FOREIGN KEY (user_id) REFERENCES users ON DELETE CASCADE
        );""",

    'sleep' : f"""CREATE TABLE IF NOT EXISTS sleep (
        date TIMESTAMP NOT NULL,
        user_id INT NOT NULL,
        sleep REAL CHECK ((sleep > 0.0) AND (sleep < 24.0) OR NULL),
        REM REAL CHECK ((REM > 0.0) AND (REM < 1.0) OR NULL),
        awake REAL CHECK ((awake > 0.0) AND (awake < 1.0) OR NULL),
        deep_sleep REAL CHECK ((deep_sleep > 0.0) AND (deep_sleep < 1.0) OR NULL),
        light_sleep REAL CHECK ((light_sleep > 0.0) AND (light_sleep < 1.0) OR NULL),
        sleep_score INT CHECK ((sleep_score > 0) AND (sleep_score < 100) OR NULL),
        insomnia BOOLEAN NOT NULL DEFAULT '0',
        freq_wakes BOOLEAN NOT NULL DEFAULT '0',
        sleep_meds BOOLEAN NOT NULL DEFAULT '0',
        sleep_meds_types TEXT,
        tz_change BOOLEAN NOT NULL DEFAULT '0',
        PRIMARY KEY (user_id, date),
        FOREIGN KEY (user_id) REFERENCES users ON DELETE CASCADE
        );"""
}
    
create_db(password=database_pw)

for name, query in queries.items():
    create_table(query, name, password=database_pw)