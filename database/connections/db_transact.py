#To Do: add password encryption (in database)
#TO DO: investigate "with connection:" and replace 
# To Do: add Constraint to allow only Unique day per user_id for each table
# TO DO: get data-dict values from keys as dicts do not have an order and same order needs to be ensured in extrcated cols and extracted values

# import libraries and modules
import psycopg2
import psycopg2.errorcodes
from dotenv import load_dotenv 
import datetime
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


def add_data(table, *args):
    '''
    Inserts data into table for specific user;
    New data passed as *args;
    '''

    # extract info from arguments
    table = table.lower()
    data, user = args

    # get user_if from username and add to data-dict
    user_id = get_uid_by_username(user)
    data['user_id'] = user_id

    # get cols and corresponding values from completed data-dict
    col_str, val_placeholders, vals = extract_query_data_from_dict(data)

    try:
        # connection + query
        con = connect_db(password=database_pw)
        with con.cursor() as cur:
            query = f"""INSERT INTO {table} ({col_str}) VALUES ({val_placeholders});""" 
            cur.execute(query, (tuple(vals)))
    except psycopg2.errors.UniqueViolation as e:  #update if entry already exists for table - pkey
        print("ERROR CAUGHT!")
        # con.close()
        update_data(table, data)
    finally:
        con.commit()   
        con.close() 


def update_data(table, data):
    '''
    Update specified table based on information in data dict
    '''

    # extract date from dict and pop (date+user_id) as these are not going to be updated but are going to be used in the WHERE clause
    date = data['date']
    data.pop('date')
    user_id = data['user_id']
    data.pop('user_id')
    print(data)

    # extract variables to pass to SQL-query and execute statement from data-dict
    col_str, val_placeholders, vals = extract_query_data_from_dict(data)

    # extend date and user_id -- list mutable tuple not --> convert to tuple after
    vals.extend([date, user_id])

    con = connect_db(password=database_pw)
    with con.cursor() as cur:
        query = f"""UPDATE {table} SET ({col_str}) = ({val_placeholders}) WHERE (date = %s and user_id = %s) RETURNING *;""" 
        # query = f"""SELECT * FROM {table} WHERE (date = %s and user_id = %s);""" 
        cur.execute(query, (vals)) #, date, user_id
        print(cur.rowcount)
    # print(f'SUCCESS! Updated database table "{table}" for user_id "{user_id}" and date "{date}"')
    con.commit()
    con.close()


def extract_query_data_from_dict(data):
    '''
    Takes data-dict with columns specified in keys and column-values in dict-values;
    Extracts columns-list from keys and value-tuple from dict-values;
    Creates placeholder string for SQL-query and converts column-list into a string for SQL-query;
    Returns col_str and val_placeholder to pass to SQL-query and vals-list to pass to psycopg2-execute statement to replace query-placeholders;
    '''

    # extract data from data-dict
    cols_list = list(data.keys())
    vals = list(data.values())

    # create additional variables to pass to SQL-statement
    val_placeholders = ', '.join(['%s']*len(vals)) 
    col_str = ', '.join(cols_list)

    return col_str, val_placeholders, vals

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
