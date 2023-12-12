import pickle

# Characteristic №1: Measure how many nouns are in each bin of each world knowledge category
# e.g. rigidity has 5 categories (water,skin,leather/plastic,wood,metal) and this distribution {5,15,20,5,55}

wkcategories = ['masscount','phase','rigidity','sentience','size','weight']

# This stores nouns with their labels e.g. Teeth = masscount: CAR, phase: WOOD, rigidity: METAL, sentience: ROCK, size: BOOK-CAT, weight: BOOK-DUMBBELL
wkdictionary = {}

# Go over every world knowledge file
for i in wkcategories:
    wkname = "noun_bin_annotations/noun2" + i + ".p"
    with open(wkname, 'rb') as file:
        data = pickle.load(file)
        listy = {}

        # Go over every item in the file
        for item_noun, item_category in data.items():

            # Firstly, check for categories and count their labels
            if item_category not in listy:
                listy[item_category] = 1
            else:
                listy[item_category] += 1

            # Secondly, add nouns with their labels to the dictionary
            if item_noun not in wkdictionary:
                wkdictionary[item_noun] = {}
            if item_category not in wkdictionary[item_noun]:
                wkdictionary[item_noun][i] = item_category

        # Show all categories and label counts
        print(listy)
        # Percentage wise distribution
        total = sum(listy.values())
        x = 100/total
        listy = {y: round(listy[y]*x,2) for y in listy}
        print(listy)

# Characteristic №2: For each event, measure the difference of the world knowledge labels of the 2 nouns

# Iterate over dictionary and replace labels with numeric values

masscount_values = {'MILK': 1, 'SAND': 2, 'LEGOS': 3, 'CAR': 4}
phase_values = {'SMOKE': 1, 'MILK': 2, 'WOOD': 3}
rigidity_values = {'WATER': 1, 'SKIN': 2, 'LEATHER/PLASTIC': 3, 'WOOD': 4, 'METAL': 5}
sentience_values = {'ROCK': 1, 'TREE': 2, 'ANT': 3, 'CAT': 4, 'CHIMP': 5, 'MAN': 6}
size_values = {'-WATCH': 1, 'WATCH-BOOK': 2, 'BOOK-CAT': 3, 'CAT-PERSON': 4, 'PERSON-JEEP': 5, 'JEEP-STADIUM': 6, 'STADIUM-': 7}
weight_values = {'-WATCH': 1, 'WATCH-BOOK': 2, 'BOOK-DUMBBELL': 3, 'DUMBBELL-PERSON': 4, 'PERSON-JEEP': 5, 'JEEP-STADIUM': 6, 'STADIUM-': 7}

# Ugly repeating code due to time constraints
for noun, labels in wkdictionary.items():
    for label, value in labels.items():
        if label == "masscount":
            for tier, number in masscount_values.items():
                if value == tier:
                    labels[label] = number
        elif label == "phase":
            for tier, number in phase_values.items():
                if value == tier:
                    labels[label] = number
        elif label == "rigidity":
            for tier, number in rigidity_values.items():
                if value == tier:
                    labels[label] = number
        elif label == "sentience":
            for tier, number in sentience_values.items():
                if value == tier:
                    labels[label] = number
        elif label == "size":
            for tier, number in size_values.items():
                if value == tier:
                    labels[label] = number
        elif label == "weight":
            for tier, number in weight_values.items():
                if value == tier:
                    labels[label] = number

    #print(f"{noun}:{labels}")

# Read all events and get both nouns

aldif = {"masscount": {}, "phase": {}, "rigidity": {}, "sentience": {}, "size": {}, "weight": {}}
word_distribution = {}

types = ['pos','neg']
for i in types:
    event_file = i + "-all.txt"
    with open(event_file, 'r') as file:
        lines = file.readlines()
        count = 0
        for line in lines:
            count += 1
            if count != 1:
                event = line.strip().split()
                noun1 = event[0]
                noun2 = event[2]

                # Char 3: word distribution
                for word in event:
                    if word not in word_distribution:
                        word_distribution[word] = 1
                    else:
                        word_distribution[word] += 1
                
                event_difference = {}
                try:
                    for label in wkdictionary[noun1]:
                        try:
                            difference = wkdictionary[noun1][label] - wkdictionary[noun2][label]
                            event_difference[label] = difference
                            if difference not in aldif[label]:
                                aldif[label][difference] = 1
                            else:
                                aldif[label][difference] += 1
                        except:
                            pass
                except:
                    pass
    print(count)

# Sort
for i in aldif:
    aldif[i] = dict(sorted(aldif[i].items()))
for i in aldif.items():
    print(f"{i}")

# Percentage distribution
for i in aldif:
    total = sum(aldif[i].values())
    x = 100/total
    aldif[i] = {y: round(aldif[i][y]*x,2) for y in aldif[i]}
for i in aldif.items():
    print(f"{i}")

# sort word distro
word_distribution = dict(sorted(word_distribution.items(), key=lambda item: item[1]))
print(word_distribution)
listoid = {"rare":0,"infrequent":0,"average":0,"frequent":0,"very frequent":0}
for i in word_distribution:
    if word_distribution[i] < 5:
        listoid["rare"] += 1
    elif word_distribution[i] < 11:
        listoid["infrequent"] += 1
    elif word_distribution[i] < 25:
        listoid["average"] += 1
    elif word_distribution[i] < 51:
        listoid["frequent"] += 1
    elif word_distribution[i] >= 75:
        listoid["very frequent"] += 1
print(listoid)
