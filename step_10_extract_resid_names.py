import json
import csv
import spacy
import pandas as pd

# Load JSON file
def load_data(file):
    with open(file, "r", encoding='utf-8') as f:
        data = json.load(f)
    return (data)

# Write JSON file
def write_data(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

# Create function that generates the list of residences for an indvidual catalogue
def gen_resid_list(file):

		#Open cleaned text file
    with open(file, "r", encoding='utf-8') as f:
        data = json.load(f)
        text = '\n'.join(item["text"] for item in data)

		# Open the existing list of residences
    master_resid_list = load_data('for_export/master_resid_list.json')

		# Create doc object from text file
    doc = nlp(text)

		# Creeate blank residence list and instantiate list of possible residence types
    resid_list = []
    locations = ['COLLEGIUM', 'collegium', 'Collegium', 'RESIDENTIA', 'residentia', 'Residentia', 'DOMUS', 'domus', 'Domus', 'ADDENDUM', 'addendum', 'Addendum', 'DEGENTES EXTRA', 'degentes extra', 'Degentes Extra', 'EX ALIIS', 'ex aliis', 'Ex Aliis', 'MUTANDA IN', 'mutanda in', 'Mutanda In', 'SCHOLA', 'schola', 'Schola']

		# For each entity, check if it contains a residence type (to avoid errors) and append to list
		# When running multiple years at once, un-comment line below to track progress
    print(f'{data[0]["text"]} YEAR')
    for ent in doc.ents:
        if ent.label_ == 'RESID':
            for location in locations:
                if location in ent.text:
                    ent_text = ent.text.replace('\n', ' ')
                    #print(f'{ent_text} {ent.label_}')
                    resid_list.append(ent_text)

    #Print to check work if needed
    #print(*resid_list, sep='\n')

		# For each residence in the individual catalogue, check if it's already in the master list
		# If it is not, add it
    for res in resid_list:
        if res in master_resid_list:
            pass
        else:
            master_resid_list.append(res)

		# Sort the list and then save the updated list to the master residence file
    master_resid_list.sort()

    #print(master_resid_list)
    write_data('for_export/master_resid_list_091421_2.json', master_resid_list)

#Create NLP model
nlp = spacy.load('dig_jes_ner_091421_2/model-best')

#Save initial blank list (Only need to do on first run - once the file exists you can comment this out)
master_resid_list = []
write_data('for_export/master_resid_list_091421_2.json', master_resid_list)

# Run through the 1880s and the 1915-1925, adding residences to master list
for i in range(80, 91):
    gen_resid_list(f'text_with_punct/Maryland_18{i}_with_punct.json')
for i in range(15, 26):
    gen_resid_list(f'text_with_punct/Maryland_19{i}_with_punct.json')

# Once completed, load file and print to check work
full_list = load_data('for_export/master_resid_list_091421_2.json')
print(*full_list, sep='\n')
print(len(full_list))

# Create a new list which is the lowercase version of the full master list
new_full_list = []
for item in full_list:
    item = item.lower()
    new_full_list.append(item)

#Print list to copy into CSV file for manual alignment
print("New Full List")
print(*new_full_list, sep='\n')
print(len(new_full_list))

#Copy list to CSV file
#Manually align residences in CSV file

#Import updated CSV file back into Python as dictionary & as list
residence_list = []
residence_dict = {}
residece_code_dict = {}

#Open CSV and append specific values from each row to the residence list and dict
with open('for_export/list_of_residences.csv', 'r') as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        if row[1] != "Value":
            residence_list.append(row[1])
            residence_list.append(row[0])
            temp_dict = {row[0]: row[1]}
            residence_dict.update(temp_dict)
            code_dict = {row[1]: row[2]}
            residece_code_dict.update(code_dict)

#Print to check work
residence_list = set(residence_list)
residence_list = sorted(residence_list)
print(*residence_list, sep='\n')
print(residence_dict)
#print(residece_code_dict)

#Translate into JSON file
#This file is to stanardize names
write_data('for_export/standard_resid_names.json', residence_dict)

#This file is to connect standard names with codes (didn't end up using)
write_data('for_export/residence_codes.json', residece_code_dict)
