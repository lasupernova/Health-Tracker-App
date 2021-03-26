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

fit = df['fitness']

insert_data = '''INSERT INTO fitness (user_id, cycling_time, gym, cardio_time, stretching_time, cycling, cardio, stretching, other, yoga, date) VALUES (%s, %s, %s, %s, %s, %s,%s,%s,True,True, %s)'''


# cur.execute(insert_data, (10,True,12,13))
for idx in fit.index:

    date = idx
    gym = True if fit.loc[idx, 'gym']==1 else False

    cardio = int(fit.loc[idx, 'running/cardio [mins]']) #if ((type(int(fit.loc[idx, 'running/cardio [mins]'])) == int) and int(fit.loc[idx, 'running/cardio [mins]'])>0) else 1

    c = False if cardio==0 else True
    stretch = int(fit.loc[idx, 'stretching [mins]']) #if ((type(int(fit.loc[idx, 'stretching [mins]'])) ==int) and int(fit.loc[idx, 'stretching [mins]'])>0) else 1

    s = False if stretch==0 else True
    cycling = int(fit.loc[idx, 'cycling [mins]']) #if ((type(int(fit.loc[idx, 'cycling [mins]'])) ==int) and int(fit.loc[idx, 'cycling [mins]'])>0) else 1

    cy = False if cycling==0 else True

    try:
        cur.execute(insert_data, (uid_oi, cycling, gym, cardio, stretch, cy, c, s, date))
    except Exception as e: 
        print(e)

conn.commit()

# -----FOOD TABLE -----

food = df.food

# fit.columns = fit.columns.droplevel(axis=1)
for col in food.columns:
    print(col)

food_query = f'''INSERT INTO food (animal_products, cereal, unhealthy_food, enough_water, fruits, healthy, laxatives, supplements, date, user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, {uid_oi})'''

for idx in food.index:
    date = idx
    animal_prod = str(food.loc[idx, 'animal products']) if str(food.loc[idx, 'animal products']) != '[nan]' else None
    cereal = food.loc[idx, 'cereal'] if str(food.loc[idx, 'cereal']) != '[nan]' else None
    cheats = food.loc[idx, 'cheats/sweets/unhealthy'] if str(food.loc[idx, 'cheats/sweets/unhealthy']) != '[nan]' else None
    water = bool(food.loc[idx, 'enough water?'])
    fruits = food.loc[idx, 'fruits'] if str(food.loc[idx, 'fruits']) != '[nan]' else None
    healthy = bool(food.loc[idx, 'healthy'])
    laxatives = food.loc[idx, 'laxatives'] if str(food.loc[idx, 'laxatives']) != '[nan]' else None
    supps = food.loc[idx, 'supplements'] if str(food.loc[idx, 'supplements']) != '[nan]' else None

    with conn.cursor() as cur:
        cur.execute(food_query, (animal_prod, cereal, cheats, water, fruits, healthy, laxatives, supps, date))
        conn.commit()

# ----- mood -----
mood = df.mood

for col in mood.columns:
    print(col)

mood_query = f'''INSERT INTO mood (angry, anxious, calm, content, depressed, emotional, energetic, excited, frustrated, happy, hyper, moody, motivated, relaxed, sad, sensitive, stressed, tired, date, user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, {uid_oi})'''

for idx in mood.index:
    date = idx
    angry = bool(mood.loc[idx, 'angry'])
    anxious = bool(mood.loc[idx, 'anxious'])
    calm = bool(mood.loc[idx, 'calm'])
    content = bool(mood.loc[idx, 'content'])
    depressed = bool(mood.loc[idx, 'depressed'])
    emotional = bool(mood.loc[idx, 'emotional'])
    energetic = bool(mood.loc[idx, 'energetic'])
    excited = bool(mood.loc[idx, 'excited'])
    frustrated = bool(mood.loc[idx, 'frustrated'])
    happy = bool(mood.loc[idx, 'happy'])
    hyper = bool(mood.loc[idx, 'hyper'])
    moody = bool(mood.loc[idx, 'moody'])
    motivated = bool(mood.loc[idx, 'motivated'])
    relaxed = bool(mood.loc[idx, 'relaxed'])
    sad = bool(mood.loc[idx, 'sad'])
    sensitive = bool(mood.loc[idx, 'sensitive'])
    stressed = bool(mood.loc[idx, 'stressed'])
    tired = bool(mood.loc[idx, 'tired'])

    with conn.cursor() as cur:
        cur.execute(mood_query, (angry, anxious, calm, content, depressed, emotional, energetic, excited, frustrated, happy, hyper, moody, motivated, relaxed, sad, sensitive, stressed, tired, date))
        conn.commit()

health = df.health

print(sorted(list(health.columns)))

num_cols = ('%s, '*22)

health_query = f'''INSERT INTO health (acidity, backpain, bloating, breakouts, chestpain, constipation, defecation, diarrhea, dizziness, hard_stool, headache, indigestion, medication, nausea, numbness, other_symptoms, palpitations, panic_attack, breathless, sick, stomachpain, date, user_id)
                VALUES ({num_cols} {uid_oi})'''

for idx in health.index:
    date = idx
    acidity = bool(health.loc[idx, 'acidity']) 
    backache = bool(health.loc[idx, 'backache'])  
    bloating = bool(health.loc[idx, 'bloating'])  
    breakouts= bool(health.loc[idx, 'breakouts'])  
    chestpain = bool(health.loc[idx, 'chestpain'])  
    constipation = bool(health.loc[idx, 'constipation'])  
    defecation = bool(health.loc[idx, 'defecation'])  
    diarrhea = bool(health.loc[idx, 'diarrhea'])  
    dizziness = bool(health.loc[idx, 'dizziness'])  
    hard_stool = bool(health.loc[idx, 'hard stool'])  
    headache = bool(health.loc[idx, 'headache'])  
    indigestion = bool(health.loc[idx, 'indigestion'])  
    medication = str(health.loc[idx, 'medication']) if str(health.loc[idx, 'medication']) != '[nan]' else None
    nausea = bool(health.loc[idx, 'nausea'])  
    numbness = str(health.loc[idx, 'numbness']) if str(health.loc[idx, 'numbness']) != '[nan]' else None
    other_symptoms = bool(health.loc[idx, 'other symptoms']) if str(health.loc[idx, 'other symptoms']) != '[nan]' else None
    palpitations = bool(health.loc[idx, 'palpitations'])  
    panic_attack = bool(health.loc[idx, 'panic attack'])  
    breathless = bool(health.loc[idx, 'shortness of breath']) 
    sick = bool(health.loc[idx, 'sick?']) if str(health.loc[idx, 'sick?']) != '[nan]' else None
    stomachpain = bool(health.loc[idx, 'stomachpain'])

    with conn.cursor() as cur:
        cur.execute(health_query, (acidity, backache, bloating, breakouts, chestpain, constipation, defecation, diarrhea, dizziness, hard_stool, headache, indigestion, medication, nausea, numbness, other_symptoms, palpitations, panic_attack, breathless, sick, stomachpain, date))
        conn.commit()

period = df.period

print(sorted(list(period.columns)))

num_cols = ('%s, '*10)

# print(period.spotting.unique())

period_query = f'''INSERT INTO period (cramps, cramps_level, cycle_day, infection, ovulation, period, intercourse, spotting, spotting_level, date, user_id)
                VALUES ({num_cols} {uid_oi})'''

for idx in period.index:
    date = idx
    cramps = bool(period.loc[idx, 'cramps']) 
    cramps_level = 2 if cramps==1 else 0
    cycle_day = int(period.loc[idx, 'cycle day']) 
    infection = str(period.loc[idx, 'infection']) if str(period.loc[idx, 'infection']) != '[nan]' else None
    ovulation = bool(period.loc[idx, 'ovulation'])
    period_ = bool(period.loc[idx, 'period'])
    intercourse = bool(period.loc[idx, 'sex'])
    spotting = bool(period.loc[idx, 'spotting'])
    spotting_level = 2 if spotting==1 else 0

    with conn.cursor() as cur:
        cur.execute(period_query, (cramps, cramps_level, cycle_day, infection, ovulation, period_, intercourse, spotting, spotting_level, date))
        conn.commit()

lt = df.longterm

print(sorted(list(lt.columns)))

num_cols = ('%s, '*6)

# print(period.spotting.unique())

lt_query = f'''INSERT INTO longterm (anatomical, climate, hormonal, nutritional, social, date, user_id)
                VALUES ({num_cols} {uid_oi})'''

for idx in lt.index:
    date = idx
    anatomical = str(lt.loc[idx, 'anatomical']) if str(lt.loc[idx, 'anatomical']) != '[nan]' else None
    climate = str(lt.loc[idx, 'climate']) if str(lt.loc[idx, 'climate']) != '[nan]' else None
    hormonal = str(lt.loc[idx, 'hormonal']) if str(lt.loc[idx, 'hormonal']) != '[nan]' else None
    nutritional = str(lt.loc[idx, 'nutritional']) if str(lt.loc[idx, 'nutritional']) != '[nan]' else None
    social = str(lt.loc[idx, 'social']) if str(lt.loc[idx, 'social']) != '[nan]' else None

    with conn.cursor() as cur:
        cur.execute(lt_query, (anatomical, climate, hormonal, nutritional, social, date))
        conn.commit()

sleep = df.sleep

# print(sleep.REM.unique())

num_cols = ('%s, ' * 11) 

sleep_query = f'''INSERT INTO sleep (sleep, REM, awake, deep_sleep, light_sleep, sleep_score, insomnia, freq_wakes, sleep_meds, tz_change, date, user_id)
                VALUES ({num_cols} {uid_oi})'''

for idx in sleep.index: 
    date = idx
    sleep_ = float(sleep.loc[idx, 'sleep'])
    rem = 0.0 if str(sleep.loc[idx, 'REM'])=='nan' else 0.0 if float(sleep.loc[idx, 'REM'])== 0.0 else float(sleep.loc[idx, 'REM'])
    awake = 0.0 if str(sleep.loc[idx, 'awake'])=='nan' else float(sleep.loc[idx, 'awake'])
    deep_sleep = 0.0 if str(sleep.loc[idx, 'deep sleep'])=='nan' else float(sleep.loc[idx, 'deep sleep'])
    light_sleep = 0.0 if str(sleep.loc[idx, 'light sleep'])=='nan' else float(sleep.loc[idx, 'light sleep'])
    sleep_score = 0.0 if str(sleep.loc[idx, 'sleep score'])=='nan' else int(sleep.loc[idx, 'sleep score'])
    insomnia = bool(sleep.loc[idx, 'insomnia'])
    freq_wakes = bool(sleep.loc[idx, 'frequent wakeups'])
    sleep_meds = str(sleep.loc[idx, 'sleep medication']) if str(sleep.loc[idx, 'sleep medication']) != '[nan]' else None
    tz_change = bool(sleep.loc[idx, 'timezone change'])

    with conn.cursor() as cur:
        cur.execute(sleep_query, (sleep_, rem, awake, deep_sleep, light_sleep, sleep_score, insomnia, freq_wakes, sleep_meds, tz_change, date))
        conn.commit()

conn.close()
    
print('DONE')
 