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
The following function analyzes abstractness combinations and tries to answer the questions:
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


file_path = 'dataset.tsv'
file_content = open_file(file_path)
# print(split_file_contents(file_content))
# dataset = split_file_contents(file_content)
# print(abstractness_combination(dataset))