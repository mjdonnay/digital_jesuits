import json
import csv
from collections import defaultdict
from statistics import mean
from statistics import median_grouped
from statistics import median

def load_data(file):
    with open(file, "r", encoding='utf-8') as f:
        data = json.load(f)
    return (data)

def write_data(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

#Load by_resid dictionary

by_resid_dict = load_data('jesuit_dicts/by_resid_dictionary.json')

#Create dictionary to store average durations
total_durations_1880s = defaultdict(dict)
total_durations_1910s = defaultdict(dict)

for residence in by_resid_dict:
    #Creates temporary list of Jesuits for each residence
    temp_jes_list = []

    # Limits residences to only academic institions within the borders of the province in the NE USA
    # Ignores Woodstock, Kingston
    if ("collegium" in residence and "collegium maximum woodstockiense" != residence \
        and "collegium kingstonense" != residence) or "schola" in residence:

        for i in range(81, 91):
            # Set the origin year and the year prior to that
            # Start with 1881 because we don't have 1879 in our dataset to compare
            # against 1880
            year = f'18{i}'
            for name in by_resid_dict[residence][year]:
                temp_jes_list.append(name)
                temp_jes_list = list(set(temp_jes_list))
        #print(residence, temp_jes_list)

        #Create a temporary list to hold list of durations
        duration_list = []

        for jesuit in temp_jes_list:
            # For each year in the first decade, 1880s
            count = 1
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
                    #If a Jesuit is there in both the origin year and the previous year, add to count
                    if jesuit in list_1 and jesuit in list_2:
                        ####I think this is an imperfect counting method that might not account
                        #for people leaving and then coming back. Confirm this when revising for
                        #publication###
                        count += 1
            #print(jesuit, count, residence, year_orig)
            duration_list.append(count)

        #print(duration_list)
        #print(f'# of durations: {len(duration_list)}')
        #print(f'# of Jesuits in resid: {len(temp_jes_list)}')

        total_durations_1880s[residence] = duration_list

#print(total_durations_1880s)

#Create dictionary of average durations at each residence
avg_duration_1880s = {}

for residence in total_durations_1880s:
    if residence != "collegium philadelphiense":
        durations = total_durations_1880s[residence]

        #Removed durations of just 1 year to remove noise
        if durations != []:
            while 1 in durations:
                durations.remove(1)
            #print("cleaned", durations)
            median_duration = median_grouped(durations)
            #print(residence, "median_cleaned", median_duration)
            avg_duration_1880s[residence] = median_duration

print("1880s", avg_duration_1880s)

## Doing for 1910s ##

for residence in by_resid_dict:
    #Creates temporary list of Jesuits for each residence
    temp_jes_list = []

    # Limits residences to only academic institions within the borders of the province in the NE USA
    # Ignores Woodstock, Kingston
    if ("collegium" in residence and "collegium maximum woodstockiense" != residence \
        and "collegium kingstonense" != residence) or "schola" in residence:

        for i in range(16, 26):
            # Set the origin year and the year prior to that
            # Start with 1881 because we don't have 1879 in our dataset to compare
            # against 1880
            year = f'19{i}'
            for name in by_resid_dict[residence][year]:
                temp_jes_list.append(name)
                temp_jes_list = list(set(temp_jes_list))
        #print(residence, temp_jes_list)

        #Create a temporary list to hold list of durations
        duration_list = []

        for jesuit in temp_jes_list:
            # For each year in the first decade, 1880s
            count = 1
            for i in range(16, 26):
                # Set the origin year and the year prior to that
                # Start with 1881 because we don't have 1879 in our dataset to compare
                # against 1880
                year_orig = f'19{i}'
                year_prev = f'19{i - 1}'
                # If there are Jesuits present in the residence during that year
                if by_resid_dict[residence][year_orig] != []:
                    # Create two lists, one of the Jesuits there in the origin year
                    # and one fo the Jesuits there the previous year
                    list_1 = by_resid_dict[residence][year_prev]
                    list_2 = by_resid_dict[residence][year_orig]
                    #If a Jesuit is there in both the origin year and the previous year, add to count
                    if jesuit in list_1 and jesuit in list_2:
                        count += 1
            #print(jesuit, count, residence, year_orig)
            duration_list.append(count)

        #print(duration_list)
        #print(f'# of durations: {len(duration_list)}')
        #print(f'# of Jesuits in resid: {len(temp_jes_list)}')

        total_durations_1910s[residence] = duration_list

#print(total_durations_1880s)

#Create dictionary of average durations at each residence
avg_duration_1910s = {}

for residence in total_durations_1910s:
    if residence != "collegium philadelphiense":
        durations = total_durations_1910s[residence]

        #Removed durations of just 1 year to remove noise
        if durations != []:
            while 1 in durations:
                durations.remove(1)
            #print("cleaned", durations)
            median_duration = median_grouped(durations)
            #print(residence, "median_cleaned", median_duration)
            avg_duration_1910s[residence] = median_duration

print("1910s/1920s", avg_duration_1910s)

# Print the individual residence medians for the 1880s
median_1880s = avg_duration_1880s.values()
print(median_1880s)
# Print the median for the province as a whole during that decade
print("Median 1880s", median_grouped(median_1880s))

# Print the individual residence medians for the 1915-1925 decade
median_1910s = avg_duration_1910s.values()
print(median_1910s)
# Print the median for the province as a whole during that decade
print("Median 1910s", median_grouped(median_1910s))

# Print the difference between the 2 decades 
print("Change in median duration: ", str(median_grouped(median_1910s) - median_grouped(median_1880s)))
