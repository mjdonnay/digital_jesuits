import json
import csv

def load_data(file):
    with open(file, "r", encoding='utf-8') as f:
        data = json.load(f)
    return (data)

def write_data(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

## Structure -> {RESID: {1880: [LIST OF JESUITS], 1881: [LIST OF JESUITS] ... 1925: [LIST of JESUITS]}}

#Load existing Jesuit dictionary from file
jesuit_dict = load_data('jesuit_dicts/jesuits_dictionary.json')

#Create new "by residence" dictionary. Started with "provincial" because it was an easy test case.
by_resid_dict = {"provincial": {
        "1880": [],
        "1881": [],
        "1882": [],
        "1883": [],
        "1884": [],
        "1885": [],
        "1886": [],
        "1887": [],
        "1888": [],
        "1889": [],
        "1890": [],
        "1915": [],
        "1916": [],
        "1917": [],
        "1918": [],
        "1919": [],
        "1920": [],
        "1921": [],
        "1922": [],
        "1923": [],
        "1924": [],
        "1925": []
}}

#Iterate through existing Jesuit dictionary, adding Jesuit to residences
for jesuit in jesuit_dict:
    #Iterate through each year in the existing Jesuit dictionary for individual Jesuit
    for year in jesuit_dict[jesuit]:
        #For each year, check if the location of that Jesuit matches an existing residence
        #in the by_residence dictionary. If it does, add the Jesuit to the appropriate resid
        #for that year.
        if jesuit_dict[jesuit][year] in by_resid_dict:
            #If that residence exists, add that Jesuit to the appropriate year
            by_resid_dict[jesuit_dict[jesuit][year]][year].append(jesuit)
            #print(by_resid_dict[jesuit_dict[jesuit][year]][year], year)
        #If a Jesuit's location for a given year is not in the by_residence dictionary
        #already, add that residence with all years populated with blank lists and then
        #add the Jesuit to the appropriate year for that residence.
        if jesuit_dict[jesuit][year] not in by_resid_dict and jesuit_dict[jesuit][year] != "na":
            by_resid_dict.update({f'{jesuit_dict[jesuit][year]}': {
                                                                "1880": [], "1881": [], "1882": [],
                                                                "1883": [], "1884": [], "1885": [],
                                                                "1886": [], "1887": [], "1888": [],
                                                                "1889": [], "1890": [], "1915": [],
                                                                "1916": [], "1917": [], "1918": [],
                                                                "1919": [], "1920": [], "1921": [],
                                                                "1922": [], "1923": [], "1924": [],
                                                                "1925": []
                                                                }
                                  })
            by_resid_dict[jesuit_dict[jesuit][year]][year].append(jesuit)

#Print selection of by_resid dictionary to check work
print(by_resid_dict["collegium caesariense sancti petri"])

#Save by_resid dictionary to file
write_data('jesuit_dicts/by_resid_dictionary.json', by_resid_dict)

## Check why 1919 provincial list is so big! (note from original project)
