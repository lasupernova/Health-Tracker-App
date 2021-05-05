def create_entry_fields(section):
    checklist = []
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
        elif entry_type == 'Entryfield':
            pass
        elif entry_type == 'MultipleChoice':
            selection = entry[entry_name]['selection_menu']
            on_demand = entry[entry_name]['on_demand']

    return checklist