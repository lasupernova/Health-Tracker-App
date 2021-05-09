# import libraries and modules
import psycopg2
from dotenv import load_dotenv 
import os

# load environmental variables required for connection
load_dotenv()
database_pw = os.environ["DATABASE_PASSWORD"]
print(database_pw)


def connect_db(user='postgres', host='localhost', port='5432', database='health_tracker', password='postgres'):
    return psycopg2.connect(f"user={user} host={host} dbname={database} password={password} port={port}")


# def add_columns_to_table(table, columns:list, col_type:list, addition=None):
def add_columns_to_table():

    # cols = ", ".join(columns)
    # col_types = ", ".join(col_type)

    # to_append = ""

    # for col, ctype in zip(columns, col_type):
    #     to_append += f"\nADD COLUMN {col} {ctype}"

    try:

            query = f'''ALTER TABLE users
                        ADD COLUMN sex SMALLINT,
                        ADD COLUMN DOB DATE;
                        '''

            con = connect_db(password=database_pw)
            
            with con.cursor() as cur:  #closes transaction, but does NOT close the connection itself
                cur.execute(query) 

            con.commit()
            print("Success running the following query: \n", query)
            return 1

            

        #### TO DO: add elif + error message if table is given but not columns or vice versa

    except Exception as e:
        print(e)
        return 0

    finally:
        con.close()

if __name__ == '__main__':
    add_columns_to_table()
