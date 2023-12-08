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


file_path = 'dataset.tsv'
file_content = open_file(file_path)
print(split_file_contents(file_content))

"""
1) The dataset provides abstractness combinations of a = abstract, m = mid-range, c = concrete for each triplet. 
The following function analyzes abstractness combinations and tries to answer the questions:
how many combinations of a-m-c are there in the dataset? Which are more common? Which are less common?

"""


def abstractness_combination():

    pass
