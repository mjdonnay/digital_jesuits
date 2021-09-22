"""
NOTE: I did not use results from this Python program for my final analysis. Rather, 
I pulled them into Excel, removed schools that just appear in 1915-1925 and 
removed St. Joe's in Philadelphia (b/c it's % new in 1880s is off because 
it isn't present throughout the entire decade).
"""

import json
import csv
from collections import defaultdict
from statistics import mean


def load_data(file):
    with open(file, "r", encoding='utf-8') as f:
        data = json.load(f)
    return (data)


def write_data(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


# Load by_resid dictionary

by_resid_dict = load_data('jesuit_dicts/by_resid_dictionary.json')

# Create dict to store percent new Jesuits per year
## Structure -> {RESID: {YEAR: % New, YEAR: % New...}}
resid_perc_new = {}

# Iterate through each residence in the dictionary
for residence in by_resid_dict:
    # Limits residences to only academic institions within the borders of the province in the NE USA
    # Ignores Woodstock, Kingston
    if ("collegium" in residence and "collegium maximum woodstockiense" != residence \
        and "collegium kingstonense" != residence) or "schola" in residence:
        # If the residence satisfies those requirements, add it to the percent new Jesuits dict
        resid_perc_new.update({residence: {
            "1881": "",
            "1882": "",
            "1883": "",
            "1884": "",
            "1885": "",
            "1886": "",
            "1887": "",
            "1888": "",
            "1889": "",
            "1890": "",
            "1916": "",
            "1917": "",
            "1918": "",
            "1919": "",
            "1920": "",
            "1921": "",
            "1922": "",
            "1923": "",
            "1924": "",
            "1925": ""
        }})
        # For each year in the first decade, 1880s
        for i in range(81, 91):
            # Set the origin year and the year prior to that
            # Start with 1881 because we don't have 1879 in our dataset to compare
            # against 1880
            year_orig = f'18{i}'
            year_prev = f'18{i - 1}'
            # If there are Jesuits present in the residence during that year
            if by_resid_dict[residence][year_orig] != []:
                # Create two lists, one of the Jesuits there in the origin year
                # and one fo the Jesuits there the previous year
                list_1 = by_resid_dict[residence][year_prev]
                list_2 = by_resid_dict[residence][year_orig]
                # Create a new list that is the Jesuits who are at that resid
                # in the origin year, but not the previous year -> new Jesuits
                compare_list = list(set(list_2) - set(list_1))
                num_new = len(compare_list)
                # The percent of new Jesuits is number of new divided by the total number
                perc_new = float(num_new / len(list_2))
                # Add that percent of new Jesuits to the dictionary
                resid_perc_new[residence][year_orig] = perc_new

        # Do the same for the years 1916 through 1925
        for i in range(16, 26):
            # Set the origin year and the year prior to that
            # Start with 1916 because we don't have 1914 in our dataset to compare
            # against 1915
            year_orig = f'19{i}'
            year_prev = f'19{i - 1}'
            # If there are Jesuits present in the residence during that year
            if by_resid_dict[residence][year_orig] != []:
                # Create two lists, one of the Jesuits there in the origin year
                # and one fo the Jesuits there the previous year
                list_1 = by_resid_dict[residence][year_prev]
                list_2 = by_resid_dict[residence][year_orig]
                # Create a new list that is the Jesuits who are at that resid
                # in the origin year, but not the previous year -> new Jesuits
                compare_list = list(set(list_2) - set(list_1))
                num_new = len(compare_list)
                # The percent of new Jesuits is number of new divided by the total number
                perc_new = float(num_new / len(list_2))
                # Add that percent of new Jesuits to the dictionary
                resid_perc_new[residence][year_orig] = perc_new

# Save data to JSON file
# write_data('jesuit_dicts/percent_new_jesuits.json', resid_perc_new)

# Create a list to get average % new at each residence in each decade
avg_perc_new = {}
avg_perc_new = defaultdict(dict)

# Iterate through dict of perc new for 1880s
for residence in resid_perc_new:
    # print(residence)
    list_avgs = []
    for i in range(81, 91):
        year_orig = f'18{i}'
        year_prev = f'18{i - 1}'
        if resid_perc_new[residence][year_orig] != "":
            list_avgs.append(resid_perc_new[residence][year_orig])
    # print(list_avgs)
    if len(list_avgs) > 0:
        average = sum(list_avgs) / len(list_avgs)
        # print(average)
        avg_perc_new[residence]["1880s"] = average

# Iterate through dict of perc new for 1910s-1920s
for residence in resid_perc_new:
    # print(residence)
    list_avgs = []
    for i in range(16, 26):
        year_orig = f'19{i}'
        year_prev = f'19{i - 1}'
        if resid_perc_new[residence][year_orig] != "":
            list_avgs.append(resid_perc_new[residence][year_orig])
    # print(list_avgs)
    if len(list_avgs) > 0:
        average = sum(list_avgs) / len(list_avgs)
        # print(average)
        avg_perc_new[residence]["1910s"] = average

# Save to JSON file
write_data('jesuit_dicts/average_new_jesuits.json', avg_perc_new)
# print(avg_perc_new)
avg_perc_new = load_data('jesuit_dicts/average_new_jesuits.json')
print(avg_perc_new)
avg_perc_new.pop('collegium philadelphiense')

# Calculate the average percent new for each decade
average_1880s = []
average_1910s = []
for residence in avg_perc_new:
    if len(avg_perc_new[residence]) > 1:
        avg_1910s = avg_perc_new[residence]['1910s']
        average_1910s.append(avg_1910s)
        avg_1880s = avg_perc_new[residence]['1880s']
        average_1880s.append(avg_1880s)
    if len(avg_perc_new[residence]) == 1:
        avg_1910s = avg_perc_new[residence]['1910s']
        average_1910s.append(avg_1910s)

# Print the average % new Jesuits for each residence for each decade
print("Avg 1910s", average_1910s)
print("Avg 1880s", average_1880s)

# Take the average of % new Jesuits for all residences for each decade
# Figure out the difference
## NOTE: DID NOT USE these numbers for final analysis, instead focused on 8
## residences that I had good data on for both decades. See Excel sheet for these.
print("Average % new in 1880s: ", mean(average_1880s))
print("Average % new in 1910s: ", mean(average_1910s))
print("Change in % new from 1880s to 1910s: ", str(mean(average_1910s) - mean(average_1880s)))
