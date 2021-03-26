##to do: implement composite primary key for data tables (excl. users table) ?
## instead of adding PRIMARY key after each of these col;umns, append PRIMARY KEY (col1, col2), to the end of the statement instead

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
        angry BOOLEAN,
        anxious BOOLEAN,
        calm BOOLEAN,
        content BOOLEAN,
        depressed BOOLEAN,
        emotional BOOLEAN,
        energetic BOOLEAN,
        excited BOOLEAN,
        frustrated BOOLEAN,
        happy BOOLEAN,
        hyper BOOLEAN,
        moody BOOLEAN,
        motivated BOOLEAN,
        relaxed BOOLEAN,
        sad BOOLEAN,
        sensitive BOOLEAN,
        stressed BOOLEAN,
        tired BOOLEAN,
        date TIMESTAMP NOT NULL,
        user_id INT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users ON DELETE CASCADE
        );""",

    'health' : f"""CREATE TABLE IF NOT EXISTS health (
        entry_id serial PRIMARY KEY,
        acidity BOOLEAN,
        backpain BOOLEAN,
        bloating BOOLEAN,
        breakouts BOOLEAN,
        chestpain BOOLEAN,
        constipation BOOLEAN,
        defecation BOOLEAN,
        diarrhea BOOLEAN,
        dizziness BOOLEAN,
        hard_stool BOOLEAN,
        headache BOOLEAN,
        indigestion BOOLEAN,
        medication TEXT,
        nausea BOOLEAN,
        numbness TEXT,
        other_symptoms TEXT,
        palpitations BOOLEAN,
        panic_attack BOOLEAN,
        breathless BOOLEAN,
        RHR INT,
        sick TEXT,
        stomachpain BOOLEAN,
        date TIMESTAMP NOT NULL,
        user_id INT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users ON DELETE CASCADE
        );""",

    'food' : f"""CREATE TABLE IF NOT EXISTS food (
        entry_id serial PRIMARY KEY,
        animal_products TEXT,
        cereal TEXT,
        unhealthy_food TEXT,
        enough_water BOOLEAN,
        fruits TEXT,
        healthy BOOLEAN,
        laxatives TEXT,
        supplements TEXT,
        date TIMESTAMP NOT NULL,
        user_id INT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users ON DELETE CASCADE
        );""",

    'fitness' : f"""CREATE TABLE IF NOT EXISTS fitness (
        entry_id serial PRIMARY KEY,
        cycling BOOLEAN,
        cycling_time INT,
        gym BOOLEAN,
        gym_time INT,
        cardio BOOLEAN,
        cardio_time INT,
        stretching BOOLEAN,
        stretching_time INT,
        yoga BOOLEAN,
        yoga_time INT,
        other BOOLEAN,
        other_time INT,
        date TIMESTAMP NOT NULL,
        user_id INT NOT NULL,
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
        CONSTRAINT yogqa_check CHECK
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
        entry_id serial PRIMARY KEY,
        cramps BOOLEAN,
        cramps_level INT CHECK ((cramps_level > 0) AND (cramps_level <5) OR NULL),
        cycle_day INT NOT NULL,
        infection TEXT,
        ovulation BOOLEAN,
        period BOOLEAN,
        intercourse BOOLEAN,
        spotting BOOLEAN,
        spotting_level INT CHECK ((spotting_level > 0) AND (spotting_level <3) OR NULL),
        date TIMESTAMP NOT NULL,
        user_id INT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users ON DELETE CASCADE
        );""",

    'longterm' : f"""CREATE TABLE IF NOT EXISTS longterm (
        entry_id serial PRIMARY KEY,
        anatomical TEXT,
        climate TEXT,
        hormonal TEXT,
        nutritional TEXT,
        social TEXT,
        date TIMESTAMP NOT NULL,
        user_id INT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users ON DELETE CASCADE
        );""",

    'sleep' : f"""CREATE TABLE IF NOT EXISTS sleep (
        entry_id serial PRIMARY KEY,
        sleep REAL CHECK ((sleep > 0.0) AND (sleep < 24.0) OR NULL),
        REM REAL CHECK ((REM > 0.0) AND (REM < 1.0) OR NULL),
        awake REAL CHECK ((awake > 0.0) AND (awake < 1.0) OR NULL),
        deep_sleep REAL CHECK ((deep_sleep > 0.0) AND (deep_sleep < 1.0) OR NULL),
        light_sleep REAL CHECK ((light_sleep > 0.0) AND (light_sleep < 1.0) OR NULL),
        sleep_score INT CHECK ((sleep_score > 0) AND (sleep_score < 100) OR NULL),
        insomnia BOOLEAN,
        freq_wakes BOOLEAN,
        sleep_meds TEXT,
        tz_change BOOLEAN NOT NULL DEFAULT '0',
        date TIMESTAMP NOT NULL,
        user_id INT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users ON DELETE CASCADE
        );"""
}
    
create_db(password=database_pw)

for name, query in queries.items():
    create_table(query, name, password=database_pw)