# To DO: check why list of dict (for order?) and change if it can be a dict of dicts instead

"""
File with summary of options to be diplayed in data entry tabs

The information is stored in list form for each tab:
[{option_name:{"type":entry_field_type, "selection_menu":["selection 1","selection 2",..."selection n"]}},{option2...}, {option 3...}...{option n}]

The key "selection_menu" is empty or missing for Checkbutton type objects, as the only options here are On or Off

Possible entry field or button types include:
ttk.Checkbutton, tk.Listbox, ttk.Combobox, tttk.Spinbox
"""

mood_info = [
            {'angry':{"type":"Checkbox", "label":"angry"}},
            {'anxious':{"type":"Checkbox", "label":"anxious"}},
            {'calm':{"type":"Checkbox", "label":"calm"}}, 
            {'content':{"type":"Checkbox", "label":"content"}}, 
            {'depressed':{"type":"Checkbox", "label":"depressed"}}, 
            {'emotional':{"type":"Checkbox", "label":"emotional"}}, 
            {'energetic':{"type":"Checkbox", "label":"energetic"}}, 
            {'excited':{"type":"Checkbox", "label":"excited"}}, 
            {'frustrated':{"type":"Checkbox", "label":"frustrated"}}, 
            {'happy':{"type":"Checkbox", "label":"happy"}}, 
            {'hyper':{"type":"Checkbox", "label":"hyper"}}, 
            {'moody':{"type":"Checkbox", "label":"moody"}}, 
            {'motivated':{"type":"Checkbox", "label":"motivated"}}, 
            {'relaxed':{"type":"Checkbox", "label":"relaxed"}}, 
            {'sad':{"type":"Checkbox", "label":"sad"}}, 
            {'sensitive':{"type":"Checkbox", "label":"sensitive"}}, 
            {'stressed':{"type":"Checkbox", "label":"stressed"}}, 
            {'tired':{"type":"Checkbox", "label":"tired"}}
            ]

health_info = [
            {'rhr':{"type":"Spinbox", "from":30, "to":180, "increment":1, "label":"RHR","message":"Select"}}, 
            {'acidity':{"type":"Checkbox", "label":"acidity"}}, 
            {'backpain':{"type":"Checkbox", "label":"backpain"}}, 
            {'bloating':{"type":"Checkbox", "label":"bloating"}}, 
            {'breakouts':{"type":"Checkbox", "label":"breakouts"}}, 
            {'chestpain':{"type":"Checkbox", "label":"chestpain"}}, 
            {'constipation':{"type":"Checkbox", "label":"constipation"}}, 
            {'defecation':{"type":"Checkbox", "label":"defecation"}}, 
            {'diarrhea':{"type":"Checkbox", "label":"diarrhea"}}, 
            {'dizziness':{"type":"Checkbox", "label":"dizziness"}}, 
            {'hard_stool':{"type":"Checkbox", "label":"hard stool"}}, 
            {'headache':{"type":"Checkbox", "label":"headache"}}, 
            {'indigestion':{"type":"Checkbox", "label":"indigestion"}}, 
            {'medication':{"type":"Checkbox", "label":"medication", "opens":"medication_type"}}, 
            {'medication_type':{"type":"Entryfield", "label":"medication", "on_demand":True}}, 
            {'nausea':{"type":"Checkbox", "label":"nausea"}}, 
            {'numbness':{"type":"Checkbox", "label":"numbness", "opens":"numbness_location"}}, 
            {'numbness_location':{"type":"Entryfield", "label":"numbness","on_demand":True,"message":"Where?"}}, 
            {'other':{"type":"Checkbox", "label":"Other Symptoms", "opens":"other_symptoms"}}, 
            {'other_symptoms':{"type":"Entryfield", "label":"other symptoms", "on_demand":True, "message":"Which?"}}, 
            {'palpitations':{"type":"Checkbox", "label":"palpitations"}}, 
            {'panic_attack':{"type":"Checkbox", "label":"panic attack"}}, 
            {'breathless':{"type":"Checkbox", "label":"breathless"}}, 
            {'sick':{"type":"Checkbox", "label":"sick?","opens":"sick_type"}}, 
            {'sick_type':{"type":"Entryfield", "label":"sick?","on_demand":True,"message":"Whats's wrong?"}}, 
            {'stomachpain':{"type":"Checkbox", "label":"stomachpain"}}
            ]

food_info = [
            {'animal_products':{"type":"Checkbox", "label":"Animal Products","opens":"animal_product_types"}}, 
            {'animal_product_types':{"type":"Entryfield", "label":"animal products","on_demand":True, "message":"Type and hit ENTER"}}, 
            {'cereal':{"type":"Checkbox", "label":"grains/seeds", "opens":"cereal_types"}}, 
            {'cereal_types':{"type":"Entryfield", "label":"gs_type","on_demand":True,"message":"Start typing grain or seed name..."}},
            {'unhealthy_food':{"type":"Checkbox", "label":"cheats/sweets/unhealthy","opens":"unhealthy_food_types"}}, 
            {'unhealthy_food_types':{"type":"Entryfield", "label":"cheats/sweets/unhealthy","on_demand":True,"message":"Ooops...what did you eat?"}}, 
            {'enough_water':{"type":"Checkbox", "label":"enough water?"}}, 
            {'fruits':{"type":"Checkbox", "label":"fruits", "opens":"fruit_types"}}, 
            {'fruit_types':{"type":"Entryfield", "label":"fruit_types", "on_demand":True,"message":"Start typing fruit name..."}}, 
            {'healthy':{"type":"Checkbox", "label":"healthy"}}, 
            {'laxatives':{"type":"Checkbox", "label":"laxatives","opens":"laxatives_types"}}, 
            {'laxatives_types':{"type":"Entryfield", "label":"laxatives","on_demand":True,"message":"Type and hit ENTER"}}, 
            {'supplements':{"type":"Checkbox", "label":"supplements","opens":"supplements_types"}}, 
            {'supplements_types':{"type":"Entryfield", "label":"supplements","on_demand":True}}
            ]

fitness_info = [
            {'cycling':{"type":"Checkbox", "label":"cycling", "opens":"cycling_time"}}, 
            {'cycling_time':{"type":"Spinbox", "from":0, "to":500, "increment":5, "label":"cycling time", "on_demand":True,"message":"mins"}}, 
            {'gym':{"type":"Checkbox", "label":"gym", "opens":"gym_time"}},
            {'gym_time':{"type":"Spinbox", "from":0, "to":500, "increment":5, "label":"gym time", "on_demand":True,"message":"mins"}}, 
            {'cardio':{"type":"Checkbox", "label":"cardio", "opens":"cardio_time"}},
            {'cardio_time':{"type":"Spinbox", "from":0, "to":500, "increment":5, "label":"cardio time", "on_demand":True,"message":"mins"}}, 
            {'stretching':{"type":"Checkbox", "label":"stretching", "opens":"stretching_time"}},
            {'stretching_time':{"type":"Spinbox", "from":0, "to":500, "increment":5, "label":"stretching time", "on_demand":True,"message":"mins"}}, 
            {'yoga':{"type":"Checkbox", "label":"yoga", "opens":"yoga_time"}}, 
            {'yoga_time':{"type":"Spinbox", "from":0, "to":500, "increment":5, "label":"yoga_time", "on_demand":True,"message":"mins"}}, 
            {'other':{"type":"Checkbox", "label":"Other", "opens":"other_time"}}, 
            {'other_time':{"type":"Spinbox", "from":0, "to":500, "increment":5, "label":"other_time", "on_demand":True,"message":"mins"}}
            ]

period_info = [
            {'cramps':{"type":"Checkbox", "label":"cramps", "opens":"cramps_level"}}, 
            {'cramps_level':{"type":"MultipleChoice", "selection_menu":["mild", "medium", "strong", "extreme"], "label":"cramps level","on_demand":True,"message":"Intensity"}}, 
            {'cycle_day':{"type":"Spinbox", "from":1, "to":40, "increment":1, "label":"cycle day", "message":"Select"}}, 
            {'infection':{"type":"Checkbox", "label":"infection","opens":"infection_type"}}, 
            {'infection_type':{"type":"Entryfield", "label":"infection","on_demand":True}}, 
            {'ovulation':{"type":"Checkbox", "label":"ovulation"}}, 
            {'period':{"type":"Checkbox", "label":"period"}}, 
            {'intercourse':{"type":"Checkbox", "label":"intercourse"}}, 
            {'spotting':{"type":"Checkbox", "label":"spotting", "opens":"spotting_level"}},
            {'spotting_level':{"type":"MultipleChoice", "selection_menu":["light", "medium", "strong"], "label":"spotting","on_demand":True,"message":"Intensity"}}
            ]

longterm_info =[
            {'anatomical':{"type":"Entryfield", "label":"anatomical", "message":"e.g. broken bones"}}, 
            {'climate':{"type":"Entryfield", "label":"climate", "message":"e.g. climate zone"}}, 
            {'hormonal':{"type":"Entryfield", "label":"hormonal", "message":"e.g. birth control"}}, 
            {'nutritional':{"type":"Entryfield", "label":"nutritional", "message":"e.g. vegan, paleo etc."}}, 
            {'social':{"type":"Entryfield", "label":"social", "message":"e.g. PhD, maternity leave"}},
            ]

sleep_info = [
            {'sleep':{"type":"Spinbox", "from":0, "to":24, "increment":0.25, "label":"sleep"}}, 
            {'rem':{"type":"Spinbox", "from":0, "to":1, "increment":0.01, "label":"REM"}}, 
            {'awake':{"type":"Spinbox", "from":0, "to":1, "increment":0.01, "label":"awake"}}, 
            {'deep_sleep':{"type":"Spinbox", "from":0, "to":1, "increment":0.01, "label":"deep sleep"}}, 
            {'freq_wakes':{"type":"Checkbox", "label":"frequent wakeups"}}, 
            {'insomnia':{"type":"Checkbox", "label":"insomnia"}}, 
            {'light_sleep':{"type":"Spinbox", "from":0, "to":1, "increment":0.01, "label":"light sleep"}}, 
            {'sleep_meds':{"type":"Checkbox", "label":"sleep medication","opens":"sleep_meds_types"}}, 
            {'sleep_meds_types':{"type":"Entryfield", "label":"sleep medication","on_demand":True}}, 
            {'sleep_score':{"type":"Spinbox", "from":10, "to":100, "increment":1, "label":"sleep score"}}, 
            {'tz_change':{"type":"Checkbox", "label":"timezone change"}}
]
