import spacy
import json

def load_data(file):
    with open(file, "r", encoding='utf-8') as f:
        data = json.load(f)
    return (data)

# Load the spaCy model you prodiced in Step 8
nlp = spacy.load('dig_jes_090721_2/model-best')

#Create a blank text object and load the cleaned text from 1 catalogue into it
text = ''

with open('data/Maryland_1918.json', "r", encoding='utf-8') as f:
    data = json.load(f)
    text = '\n'.join(item["text"] for item in data)

# Create a doc object using the NLP model
doc = nlp(text)

# Print the year and the named entities for that doc
print(f'{data[0]["text"]} YEAR')
for ent in doc.ents:
    print(f'{ent.text} {ent.label_}')
