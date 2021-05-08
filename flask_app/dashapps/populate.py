from assets.entry_information import * 
from entry import create_entry_fields
import sys
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from entry import create_entry_fields
from assets.entry_information import * 
from assets.grains_seeds import g_and_s
from assets.fruits import fruits


entry_info = {'mood':mood_info, 'health':health_info, 'food':food_info, 
              'fitness': fitness_info, 'period':period_info, 'sleep':sleep_info, 'longterm':longterm_info}


def create_non_entry(category_dict, entry_name):
    """
    Returns dict with info of entry 'to open'
    """
    return [entry for entry in category_dict if entry_name in entry.keys()][0]


def create_dcc_obj_by_type(entry_dict, called_by=None ,on_demand=False):
    """
    Creates dcc entry object based on type given in passed entry_dict
    """
    entry_name = list(entry_dict.keys())[0]
    entry_dict = entry_dict[entry_name]
    entry_type = entry_dict['type']
    entry_label = entry_dict['label']
    id_label = called_by
    child_list = []  
    if on_demand:
        id_ = {"name":id_label, "type":"on_demand"}
    else:
        id_ = {"name":entry_name, "type":"permanent"}
        label_ = html.Label([entry_label])  #add label to non-on_demand entries in order to identify them
        child_list.append(label_)
    if entry_type == 'Spinbox':
        min_= entry_dict['from']
        max_ = entry_dict['to']
        step = entry_dict['increment']
        to_open = dcc.Input(id=id_, type="number", min=min_, max=max_, step=step)
    elif entry_type == 'Entryfield':
        if entry_label == "grains/seeds":
            opts = [{'label':item.capitalize(), 'value':item} for item in g_and_s]  #convert from list to list of dicts with form [{'label1':x, 'value1':y},...]
            to_open = dcc.Dropdown(id=id_, options=opts,
                                    placeholder='Start typing a grain or seed name...',
                                    multi=True)
        elif entry_label == "fruits":
            opts = [{'label':item.capitalize(), 'value':item} for item in fruits]
            to_open = dcc.Dropdown(id=id_, options=opts,
                                    placeholder='Start typing a fruit name...',
                                    multi=True)
        else:
            to_open = dcc.Input(id=id_, type='text')
    elif entry_type == 'MultipleChoice':
            selection = [{'label':item, 'value':item} for item in entry_dict['selection_menu']]
            to_open = dcc.Dropdown(id=id_, options=selection,
                                    placeholder='Select...',
                                    multi=False)

    child_list.append(to_open)
    # wrap in html.Div in order to have every entry on separate line
    div = html.Div(child_list)

    return div 

def create_first_col_children(category_dict):
    dcc_obj_list = []
    for entry in category_dict:
        entry_name = [*entry][0]
        entry_label = entry[entry_name]['label'] 
        if entry[entry_name]['type'] == 'Checkbox':
            if 'opens' in entry[entry_name].keys():
                checkbox = dcc.Checklist(id={"name":entry_name,"type":"check_toggle"}, options=[{'label':entry_label,'value':entry_name}], value=[])
                opens = entry[entry_name]['opens'] 
                to_open = create_non_entry(category_dict, opens)
                to_open = create_dcc_obj_by_type(to_open, entry_name, on_demand=True)
                div = html.Div([
                                html.Div([checkbox],style={'margin-right':'5px', 'display':'inline-block'}), 
                                html.Div(id={"name":entry_name,"type":"div"}, children=[to_open],style={'display': 'none', 'width':'30%'})
                                ])
                # print(f"\tCheckbox: {div}")  ##uncomment for troubleshooting   
            else:
                div = dcc.Checklist(id={"name":entry_name,"type":"check"}, options=[{'label':entry_label,'value':entry_name}], value=[])
                # print(f'\tCheckbox: {div}')  ##uncomment for troubleshooting
        else:
            if 'on_demand' in entry[entry_name].keys():
                continue
                # print(f'\t\tON DEMAND SETTING: {entry_name}')  ##uncomment for troubleshooting
            else:
                div = create_dcc_obj_by_type(entry)
                # print('\t', div)  ##uncomment for troubleshooting
        dcc_obj_list.append(div)
    return dcc_obj_list

def return_full_entrytab(category):
    return_val = create_first_col_children(category)
    return dbc.Row([dbc.Col(return_val, width = 4), dbc.Col([html.Div("Col 2", style={'backgroundColor': 'pink'})], width = 8)])


