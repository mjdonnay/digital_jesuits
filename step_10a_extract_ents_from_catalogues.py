import spacy
import json

def load_data(file):
    with open(file, "r", encoding='utf-8') as f:
        data = json.load(f)
    return (data)

def write_data(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

#This function creates a dictionary of Jesuit/Residence pairs for a single year
def create_jesuit_dict(file):

    #Load most up to date spacy model
    nlp = spacy.load('dig_jes_ner_091421_2/model-best')

    #Open Catalogue_with_punct.json file and merge into text object
    with open(file, "r", encoding='utf-8') as f:
        data = json.load(f)
        text = '\n'.join(item["text"] for item in data)

    #Create document object with NLP model
    doc = nlp(text)

    #Create temporary list of Jesuits to add to
    temporary_jes_list = []

    #Pull year from top line of json file, save to first item of list
    temporary_jes_list.append(f'{data[0]["text"]} YEAR')

    #Iterate through entities in doc object, appending them as strings to temporary list
    for ent in doc.ents:
        # print(f'{ent.text} {ent.label_}')
        temp_string = f'{ent.text} {ent.label_}'
        # temp_string = temp_string.split(" ")
        temporary_jes_list.append(temp_string)

    #Print temporary list to check work
    #print(*temporary_jes_list, sep='\n')

    #Create temporary dictionary to add formatted Jesuits to
    temporary_jes_dict = {}

    #Create temporary name and residence list to add Jesuits to
    temporary_name_list = []
    temporary_resid_list = []

    #Create blank residence string - lives outside for loop so that it holds value until new value assigned
    resid = ""

    #List of residence terms to check against NLP produced residences
    locations = load_data('for_export/standard_resid_names.json')
    resid_codes = load_data('for_export/residence_codes.json')

    #Iterate through each Jesuit in the temporary list
    for item in temporary_jes_list:
        #Ignore: Define year as the first 4 characters from first item, ie. year of catalogue
        #year = f'{temporary_jes_list[0][0:5].strip(" ")}'
        #Create blank name string
        name = ''

        #Split each Jesuit in temporary list at " "
        item_split = item.split()

        #To assign name, check for , to indicate Last, First Middle and then rejoin in correct order
        if item_split[-1] == 'PERSON':
            if "," in item:
                name = f'{" ".join(item_split[1:-1]).title()} {item_split[0].strip(",")}'
                name = name.strip(",")
            else:
                name = f'{" ".join(item_split[0:-1]).title().strip(",")}'
                name = name.strip(",")

        #To assign residence, check last item in list and rejoin all elements of residence
        #Check residence against terms list from above to weed out mistakes from NLP model
        elif item_split[-1] == "RESID":
            resid_test = f'{" ".join(item_split[0:-1])}'
            #print(resid_test.lower())
            for location in locations:
                #print(location)
                #Don't include Ex Aliis Provinciis as residence for this b/c we want to avoid double counting Jesuits
                if location.lower() in resid_test.lower():
                    resid = locations[location].lower()
                    resid = resid.strip(",").strip(" ")
                    #print(resid)

        #If there is a name present in this iteration and the residence hasn't been assigned
        #that means it's from the first page. Assign it to residence "Provinicial"
        if resid == "":
            resid = 'provincial'
        #Don't append Ex Aliis Provinciis Jesuits to avoid double counting.
        if resid != "ex aliis provinciis in nostra degentes":
            #Catches error if Degentes Extra Provinciam gets assigned as a PERSON
            if name.lower() == 'degentes extra provinciam':
                resid = 'degentes extra provinciam'
            #Checks for a few common errors
            if name != "" and name != 'Degentes Extra Provinciam' and "socius" not in name.lower():
        #Update the temporary dictionary with formatted Jesuit in proper dictionary form
				#Add all of the years at once to allow easier replacement in "update" function
                temporary_jes_dict.update({name: {'1880': resid,
                                            '1881': 'na',
                                            '1882': 'na',
                                            '1883': 'na',
                                            '1884': 'na',
                                            '1885': 'na',
                                            '1886': 'na',
                                            '1887': 'na',
                                            '1888': 'na',
                                            '1889': 'na',
                                            '1890': 'na',
                                            '1915': 'na',
                                            '1916': 'na',
                                            '1917': 'na',
                                            '1918': 'na',
                                            '1919': 'na',
                                            '1920': 'na',
                                            '1921': 'na',
                                            '1922': 'na',
                                            '1923': 'na',
                                            '1924': 'na',
                                            '1925': 'na',
                                                  }})

    #Print final list to check work
    #print(*temporary_jes_dict, sep='\n')
    write_data(f'jesuit_dicts/jesuits_dictionary.json', temporary_jes_dict)
    
