"""
File with summary of options to be diplayed in data entry tabs

The information is stored in list form for each tab:
[{option_name:{"type":entry_field_type, "selection_menu":["selection 1","selection 2",..."selection n"]}},{option2...}, {option 3...}...{option n}]

The key "selection_menu" is empty or missing for Checkbutton type objects, as the only options here are On or Off

Possible entry field or button types include:
ttk.Checkbutton, tk.Listbox, ttk.Combobox, tttk.Spinbox
"""

mood_info = [
            {'angry':{"type":"Checkbox"}},
            {'anxious':{"type":"Checkbox"}},
            {'calm':{"type":"Checkbox"}}, 
            {'content':{"type":"Checkbox"}}, 
            {'depressed':{"type":"Checkbox"}}, 
            {'emotional':{"type":"Checkbox"}}, 
            {'energetic':{"type":"Checkbox"}}, 
            {'excited':{"type":"Checkbox"}}, 
            {'frustrated':{"type":"Checkbox"}}, 
            {'happy':{"type":"Checkbox"}}, 
            {'hyper':{"type":"Checkbox"}}, 
            {'moody':{"type":"Checkbox"}}, 
            {'motivated':{"type":"Checkbox"}}, 
            {'relaxed':{"type":"Checkbox"}}, 
            {'sad':{"type":"Checkbox"}}, 
            {'sensitive':{"type":"Checkbox"}}, 
            {'stressed':{"type":"Checkbox"}}, 
            {'tired':{"type":"Checkbox"}}
            ]

health_info = [
            {'RHR':{"type":"Spinbox", "from":30, "to":180, "increment":1}}, 
            {'acidity':{"type":"Checkbox"}}, 
            {'backpain':{"type":"Checkbox"}}, 
            {'bloating':{"type":"Checkbox"}}, 
            {'breakouts':{"type":"Checkbox"}}, 
            {'chestpain':{"type":"Checkbox"}}, 
            {'constipation':{"type":"Checkbox"}}, 
            {'defecation':{"type":"Checkbox"}}, 
            {'diarrhea':{"type":"Checkbox"}}, 
            {'dizziness':{"type":"Checkbox"}}, 
            {'hard stool':{"type":"Checkbox"}}, 
            {'headache':{"type":"Checkbox"}}, 
            {'indigestion':{"type":"Checkbox"}}, 
            {'medication':{"type":"Entryfield"}}, 
            {'nausea':{"type":"Checkbox"}}, 
            {'numbness':{"type":"Entryfield"}}, 
            {'other symptoms':{"type":"Entryfield"}}, 
            {'palpitations':{"type":"Checkbox"}}, 
            {'panic attack':{"type":"Checkbox"}}, 
            {'breathless':{"type":"Checkbox"}}, 
            {'sick?':{"type":"Entryfield"}}, 
            {'stomachpain':{"type":"Checkbox"}}
            ]

food_info = [
            {'animal products':{"type":"Entryfield"}}, 
            {'cereal':{"type":"Entryfield"}}, 
            {'cheats/sweets/unhealthy':{"type":"Entryfield"}}, 
            {'enough water?':{"type":"Checkbox"}}, 
            {'fruits':{"type":"Entryfield"}}, 
            {'healthy':{"type":"Checkbox"}}, 
            {'laxatives':{"type":"Entryfield"}}, 
            {'supplements':{"type":"Entryfield"}}, 
            ]

fitness_info = [
            {'cycling':{"type":"Spinbox", "from":0, "to":500, "increment":5}}, 
            {'gym':{"type":"Spinbox", "from":0, "to":500, "increment":5}}, 
            {'hiking':{"type":"Spinbox", "from":0, "to":500, "increment":5}}, 
            {'cardio':{"type":"Spinbox", "from":0, "to":500, "increment":5}}, 
            {'stretching':{"type":"Spinbox", "from":0, "to":500, "increment":5}}, 
            {'yoga':{"type":"Spinbox", "from":0, "to":500, "increment":5}}, 
            {'other':{"type":"Spinbox", "from":0, "to":500, "increment":5}}
            ]

period_info = [
            {'cramps':{"type":"MultipleChoice", "selection_menu":["mild", "medium", "strong", "extreme"]}}, 
            {'cycle day':{"type":"Spinbox", "from":1, "to":40, "increment":1}}, 
            {'infection':{"type":"Entryfield"}}, 
            {'ovulation':{"type":"Checkbox"}}, 
            {'period':{"type":"Checkbox"}}, 
            {'intercourse':{"type":"Checkbox"}}, 
            {'spotting':{"type":"MultipleChoice", "selection_menu":["light", "medium", "strong"]}}
            ]

longterm_info =[
            {'anatomical':{"type":"Entryfield"}}, 
            {'climate':{"type":"Entryfield"}}, 
            {'hormonal':{"type":"Entryfield"}}, 
            {'nutritional':{"type":"Entryfield"}}, 
            {'social':{"type":"Entryfield"}},
            ]

sleep_info = [
            {'sleep':{"type":"Spinbox", "from":0, "to":24, "increment":0.25}}, 
            {'REM':{"type":"Spinbox", "from":0, "to":1, "increment":0.01}}, 
            {'awake':{"type":"Spinbox", "from":0, "to":1, "increment":0.01}}, 
            {'deep sleep':{"type":"Spinbox", "from":0, "to":1, "increment":0.01}}, 
            {'frequent wakeups':{"type":"Checkbox"}}, 
            {'insomnia':{"type":"Checkbox"}}, 
            {'light sleep':{"type":"Spinbox", "from":0, "to":1, "increment":0.01}}, 
            {'sleep medication':{"type":"XXX"}}, 
            {'sleep score':{"type":"Spinbox", "from":10, "to":100, "increment":1}}, 
            {'timezone change':{"type":"Checkbox"}}
]