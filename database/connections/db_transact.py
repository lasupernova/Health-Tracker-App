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
    table_cols, val_placeholders = get_column_names(table)
    con = connect_db(password=database_pw)
    cur = con.cursor()
    query = f"""INSERT INTO users ({table_cols}) VALUES ({val_placeholders});""" #To Do: add password encryption (in database)
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

    val_PH = ['%s']*(len(cols)-2) #placeholder-string for values in query; create BEFORE converting cols into string!
    val_PH = ', '.join(str(x) for x in val_PH)

    cols = ", ".join(str(x) for x in cols[1:-1])

    print(val_PH)

    return cols, val_PH

def sign_up(user, password):
    try:
        con = connect_db(password=database_pw)

        query_check = f"""SELECT * FROM users WHERE username=%s;"""

        query_ins = f"""INSERT INTO users (username, password) VALUES (%s, %s);"""

        with con.cursor() as cur: #closes transaction, but does NOT close the connection itself
            cur.execute(query_check, (user, ))
            rows = cur.fetchone()
            if rows: #if user already exists, return -1 to display error message
                return -1
            else:
                cur.execute(query_ins, (user, password)) 
                return 1
    
    except Exception as e:
        print(e)
        return 0
    
    finally:
        con.close()


def query_data_by_date(date, user):
    try:
        con = connect_db(password=database_pw)

        query = f"""SELECT * FROM fitness 
                          WHERE date(date) = %s and user_id = %s;"""  #date() is a type cast and can also be written as created_date::date or cast(created_data as date)

        uid = get_uid_by_username(user)
        
        with con.cursor() as cur: #closes transaction, but does NOT close the connection itself
            cur.execute(query, (date, uid)) 
            rows = cur.fetchone()
            if rows: #if user already exists, return -1 to display error message
                print(rows)
                return rows
            else:
                print("No data available for that date!")
                return 0
    
    except Exception as e:
        print(e)
        return 0
    
    finally:
        con.close()


def get_uid_by_username(user):
    try:
        con = connect_db(password=database_pw)

        query = f"""SELECT user_id FROM users WHERE username=%s;"""

        with con.cursor() as cur: #closes transaction, but does NOT close the connection itself
            cur.execute(query, (user, )) 
            rows = cur.fetchone()
            if rows:
                return rows[0]
            else:
                return -1
    
    except Exception as e:
        print(e)
        return 0
    
    finally:
        con.close()



