### Import Space ###

import pickle

### Extraction ###
# Run this to save a dictionary with all nouns and their world knowledge features from the files in noun_bin_annotations

wkcategories = ['masscount','phase','rigidity','sentience','size','weight']

# This stores the nouns and their labels e.g. 'coach': {'masscount': 'CAR', 'phase': 'WOOD', 'rigidity': 'SKIN', 'sentience': 'MAN', 'size': 'CAT-PERSON', 'weight': 'DUMBBELL-PERSON'}
wkdictionary = {}

# Go over every world knowledge file
for category in wkcategories:
    wkname = "noun_bin_annotations/noun2" + category + ".p"
    with open(wkname, 'rb') as file:
        data = pickle.load(file)

        # Each file consists of pairs of nouns with the label belonging to the category e.g. Jeep
        for item_noun, item_label in data.items():

            # Add nouns and labels to the dictionary
            if item_noun not in wkdictionary:
                wkdictionary[item_noun] = {}
            if item_label not in wkdictionary[item_noun]:
                wkdictionary[item_noun][category] = item_label

# Store dictionary as a file
with open("wknouns.txt", "w") as file:
    file.write(str(wkdictionary))