#To Do: add password encryption (in database)
#TO DO: investigate "with connection:" and replace 
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
# print(database_pw)  ##uncomment for troubleshooting

db = 'health_tracker2'

def connect_db(user='postgres', host='localhost', port='5432', database=db, password='postgres'):
    '''
    Connects to specific database
    '''
    print(f"Connected to: {db}")
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
        print("ENTRY ALREADY EXISTS FOR THIS DATE -- UPDATING ENTRY!")
        update_data(table, data)
    finally:
        con.commit()   
        con.close() 


def update_data(table, data):
    '''
    Update specified table based on information in data dict
    '''

    # extract date from dict and pop (date+user_id) as these are not going to be updated but are going to be used in the WHERE clause + need to be at the end of list
    date = data['date']
    data.pop('date')
    user_id = data['user_id']
    data.pop('user_id')

    # extract variables to pass to SQL-query and execute statement from data-dict
    col_str, val_placeholders, vals = extract_query_data_from_dict(data)

    # extend date and user_id -- list mutable tuple not --> convert to tuple after
    vals.extend([date, user_id])

    con = connect_db(password=database_pw)
    with con.cursor() as cur:
        query = f"""UPDATE {table} SET ({col_str}) = ROW({val_placeholders}) WHERE (date = %s and user_id = %s);""" 
        # query = f"""SELECT * FROM {table} WHERE (date = %s and user_id = %s);""" 
        cur.execute(query, (vals)) #, date, user_id

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

def get_gender(user):
    '''
    Checks if inserted credentials match to login user in GUI
    '''

    con = connect_db(password=database_pw)

    query = f"""SELECT sex FROM users WHERE username=%s;"""

    with con.cursor() as cur:
        cur.execute(query, (user, ))

        rows = cur.fetchone()

        if rows: 
            return 'female' if rows[0]==1 else 'male' if rows[0]==0 else 'undetermined'
        else: #if query does not return result -> no entry for this specific user
            return -1

def sign_up(user, password, sex, dob):
    '''
    Inserts new user into users table in order to sign up new user to health tracker app
    '''

    try:
        con = connect_db(password=database_pw)

        query_check = f"""SELECT * FROM users WHERE username=%s;"""
        query_ins = f"""INSERT INTO users (username, password, sex, DOB) VALUES (%s, %s, %s, %s);"""

        with con.cursor() as cur: #closes transaction, but does NOT close the connection itself
            cur.execute(query_check, (user, ))
            rows = cur.fetchone()
            if rows: #if user already exists, return -1 to display error message
                return -1
            else:
                cur.execute(query_ins, (user, password, sex, dob)) 
                return 1
    
    except Exception as e:
        print(e)
        return 0
    
    finally:
        con.commit()
        con.close()

def check_user_existance(user):
    '''
    Check if user already exists in 'users' table
    '''

    try:
        con = connect_db(password=database_pw)

        query_check = f"""SELECT * FROM users WHERE username=%s;"""

        with con.cursor() as cur: #closes transaction, but does NOT close the connection itself
            cur.execute(query_check, (user, ))
            rows = cur.fetchone()
            if rows: #if user already exists, return -1 to display error message
                return -1
            else:
                return 0
    
    except Exception as e:
        print(e)
        return 1
    
    finally:
        con.commit()
        con.close()


def query_data_by_date_and_user(date, user, end_date=None):
    '''
    Returns dict of all health data for a specified user and a specified data
    '''

    try:
        uid = get_uid_by_username(user)

        table_names = get_table_list()

        if table_names == 0: #if exception was thrown calling get_table_list()
            return 1

        else:
            data_dict = {}

            for table in table_names:

                col_names = get_columns_from_table(table)

                if end_date==None:
                    data = get_table_data(table, date, uid)
                else:
                    data = get_table_data(table, date, end_date, user)

                if data != 0:
                    data_dict[table] = {}
                    for col, value in zip(col_names, data):
                        if col == 'user_id' or col == 'date':  #exclude these two columns, as they do not contain health data
                            pass
                        else:
                            data_dict[table][str(col)] = value if str(value) != 'nan' else None
                else:
                    continue

            if data_dict:
                return data_dict
            else:
                return 2

    except Exception as e:
        print(e)
        return -1

def query_data_between_dates_by_user(user:str, start_date=None, end_date=None, table:str=None, columns:list=None):
    """
    Query data from specified table and columns between a start and an end date for a specified user.
    When start - and end_date default to None: data for all dates is returned

    Parameters:
        user: username - a string
        start_date: start_date of query (default: None - e.g. for food data) - a datetime object
        end_date: end_date of query (default: None - e.g. for food data) - a datetime object
        table: name of table in database to query - a string
        columns: name(s) of column(s) in table to get data from - a list

    Returns:
        data - a list of tuples with with one tuple per returned entry data
    """
    if start_date != None and end_date != None:
        try:

            uid = get_uid_by_username(user)

            if table == None and columns==None:
                pass   #query_data_by_date_and_user(date, user, end_date)

            elif table != None and columns!=None:

                col_str = ', '.join(columns)

                query = f'''SELECT {col_str}
                            FROM {table}
                            WHERE
                            (date(date) between date(%s) and date(%s)) 
                            AND (user_id=%s);
                            '''

                con = connect_db(password=database_pw)
                
                with con.cursor() as cur:  #closes transaction, but does NOT close the connection itself
                    cur.execute(query, (start_date, end_date, uid)) 

                    data = cur.fetchall()  #returns a list of tuples with table_information

                return data

            #### TO DO: add elif + error message if table is given but not columns or vice versa

        except Exception as e:
            print(e)
            return 0

    else:
        try:

            uid = get_uid_by_username(user)

            if table == None and columns==None:
                pass   #query_data_by_date_and_user(date, user, end_date)

            elif table != None and columns!=None:

                col_str = ', '.join(columns)

                query = f'''SELECT {col_str}
                            FROM {table}
                            WHERE
                            (user_id=%s);
                            '''

                con = connect_db(password=database_pw)
                
                with con.cursor() as cur:  #closes transaction, but does NOT close the connection itself
                    cur.execute(query, (uid, )) 

                    data = cur.fetchall()  #returns a list of tuples with table_information

                return data

            #### TO DO: add elif + error message if table is given but not columns or vice versa

        except Exception as e:
            print(e)
            return 0        


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


def get_table_data(table_name, date, user, end_date=None):
    '''
    Retrieve data from specified database table for specified user and date;
    Return information as a tuple with one value per column;
    '''

    try:
        con = connect_db(password=database_pw)
        
        if end_date==None:
            query_data = f"""SELECT * 
                            FROM {table_name}
                            WHERE date(date) = %s and user_id = %s
                            ;"""  #date() is a type cast and can also be written as created_date::date or cast(created_data as date)

            execution_params = (date, user)

        else:
            query_data = f"""SELECT * 
                FROM {table_name}
                WHERE (date(date) between %s and %s) AND (user_id = %s)
                ;"""  #date() is a type cast and can also be written as created_date::date or cast(created_data as date)

            execution_params = (date, end_date, user)
        
        with con.cursor() as cur:  

            cur.execute(query_data, execution_params) 

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

