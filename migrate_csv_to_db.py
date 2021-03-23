import psycopg2
from dotenv import load_dotenv 
import os
import pandas as pd

# ----- dataFrame part -----
df = pd.read_csv("test_df.csv", index_col= 0, parse_dates=True, header=[0, 1], skipinitialspace=True)





# ----- Database part -----
# load environmental variables required for connection
load_dotenv()
database_pw = os.environ["DATABASE_PASSWORD"]
print(database_pw)

conn = psycopg2.connect(f"host=localhost dbname=health_tracker user=postgres port=5432 password={database_pw}")

get_uid_from_uname = '''SELECT user_id FROM users WHERE username='gabri';'''
cur = conn.cursor()
cur.execute(get_uid_from_uname)
conn.commit()

uid_oi = cur.fetchone()[0]

# -----FITNESS TABLE -----

# fit = df['fitness']

# insert_data = '''INSERT INTO fitness (user_id, cycling_time, gym, cardio_time, stretching_time, cycling, cardio, stretching, other, yoga, date) VALUES (%s, %s, %s, %s, %s, %s,%s,%s,True,True, %s)'''


# # cur.execute(insert_data, (10,True,12,13))
# for idx in fit.index:

#     date = idx
#     gym = True if fit.loc[idx, 'gym']==1 else False
#     print(f"GYM: {gym}")
#     cardio = int(fit.loc[idx, 'running/cardio [mins]']) #if ((type(int(fit.loc[idx, 'running/cardio [mins]'])) == int) and int(fit.loc[idx, 'running/cardio [mins]'])>0) else 1
#     print(f"Cardio: {cardio}, {type(cardio)}")
#     c = False if cardio==0 else True
#     stretch = int(fit.loc[idx, 'stretching [mins]']) #if ((type(int(fit.loc[idx, 'stretching [mins]'])) ==int) and int(fit.loc[idx, 'stretching [mins]'])>0) else 1
#     print(f"Stretch: {stretch}")
#     s = False if stretch==0 else True
#     cycling = int(fit.loc[idx, 'cycling [mins]']) #if ((type(int(fit.loc[idx, 'cycling [mins]'])) ==int) and int(fit.loc[idx, 'cycling [mins]'])>0) else 1
#     print(f"cycling: {cycling}")
#     cy = False if cycling==0 else True

#     try:
#         cur.execute(insert_data, (uid_oi, cycling, gym, cardio, stretch, cy, c, s, date))
#     except Exception as e: 
#         print(e)

# conn.commit()

# -----FOOD TABLE -----

# food = df.food

# # fit.columns = fit.columns.droplevel(axis=1)
# for col in food.columns:
#     print(col)

# food_query = f'''INSERT INTO food (animal_products, cereal, unhealthy_food, enough_water, fruits, healthy, laxatives, supplements, date, user_id)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, {uid_oi})'''

# for idx in food.index:
#     date = idx
#     animal_prod = str(food.loc[idx, 'animal products']) if str(food.loc[idx, 'animal products']) != '[nan]' else None
#     cereal = food.loc[idx, 'cereal'] if str(food.loc[idx, 'cereal']) != '[nan]' else None
#     cheats = food.loc[idx, 'cheats/sweets/unhealthy'] if str(food.loc[idx, 'cheats/sweets/unhealthy']) != '[nan]' else None
#     water = bool(food.loc[idx, 'enough water?'])
#     fruits = food.loc[idx, 'fruits'] if str(food.loc[idx, 'fruits']) != '[nan]' else None
#     healthy = bool(food.loc[idx, 'healthy'])
#     laxatives = food.loc[idx, 'laxatives'] if str(food.loc[idx, 'laxatives']) != '[nan]' else None
#     supps = food.loc[idx, 'supplements'] if str(food.loc[idx, 'supplements']) != '[nan]' else None

#     with conn.cursor() as cur:
#         cur.execute(food_query, (animal_prod, cereal, cheats, water, fruits, healthy, laxatives, supps, date))
#         conn.commit()

# # ----- mood -----
# mood = df.mood

# for col in mood.columns:
#     print(col)

# mood_query = f'''INSERT INTO mood (angry, anxious, calm, content, depressed, emotional, energetic, excited, frustrated, happy, hyper, moody, motivated, relaxed, sad, sensitive, stressed, tired, date, user_id)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, {uid_oi})'''

# for idx in mood.index:
#     date = idx
#     angry = bool(mood.loc[idx, 'angry'])
#     anxious = bool(mood.loc[idx, 'anxious'])
#     calm = bool(mood.loc[idx, 'calm'])
#     content = bool(mood.loc[idx, 'content'])
#     depressed = bool(mood.loc[idx, 'depressed'])
#     emotional = bool(mood.loc[idx, 'emotional'])
#     energetic = bool(mood.loc[idx, 'energetic'])
#     excited = bool(mood.loc[idx, 'excited'])
#     frustrated = bool(mood.loc[idx, 'frustrated'])
#     happy = bool(mood.loc[idx, 'happy'])
#     hyper = bool(mood.loc[idx, 'hyper'])
#     moody = bool(mood.loc[idx, 'moody'])
#     motivated = bool(mood.loc[idx, 'motivated'])
#     relaxed = bool(mood.loc[idx, 'relaxed'])
#     sad = bool(mood.loc[idx, 'sad'])
#     sensitive = bool(mood.loc[idx, 'sensitive'])
#     stressed = bool(mood.loc[idx, 'stressed'])
#     tired = bool(mood.loc[idx, 'tired'])

#     with conn.cursor() as cur:
#         cur.execute(mood_query, (angry, anxious, calm, content, depressed, emotional, energetic, excited, frustrated, happy, hyper, moody, motivated, relaxed, sad, sensitive, stressed, tired, date))
#         conn.commit()


conn.close()
    
print('DONE')
 