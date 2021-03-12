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

def add_data(table, user, password):
    table_cols = get_column_names(table)
    con = connect_db(password=database_pw)
    cur = con.cursor()
    query = f"""INSERT INTO users ({table_cols}) VALUES (%s, %s);""" #To Do: add password encryption (in database)
    # crypt_pw = crypt(password, gen_salt('bf'))
    cur.execute(query, (user, password)) 
    con.commit()    
    print("New user signed up!")
    print(f"\t username: {user}; password: {password}")
    con.close() #TO DO: modify code to use "with connection:" instead

def login_user(user, password):
    con = connect_db(password=database_pw)

    query = f"""SELECT password FROM users WHERE username=%s;"""

    with con.cursor() as cur:
        cur.execute(query, (user, ))

        rows = cur.fetchone() #there will be 1 amnd only 1 entry per username

        if rows: #compare password input to database pw, if query returns something
            pw = rows[0]
            if password == pw:
                return 1
            else:
                return 0
        else: #if query does not return result -> no entry for this specific user
            return -1

def get_column_names(table):
    '''
    Get all column names from specified table;
    Create string with all column names separated by commas;
    Create string with placeholder for number of values to pass to query - based on number of columns in columns-string;
    Return columns-string to pass on to subsequent function for use in query
    '''
    con = connect_db(password=database_pw)
    query = f"""SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=%s;"""

    with con.cursor() as cur:
        cur.execute(query, (table, ))
        rows=cur.fetchall() 
    
    cols = []
    for row in rows:
        cols.append(row[0])

    cols = ", ".join(str(x) for x in cols[1:-1])

    val_PH = ['%s']*len(cols) #placeholder-string for values in query
    val_PH = ', '.join(str(x) for x in val_PH)

    return cols, val_PH

add_data('users','gabri','ela')



