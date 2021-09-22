import json

#This function makes loading data from existing JSON files easy
def load_data(file):
    with open(file, "r", encoding='utf-8') as f:
        data = json.load(f)
    return (data)

#This function makes writing data to a JSON file easy
def write_data(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

#Make blank residences list
residences = []

#Import the residences from the text file into the list
with open('data/residence_list.txt', 'r', encoding='utf-8') as f:
    residences = f.read()
    residences = residences.lower()
    residences = residences.split('\n')

#print(*text, sep='\n')

#Create a blank patterns list
patterns = []

#For each of the individual residences:
for res in residences:
		#if residence exists
    if res != "":
				#split at the blank spaces to create a new list of each individual word
        res = res.split(' ')
				#create a temporary list into which the individual dictionaries will get added
        temp_list = []
				#for each word in the residence name, add that word to a dictionary in spacy
				#formatt and append that dictionary to the temporary list
        for word in res:
            temp_dict = {'LOWER': word}
            temp_list.append(temp_dict)
        #create a full pattern dictionary in spacy format for each residence
            pattern = {'label': 'RESID', 'pattern': temp_list}
        #append that dictionary to the patterns list
        patterns.append(pattern)

# Print full patterns list to check your work
print(*patterns, sep='\n')

#Save all of the patterns to a json file
write_data('data/resid_name_patterns.json', patterns)
