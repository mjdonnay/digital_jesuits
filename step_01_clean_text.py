import requests
import json
import re

# This function makes loading data from existing JSON files easy
def load_data(file):
    with open(file, "r", encoding='utf-8') as f:
        data = json.load(f)
    return (data)

# This function makes writing data to a JSON file easy
def write_data(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

#I inititally tried a number of different ways of processing these text files
#Ultimately, I decided that splitting them at the page break and retaining the commas and
#periods produced the best results for NER when using prodigy.

#This function splits text files by pages, but retains periods and commas
def gen_clean_with_punct(file, province_and_year):
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
        text = text.replace("\n\n\n", "\n\n")
        text = text.split('\n\n')
        #text = re.split('(?<!ET )(COLLEGIUM|RESIDENTIA|DOMUS|ADDENDUM|DEGENTES EXTRA|EX ALIIS|IN STATU|MUTANDA IN)',
                        #text)

    temp_catalogue = []
    locations = ['COLLEGIUM', 'RESIDENTIA', 'DOMUS', 'ADDENDUM', 'DEGENTES EXTRA', 'EX ALIIS', 'MUTANDA IN']

		#This strips leading/trailing spaces, replaces internal line breaks with spaces and removes most punctuation
		#Then it reformats some of the specific issues known to occur with the catalogues
    for segment in text:
        segment = segment.strip()
        segment = segment.replace("\n", " ")

        punc = '''!()-[]—{}–;:“"\<>/?@#$%^&*_~'''
        for ele in segment:
            if ele in punc:
                segment = segment.replace(ele, " ")

        segment = re.sub('\s+', ' ', segment)
        segment = segment.replace("B V M", "BVM")
        segment = segment.replace("¬", "")
        segment = segment.replace("ü", "u").replace('ο', "o").replace('è', 'e').replace('é', 'e').replace('ö', 'o')

				#Once each segment has been cleaned, it is appended to the temporary list
        if segment != "":
            temp_catalogue.append(segment)

    catalogue_list = []

		#This section checks to make sure each segment has text and if it does, appends it to the final list and saves
		#that list to a JSON file
    for sent in temp_catalogue:
        if sent != "":
            dict_ent = {"text": sent}
            catalogue_list.append(dict_ent)
    print(*catalogue_list, sep='\n')
    write_data(f'text_with_punct/{province_and_year}_with_punct.json', catalogue_list)


#Run function on each individual text file
gen_clean_with_punct('data/Maryland_1880.txt', 'Maryland_1880')
