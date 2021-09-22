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

# Load both existing patterns files
names_patterns = load_data('data/jes_name_patterns.json')
residence_patterns = load_data('data/resid_name_patterns.json')

# Combine them into a new list
full_patterns = names_patterns + residence_patterns

#Save full_patterns in JSONL format
with open("sources/ner_patterns.json", 'w') as f:
    for pattern in full_patterns:
        f.write(json.dumps(pattern) + "\n")
