"""
This step is NOT necessary for the final workflow because I ended up 
using dictionaries, rather than pandas DataFrames, to analyze 
the data. I've kept this step here just so I can have the process saved.
"""

import json
import csv
import pandas as pd

def load_data(file):
    with open(file, "r", encoding='utf-8') as f:
        data = json.load(f)
    return (data)

def write_data(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

data = load_data('jesuit_dicts/jesuits_dictionary.json')

df = pd.DataFrame.from_dict({(i): data[i]
                           for i in data.keys()},
                       orient='index')
print(df)
df.to_csv('jesuit_dicts/jesuit_list.csv')
