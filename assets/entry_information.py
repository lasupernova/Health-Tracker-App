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
            {'rhr':{"type":"Spinbox", "from":30, "to":180, "increment":1, "label":"RHR"}}, 
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
            {'medication':{"type":"Entryfield", "label":"medication"}}, 
            {'nausea':{"type":"Checkbox", "label":"nausea"}}, 
            {'numbness':{"type":"Entryfield", "label":"numbness"}}, 
            {'other_symptoms':{"type":"Entryfield", "label":"other symptoms"}}, 
            {'palpitations':{"type":"Checkbox", "label":"palpitations"}}, 
            {'panic_attack':{"type":"Checkbox", "label":"panic attack"}}, 
            {'breathless':{"type":"Checkbox", "label":"breathless"}}, 
            {'sick':{"type":"Entryfield", "label":"sick?"}}, 
            {'stomachpain':{"type":"Checkbox", "label":"stomachpain"}}
            ]

food_info = [
            {'animal_products':{"type":"Entryfield", "label":"animal products"}}, 
            {'cereal':{"type":"Entryfield", "label":"cereal"}}, 
            {'unhealthy_food':{"type":"Entryfield", "label":"cheats/sweets/unhealthy"}}, 
            {'enough_water':{"type":"Checkbox", "label":"enough water?"}}, 
            {'fruits':{"type":"Entryfield", "label":"fruits"}}, 
            {'healthy':{"type":"Checkbox", "label":"healthy"}}, 
            {'laxatives':{"type":"Entryfield", "label":"laxatives"}}, 
            {'supplements':{"type":"Entryfield", "label":"supplements"}}, 
            ]

fitness_info = [
            {'cycling':{"type":"Checkbox", "label":"cycling", "opens":"cycling_time"}}, 
            {'cycling_time':{"type":"Spinbox", "from":0, "to":500, "increment":5, "label":"cycling time", "on_demand":True}}, 
            {'gym':{"type":"Checkbox", "label":"gym", "opens":"gym_time"}},
            {'gym_time':{"type":"Spinbox", "from":0, "to":500, "increment":5, "label":"gym time", "on_demand":True}}, 
            {'cardio':{"type":"Checkbox", "label":"cardio", "opens":"cardio_time"}},
            {'cardio_time':{"type":"Spinbox", "from":0, "to":500, "increment":5, "label":"cardio time", "on_demand":True}}, 
            {'stretching':{"type":"Checkbox", "label":"stretching", "opens":"stretching_time"}},
            {'stretching_time':{"type":"Spinbox", "from":0, "to":500, "increment":5, "label":"stretching time", "on_demand":True}}, 
            {'yoga':{"type":"Checkbox", "label":"yoga", "opens":"yoga_time"}}, 
            {'yoga_time':{"type":"Spinbox", "from":0, "to":500, "increment":5, "label":"yoga_time", "on_demand":True}}, 
            {'other':{"type":"Checkbox", "label":"Other", "opens":"other_time"}}, 
            {'other_time':{"type":"Spinbox", "from":0, "to":500, "increment":5, "label":"other_time", "on_demand":True}}
            ]

period_info = [
            {'cramps':{"type":"Checkbox", "label":"cramps", "opens":"cramps_level"}}, 
            {'cramps_level':{"type":"MultipleChoice", "selection_menu":["mild", "medium", "strong", "extreme"], "label":"cramps level","on_demand":True}}, 
            {'cycle_day':{"type":"Spinbox", "from":1, "to":40, "increment":1, "label":"cycle day"}}, 
            {'infection':{"type":"Entryfield", "label":"infection"}}, 
            {'ovulation':{"type":"Checkbox", "label":"ovulation"}}, 
            {'period':{"type":"Checkbox", "label":"period"}}, 
            {'intercourse':{"type":"Checkbox", "label":"intercourse"}}, 
            {'spotting':{"type":"Checkbox", "label":"spotting", "opens":"spotting_level"}},
            {'spotting_level':{"type":"MultipleChoice", "selection_menu":["light", "medium", "strong"], "label":"spotting","on_demand":True}}
            ]

longterm_info =[
            {'anatomical':{"type":"Entryfield", "label":"anatomical"}}, 
            {'climate':{"type":"Entryfield", "label":"climate"}}, 
            {'hormonal':{"type":"Entryfield", "label":"hormonal"}}, 
            {'nutritional':{"type":"Entryfield", "label":"nutritional"}}, 
            {'social':{"type":"Entryfield", "label":"social"}},
            ]

sleep_info = [
            {'sleep':{"type":"Spinbox", "from":0, "to":24, "increment":0.25, "label":"sleep"}}, 
            {'rem':{"type":"Spinbox", "from":0, "to":1, "increment":0.01, "label":"REM"}}, 
            {'awake':{"type":"Spinbox", "from":0, "to":1, "increment":0.01, "label":"awake"}}, 
            {'deep_sleep':{"type":"Spinbox", "from":0, "to":1, "increment":0.01, "label":"deep sleep"}}, 
            {'freq_wakes':{"type":"Checkbox", "label":"frequent wakeups"}}, 
            {'insomnia':{"type":"Checkbox", "label":"insomnia"}}, 
            {'light_sleep':{"type":"Spinbox", "from":0, "to":1, "increment":0.01, "label":"light sleep"}}, 
            {'sleep_meds':{"type":"Entryfield", "label":"sleep medication"}}, 
            {'sleep_score':{"type":"Spinbox", "from":10, "to":100, "increment":1, "label":"sleep score"}}, 
            {'tz_change':{"type":"Checkbox", "label":"timezone change"}}
]