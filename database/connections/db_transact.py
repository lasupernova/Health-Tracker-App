#To Do: add password encryption (in database)

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
    '''
    Connects to specific database
    '''

    return psycopg2.connect(f"user={user} host={host} dbname={database} password={password} port={port}")


def add_data(table, user, password):
    '''
    Inserts data into table for specific user
    '''

    # get column names for specified table
    cols_list = list(get_columns_from_table(table))
    cols = ', '.join(cols_list[1:-1])

    # create value placeholder string with correct number of columns values - to pass on to query
    val_placeholders = ['%s']*(len(cols_list)-2)
    val_placeholders = ', '.join(str(x) for x in val_placeholders)

    # connection + query
    con = connect_db(password=database_pw)
    cur = con.cursor()
    query = f"""INSERT INTO users ({cols}) VALUES ({val_placeholders});""" 
    cur.execute(query, (user, password)) 
    con.commit()   
    con.close() #TO DO: modify code to use "with connection:" instead 

    # info message
    print("New user signed up!")
    print(f"\t username: {user}; password: {password}")  


def login_user(user, password):
    '''
    Checks if inserted credentials match to login user in GUI
    '''

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


def sign_up(user, password):
    '''
    Inserts new user into users table in order to sign up new user to health tracker app
    '''

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
        con.commit()
        con.close()


def query_data_by_date_and_user(date, user):
    '''
    Returns dict of all health data for a specified user and a specified data
    '''

    try:
        con = connect_db(password=database_pw)

        uid = get_uid_by_username(user)

        table_names = get_table_list()

        if table_names == 0: #if exception was thrown calling get_table_list()
            return 0

        else:
            data_dict = {}

            for table in table_names:

                data_dict[table] = {}

                col_names = get_columns_from_table(table)

                data = get_table_data(table, date, uid)

                for col, value in zip(col_names, data):
                    if col == 'user_id' or col == 'entry_id' or col == 'date':  #exclude these three ocolumns, as they do not contain health data
                        pass
                    else:
                        data_dict[table][str(col)] = value if str(value) != 'nan' else None

        return data_dict

    except Exception as e:
        print(e)
        return 0
    
    finally:
        con.close()


def get_table_list():
    '''
    Returns list of all table names in database
    '''

    try:
        con = connect_db(password=database_pw)

        query_tables = """SELECT * 
                          FROM information_schema.tables 
                          WHERE table_schema = 'public' 
                          AND table_type = 'BASE TABLE'
                          ;""" #NOTE: 'BASE TABLE' will only list tables and exclude views
        
        with con.cursor() as cur:  #closes transaction, but does NOT close the connection itself
            cur.execute(query_tables) 

            tables = cur.fetchall()  #returns a list of tuples with table_information

            table_names = [table[2] for table in tables if table[2]!='users'] #exclude 'users'-table as it does not contain any health data

        return table_names
    
    except Exception as e:
        print(e)
        return 0
    
    finally:
        con.close()


def get_columns_from_table(table_name):
    '''
    Get all column information for all columns in specified table;
    Create tuple with only columns name information for each column;
    Return columns name tuple to pass on to subsequent function to create data-dict to be passed on to health tracker
    '''
    try:
        con = connect_db(password=database_pw)
        
        query_columns = f"""SELECT *
                        FROM information_schema.columns
                        WHERE table_schema = 'public'
                        AND table_name   = %s
                        ;"""
        
        with con.cursor() as cur:  

            cur.execute(query_columns, (table_name, )) 

            col_info = cur.fetchall()

        if not col_info:
            return 0
        
        else:
            col_names = [column[3] for column in col_info]
            return col_names

    except Exception as e:
        print(e)
        return 0
    
    finally:
        con.close()


def get_table_data(table_name, date, user):
    '''
    Retrieve data from specified database table for specified user and date;
    Return information as a tuple with one value per column;
    '''

    try:
        con = connect_db(password=database_pw)
        
        query_data = f"""SELECT * 
                         FROM {table_name}
                         WHERE date(date) = %s and user_id = %s
                         ;"""  #date() is a type cast and can also be written as created_date::date or cast(created_data as date)
        
        with con.cursor() as cur:  

            cur.execute(query_data, (date, user)) 

            data = cur.fetchall()

        if not data:
            return 0
        
        else:
            return data[0]

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
