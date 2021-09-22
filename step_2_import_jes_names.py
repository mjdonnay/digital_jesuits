import json
import re
import csv

# This function makes loading data from existing JSON files easy
def load_data(file):
    with open(file, "r", encoding='utf-8') as f:
        data = json.load(f)
    return (data)

# This function makes writing data to a JSON file easy
def write_data(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

# Open the CSV file with initial Jesuit names saved
filename = open('data/jesuit_names_update_2.csv')

# use DictReader to create file object
file = csv.DictReader(filename)

# create empty lists for first, middle, and last names
first_names = []
middle_names = []
last_names = []

# iterate over each row and append values to empty list
# First, Middle, Last indicates the label at the top of the column
for row in file:
    first_names.append(row['First'])
    middle_names.append(row['Middle'])
    last_names.append(row['Last'])

# Print the length of each list to ensure they are equal
print(len(first_names))
print(len(middle_names))
print(len(last_names))

# Create new lists for clean names
first_names_cl = []
middle_names_cl = []
last_names_cl = []

# For each list, replace weird stop symbol, make all letters lowercased, 
# and strip the extra spaces out. Then append that name to the list of 
# cleaned names.
for name in first_names:
    name = name.replace(u'\xa0', '')
    name = name.lower()
    name = name.strip()
    first_names_cl.append(name)

for name in last_names:
    name = name.replace(u'\xa0', '')
    name = name.lower()
    name = name.strip()
    last_names_cl.append(name)

for name in middle_names:
    name = name.replace(u'\xa0', '')
    name = name.lower()
    name = name.strip()
    middle_names_cl.append(name)

# Create an empty patterns list, which will ultimately be the data saved to
# JSON file at the end of this program.
patterns = []

# Iterate through each list of names at the same rate to combine together
i = 0
for i in range(len(first_names_cl)):
    # Create id for pattern by combining all 3 lists
    id = first_names_cl[i] + " " + middle_names_cl[i] + " " + last_names_cl[i]
    # Replace any extra spaces with a single space
    id = re.sub("\s+", " ", id)
    # Create temporary lists for each type of name, which will get the split
    # names appended to them further down.
    temp_list_first = []
    temp_list_middle = []
    temp_list_last = []
    if first_names_cl[i] != "":
        # Split first name into individual names
        first_name = first_names_cl[i].split(" ")
        # For each word in the name, put it in spaCy format and append to list
        for word in first_name:
            temp_dict_first = {'LOWER': word}
            temp_list_first.append(temp_dict_first)
        # Split middle name into individual names (if any)
        middle_name = middle_names_cl[i].split(" ")
        # For each word in the name, put it in spaCy format and append to list
        for word in middle_name:
            # Only create middle name in spaCy format if there is a middle name,
            # otherwise skip it.
            if word != "":
                temp_dict_middle = {'LOWER': word}
                temp_list_middle.append(temp_dict_middle)
            # Split last name into individual names
        last_name = last_names_cl[i].split(" ")
        # For each word in the name, put it in spaCy format and append to list
        for word in last_name:
            temp_dict_last = {'LOWER': word}
            temp_list_last.append(temp_dict_last)

    # Create two new lists by combining all of the temporary lists
    # The first is the order "FIRST MIDDLE LAST"
    # The second is the order "LAST FIRST MIDDLE"
    full_name_fml = temp_list_first + temp_list_middle + temp_list_last
    full_name_lfm = temp_list_last + temp_list_first + temp_list_middle

    # Put each of the full names into the spaCy format, with the id
    pattern_1 = {'label': 'PERSON', 'pattern': full_name_fml, "id": id}
    pattern_2 = {'label': 'PERSON', 'pattern': full_name_lfm, "id": id}

    # Append both of those patterns to the original patterns list
    patterns.append(pattern_1)
    patterns.append(pattern_2)

# Print the full patterns list to check your work.
print(*patterns, sep='\n')

# Save the data as JSON file to use later in the process
write_data('data/jes_name_patterns.json', patterns)
