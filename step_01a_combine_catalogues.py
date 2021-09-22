import json

# This function makes loading data from existing JSON files easy
def load_data(file):
    with open(file, "r", encoding='utf-8') as f:
        data = json.load(f)
    return (data)

# This function makes writing data to a JSON file easy
def write_data(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

#Load files for specific dataset - add or remove additional as needed
file_1 = load_data('data/Maryland_1880.json')
file_2 = load_data('data/Maryland_1915.json')
file_3 = load_data('data/Maryland_1882.json')
#file_4 = load_data('data/Maryland_1915.json')
#file_5 = load_data('data/Maryland_1918.json')
#file_6 = load_data('data/Maryland_1917.json')

#Concatenate lists to create larger list - add additional as needed
new_text = file_1 + file_2 + file_3 
#+file_4 + file_5 + file_6

#Save new list as source file
write_data('sources/sourcefile_1.json', new_text)
