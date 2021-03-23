import psycopg2
from dotenv import load_dotenv 
import os
import pandas as pd

# ----- dataFrame part -----
df = pd.read_csv("test_df.csv", index_col= 0, parse_dates=True, header=[0, 1], skipinitialspace=True)


fit = df['fitness']
 
# fit.columns = fit.columns.droplevel(axis=1)
for col in fit.columns:
    print(col)

print(fit.index.values)


# ----- Database part -----
# load environmental variables required for connection
load_dotenv()
database_pw = os.environ["DATABASE_PASSWORD"]
print(database_pw)

conn = psycopg2.connect(f"host=localhost dbname=health_tracker user=postgres port=5432 password={database_pw}")

get_uid_from_uname = '''SELECT user_id FROM users WHERE username='gabri';'''
insert_data = '''INSERT INTO fitness (user_id, cycling_time, gym, cardio_time, stretching_time, cycling, cardio, stretching, other, yoga, date) VALUES (%s, %s, %s, %s, %s, %s,%s,%s,True,True, %s)'''

cur = conn.cursor()

cur.execute(get_uid_from_uname)

uid_oi = cur.fetchone()[0]

# cur.execute(insert_data, (10,True,12,13))
for idx in fit.index:

    date = idx
    gym = True if fit.loc[idx, 'gym']==1 else False
    print(f"GYM: {gym}")
    cardio = int(fit.loc[idx, 'running/cardio [mins]']) #if ((type(int(fit.loc[idx, 'running/cardio [mins]'])) == int) and int(fit.loc[idx, 'running/cardio [mins]'])>0) else 1
    print(f"Cardio: {cardio}, {type(cardio)}")
    c = False if cardio==0 else True
    stretch = int(fit.loc[idx, 'stretching [mins]']) #if ((type(int(fit.loc[idx, 'stretching [mins]'])) ==int) and int(fit.loc[idx, 'stretching [mins]'])>0) else 1
    print(f"Stretch: {stretch}")
    s = False if stretch==0 else True
    cycling = int(fit.loc[idx, 'cycling [mins]']) #if ((type(int(fit.loc[idx, 'cycling [mins]'])) ==int) and int(fit.loc[idx, 'cycling [mins]'])>0) else 1
    print(f"cycling: {cycling}")
    cy = False if cycling==0 else True

    try:
        cur.execute(insert_data, (uid_oi, cycling, gym, cardio, stretch, cy, c, s, date))
    except Exception as e: 
        print(e)

conn.commit()
conn.close()
    
print('DONE')
