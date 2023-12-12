"""
The following code aims to analyze the PAP dataset.
Five characteristics were chosen to be analyzed and have been prepared for the next steps in the project.
Five functions analyze five different aspects.

"""

"""

The file has been opened and split through these two functions. 
This is how each line looks after splitting: 
['ability means mobility', 'plausible', 'a-m-a', '[2, 5, 4, 5, 5, 2, 5, 5, 5, 5]', '5', '[0.0, 20.0, 10.0, 70.0]', '1', '[80.0, 20.0]']

"""

from collections import Counter
import statistics
import ast
import csv


def open_file(file_path):
    # Open file
    with open(file_path, 'r') as file:
        # Show contents
        content = file.read()
        return content


def split_file_contents(content):
    # Split the content into lines
    lines = content.split('\n')
    result = []  # To store the elements

    for line in lines:
        # Split the line when tab is found
        elements = line.strip().split('\t')
        # print(elements)
        result.append(elements)
    return result


"""

1) The dataset provides abstractness combinations of a = abstract, m = mid-range, c = concrete for each triplet. 
The abstractness_combination function analyzes abstractness combinations and tries to answer the questions:
How many combinations of a-m-c are there in the dataset? Which is the most common? Which is the least common?
Outputs: 27 combinations, 'm-a-a' is the most common, 'm-m-a' is the least common. 

"""


def abstractness_combination(dataset):
    amc_combinations = []  # Here the different combinations will be stored
    for sublist in dataset:  # loop goes through each sublist of dataset
        if len(sublist) > 2 and sublist[2] != 'abstractness_combination':  # check len and exclude column title
            amc_combinations.append(sublist[2])  # Take elements in index 2 and group them
            # Output ex. ['a-m-a', 'a-c-m', 'a-m-a', 'a-c-m', 'a-c-m',...]
    # return amc_combinations

    # Used Counter method to count the occurrences of each combination
    combination_counts = Counter(amc_combinations)  # There are 27 combinations in total
    # print(len(combination_counts))

    # Rank the combinations in order of appearance using .most_common() method
    ranked_combinations = []  # start a list for ranking
    for combination in combination_counts:  # loop over every combination
        ranked_combinations = [combination_counts.most_common()]  # sort the list from the most common to the least
        # Output ex. [[('m-a-a', 72), ('c-m-m', 69), ('c-a-m', 69), ('c-c-c', 69), ('c-a-c', 68), ('c-m-a', 67),...]
    return ranked_combinations


"""

2) The average_distribution function averages the ratings provided by annotators. Ratings here refer to what extent
they considered the event plausible (5) or implausible (1). 
The function aims to provide insights on how plausible each event was perceived. 

"""


def average_distribution(dataset):
    ratings_average = []  # Here the ratings will be stored

    for sublist in dataset:  # loop goes through each sublist of dataset
        if len(sublist) > 3 and sublist[3] != 'rating':  # check len and exclude column title
            # Convert the string representation of a list to an actual list
            rating_values = ast.literal_eval(sublist[3])
            # Output ex. ['[2, 5, 4, 5, 5, 2, 5, 5, 5, 5]', '[5, 5, 5, 5, 4, 5, 5, 4]',...]']
        # return ratings

            # Calculate the mean of the numerical values for each sublist
            sublist_average = statistics.mean(rating_values)

            ratings_average.append(sublist_average)
            # Output ex. [4.3, 4.75, 3.888888888888889, 3.7, 3.5, 4.375, 3.888888888888889,...]
    return ratings_average


"""

3) The dataset presents original labels ('plausible' or 'implausible') serving as gold standard. 
The annotators voted 0 for implausibility and 1 for plausibility and the majority was assigned in the majority_binary section. 
'Unsure' denotes disagreement. 
The function labels_agreement explores the relations between the given standard and the binary setup from annotators. 
The goal is to answer the question: to what extent do the experimenters and the annotators agree?

"""


def labels_agreement(dataset):
    labels_lists = []  # List to store lists of corresponding standard and binary labels

    for sublist in dataset:
        if len(sublist) > 1 and sublist[1]!='original_label' :
            if len(sublist) > 6 and sublist[6]!='majority_binary':
                standard_label = sublist[1]
                binary_label = sublist[6]

                # Create a new list with standard and binary labels for each sublist
                labels_lists.append([standard_label, binary_label])
                # Output ex. [['plausible', '1'], ['implausible', 'unsure'], ['implausible', '0'], ...]]

    return labels_lists


"""

4) The dataset provides with three-element-events and the events_representation functions aims to the analysis of
the equality of representation for each noun/verb/noun in the events (subject, verb, object). 
Therefore, it aims to answer the question: is each noun/verb/noun represented equally in the events?

"""


def events_representation(dataset):
    events_split = []  # Here the split events will be stored

    for sublist in dataset:  # loop goes through each sublist of dataset
        if len(sublist) > 0 and sublist[0] != 'event':  # check len and exclude column title
            event = sublist[0]  # Take the event from the sublist
            split_event = event.split()  # Split the event into words
            events_split.append(split_event)
            # Output ex. [['ability', 'means', 'mobility'], ['ability', 'permits', 'multiplication'], ...]]

    # return events_split

    word_counts = {}
    for event in events_split:
        for position, word in enumerate(event):
            if position == 0:
                position_label = "SUBJ"
            elif position == 1:
                position_label = "VERB"
            else:
                position_label = "OBJ"

            # Use tuple (word, position) as key
            key = (word, position_label)
            # Update counts in the dictionary
            word_counts[key] = word_counts.get(key, 0) + 1
            # Output ex. {('ability', 'SUBJ'): 2, ('means', 'VERB'): 8, ('mobility', 'OBJ'): 3, ...}
    return word_counts


"""

5) The function check_overlap checks if overlap between dev/train/test set (SV, VO, SO combinations) occurs
in order to make sure that the dataset we will base the model on  performs well on unseen data. 
Output: 0 overlapping between the sets. 

"""


def check_overlap(data):

    datasets = ["dev",'train','test']
    dictionary = {}

    for dataset in datasets:
        dataset_file = dataset + ".csv"
        with open(dataset_file) as file:
            reader = csv.reader(file)
            SVlist = []
            VOlist = []
            SOlist = []
            counter = 0
            for row in reader:
                counter += 1
                # Skip header row
                if counter != 1:
                    event = row[0].split()
                    noun1 = event[0]
                    verb = event[1]
                    noun2 = event[2]
                    SVlist.append((noun1, verb))
                    VOlist.append((verb, noun2))
                    SOlist.append((noun1, noun2))
            dictionary[dataset] = [SVlist, VOlist, SOlist]

    # Dev/Train + Train/Dev

    overlap = []
    for number, pair_list in enumerate(dictionary['dev']):
        for count, pair in enumerate(pair_list):
            try:
                if pair == dictionary['train'][number][count]:
                    overlap.append(pair)
            except:
                pass
    print(f"Overlap count: {len(overlap)} / Overlap list: {overlap})")

    overlap = []
    for number, pair_list in enumerate(dictionary['train']):
        for count, pair in enumerate(pair_list):
            try:
                if pair == dictionary['dev'][number][count]:
                    overlap.append(pair)
            except:
                pass
    print(f"Overlap count: {len(overlap)} / Overlap list: {overlap})")

    # Train/Test + Test/Train

    overlap = []
    for number, pair_list in enumerate(dictionary['train']):
        for count, pair in enumerate(pair_list):
            try:
                if pair == dictionary['test'][number][count]:
                    overlap.append(pair)
            except:
                pass
    print(f"Overlap count: {len(overlap)} / Overlap list: {overlap})")

    overlap = []
    for number, pair_list in enumerate(dictionary['test']):
        for count, pair in enumerate(pair_list):
            try:
                if pair == dictionary['train'][number][count]:
                    overlap.append(pair)
            except:
                pass
    print(f"Overlap count: {len(overlap)} / Overlap list: {overlap})")

    # Test/Dev + Dev/Test

    overlap = []
    for number, pair_list in enumerate(dictionary['test']):
        for count, pair in enumerate(pair_list):
            try:
                if pair == dictionary['dev'][number][count]:
                    overlap.append(pair)
            except:
                pass
    print(f"Overlap count: {len(overlap)} / Overlap list: {overlap})")

    overlap = []
    for number, pair_list in enumerate(dictionary['dev']):
        for count, pair in enumerate(pair_list):
            try:
                if pair == dictionary['test'][number][count]:
                    overlap.append(pair)
            except:
                pass
    print(f"Overlap count: {len(overlap)} / Overlap list: {overlap})")
    return overlap


file_path = 'dataset.tsv'
file_content = open_file(file_path)
# print(split_file_contents(file_content))
dataset = split_file_contents(file_content)
# print(abstractness_combination(dataset))
# print(average_distribution(dataset))
# print(labels_agreement(dataset))
# print(events_representation(dataset))
# print(check_overlap(dataset))
