def create_entry_fields(section):
    checklist = []
    sliders = []
    for entry in section:
        entry_name = [*entry][0]  #get param name
        entry_type = entry[entry_name]['type']
        entry_label = entry[entry_name]['label']

        if entry_type == 'Checkbox':
            checkbox = {'label':entry_label.capitalize(), 'value':entry_label}
            checklist.append(checkbox)
        elif entry_type == 'Spinbox':
            from_ = entry[entry_name]['from']
            to_ = entry[entry_name]['to']
            increment = entry[entry_name]['increment']
            slider = {'label':entry_label.capitalize(), 'min':from_, 'max':to_, 'step':increment}
            sliders.append(slider)
            if 'on_demand' in entry[entry_name].keys():
                on_demand = entry[entry_name]['on_demand']
        elif entry_type == 'Entryfield':
            pass
        elif entry_type == 'MultipleChoice':
            selection = entry[entry_name]['selection_menu']
            on_demand = entry[entry_name]['on_demand']

    return checklist, sliders