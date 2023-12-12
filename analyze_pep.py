import pickle
import csv

# Import Space #



### Characteristic №1: Overlap between dev/train/test set (SV, VO, SO combinations) ###

datasets = ['dev','train','test']
dictionary = {}

# Read all csv files and record all SV/VO/SO pairs
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
                # Split row i.e. event into nouns and verba and record the pairs
                event = row[1].split()
                noun1 = event[0]
                verb = event[1]
                noun2 = event[2]
                SVlist.append((noun1,verb))
                VOlist.append((verb,noun2))
                SOlist.append((noun1,noun2))
        dictionary[dataset] = [SVlist,VOlist,SOlist]

# WARNING: Ugly repeating code! This chunk repeats 6 times due to time constraints.

# Check Dev/Train overlap & Train/Dev overlap

overlap = []
for number, pair_list in enumerate(dictionary['dev']):
    for count, pair in enumerate(pair_list):
        try:
            if pair == dictionary['train'][number][count]:
                overlap.append(pair)
        except:
            pass
print(f"Dev/Train overlap count: {len(overlap)} / Overlap list: {overlap})")

overlap = []
for number, pair_list in enumerate(dictionary['train']):
    for count, pair in enumerate(pair_list):
        try:
            if pair == dictionary['dev'][number][count]:
                overlap.append(pair)
        except:
            pass
print(f"Train/Dev overlap count: {len(overlap)} / Overlap list: {overlap})")

# Check Train/Test overlap & Test/Train overlap

overlap = []
for number, pair_list in enumerate(dictionary['train']):
    for count, pair in enumerate(pair_list):
        try:
            if pair == dictionary['test'][number][count]:
                overlap.append(pair)
        except:
            pass
print(f"Train/Test overlap count: {len(overlap)} / Overlap list: {overlap})")

overlap = []
for number, pair_list in enumerate(dictionary['test']):
    for count, pair in enumerate(pair_list):
        try:
            if pair == dictionary['train'][number][count]:
                overlap.append(pair)
        except:
            pass
print(f"Test/Train overlap count: {len(overlap)} / Overlap list: {overlap})")

# Check Test/Dev overlap & Dev/Test overlap

overlap = []
for number, pair_list in enumerate(dictionary['test']):
    for count, pair in enumerate(pair_list):
        try:
            if pair == dictionary['dev'][number][count]:
                overlap.append(pair)
        except:
            pass
print(f"Test/Dev overlap count: {len(overlap)} / Overlap list: {overlap})")

overlap = []
for number, pair_list in enumerate(dictionary['dev']):
    for count, pair in enumerate(pair_list):
        try:
            if pair == dictionary['test'][number][count]:
                overlap.append(pair)
        except:
            pass
print(f"Dev/Test overlap count: {len(overlap)} / Overlap list: {overlap})")



### Characteristic №3: Measure how many nouns are in each bin of each world knowledge category ###
print("\n")

wkcategories = ['masscount','phase','rigidity','sentience','size','weight']

# This stores nouns with their labels e.g. Teeth = masscount: CAR, phase: WOOD, etc.
wkdictionary = {}

# Go over every world knowledge file
for category in wkcategories:
    wkname = "noun_bin_annotations/noun2" + category + ".p"
    with open(wkname, 'rb') as file:
        data = pickle.load(file)
        category_list = {}

        # Each file is about 1 category e.g. Size and consist of pairs of nouns with the label belonging to the category e.g. Jeep
        for item_noun, item_label in data.items():

            # Firstly, record categories and count their labels
            if item_label not in category_list:
                category_list[item_label] = 1
            else:
                category_list[item_label] += 1

            # Secondly, add nouns with their labels to the dictionary
            if item_noun not in wkdictionary:
                wkdictionary[item_noun] = {}
            if item_label not in wkdictionary[item_noun]:
                wkdictionary[item_noun][category] = item_label

        # Show all categories and label counts
        print(f"Countwise {category} distribution -> {category_list}")
        # Percentage wise distribution
        total = sum(category_list.values())
        x = 100/total
        category_list = {y: round(category_list[y]*x,2) for y in category_list}
        print(f"Percentagewise {category} distribution -> {category_list}\n")
        


### Characteristic №4: For each event, measure the difference of the world knowledge labels of the 2 nouns ###
### ALSO ###
### Characteristic №2: Measure representation of nouns and verbs ###
print("\n")

# First, we need to iterate over the wkdictionary and replace labels with numeric values

# Record all label numerical values
masscount_values = {'MILK': 1, 'SAND': 2, 'LEGOS': 3, 'CAR': 4}
phase_values = {'SMOKE': 1, 'MILK': 2, 'WOOD': 3}
rigidity_values = {'WATER': 1, 'SKIN': 2, 'LEATHER/PLASTIC': 3, 'WOOD': 4, 'METAL': 5}
sentience_values = {'ROCK': 1, 'TREE': 2, 'ANT': 3, 'CAT': 4, 'CHIMP': 5, 'MAN': 6}
size_values = {'-WATCH': 1, 'WATCH-BOOK': 2, 'BOOK-CAT': 3, 'CAT-PERSON': 4, 'PERSON-JEEP': 5, 'JEEP-STADIUM': 6, 'STADIUM-': 7}
weight_values = {'-WATCH': 1, 'WATCH-BOOK': 2, 'BOOK-DUMBBELL': 3, 'DUMBBELL-PERSON': 4, 'PERSON-JEEP': 5, 'JEEP-STADIUM': 6, 'STADIUM-': 7}

# Do the replacement here
# WARNING: Ugly repeating code due to time constraints!
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

# Second, we read all events and get both nouns
# We'll store differences here
alldif = {"masscount": {}, "phase": {}, "rigidity": {}, "sentience": {}, "size": {}, "weight": {}}

# Simultaneously, we can count word distribution for Characteristic №2
word_distribution = {}

# Read both all-pos.txt and neg-all.txt line by line
types = ['pos','neg']
for i in types:
    event_file = i + "-all.txt"
    with open(event_file, 'r') as file:
        lines = file.readlines()
        count = 0
        for line in lines:
            count += 1
            if count != 0:
                event = line.strip().split()
                noun1 = event[0]
                noun2 = event[2]

                # Characteristic №2 measure
                for word in event:
                    if word not in word_distribution:
                        word_distribution[word] = 1
                    else:
                        word_distribution[word] += 1
                # Characteristic №2 measure

                # Go over all world knowledge labels of a noun and compare them to the categories of the other noun
                event_difference = {}
                try:
                    for label in wkdictionary[noun1]:
                        try:
                            difference = wkdictionary[noun1][label] - wkdictionary[noun2][label]
                            event_difference[label] = difference
                            if difference not in alldif[label]:
                                alldif[label][difference] = 1
                            else:
                                alldif[label][difference] += 1
                        except:
                            pass
                except:
                    pass

# Sort alldif
for i in alldif:
    alldif[i] = dict(sorted(alldif[i].items()))
for i in alldif.items():
    print(f"Countwise difference distribution of {i}")

print("\n")
# Percentage distribution of alldif
for i in alldif:
    total = sum(alldif[i].values())
    x = 100/total
    alldif[i] = {y: round(alldif[i][y]*x,2) for y in alldif[i]}
for i in alldif.items():
    print(f"Percentagewise difference distribution of {i}")

# Sort word distribution (mostly used for better printing during testing)
word_distribution = dict(sorted(word_distribution.items(), key=lambda item: item[1]))

# Sort word distribution into categories
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
print("\n")
print("Word frequency categories: rare <5, infrequent <11, average <25, frequent <51, very frequent >=75")
print(f"Categorized word distribution: {listoid}")



### Characteristic №5 ###
print("\n")

# The code below was used to extract the first 50 nouns and give them default labels to cut some time from the manual annotation

# Store augmentations here
augment_dictionary = {}

# Get first 50 nouns
with open("noun_bin_annotations/noun2masscount.p", 'rb') as file:
    data = pickle.load(file)
    counter = 0
    for item_noun, item_label in data.items():
        counter += 1
        if counter <= 50:
            if item_noun not in augment_dictionary:
                augment_dictionary[item_noun] = ['rock','flower','mammal']

#for k,v in augment_dictionary.items():
#    print(f"{k} = {v}")

# Augmentation categories
# Edibility - mountain, rock, paper, coconut, strawberry, water
# Naturalness - moon, flower, hut, plastic, car, skyscraper 
# Hollowness - bubble, football, sponge, mammal, wood, iron

coach = ['rock', 'flower', 'mammal']
lace = ['paper', 'plastic', 'sponge']
rod = ['rock', 'plastic', 'iron']
tent = ['rock', 'hut', 'sponge']
skin = ['coconut', 'flower', 'mammal']
chair = ['rock', 'hut', 'wood']
dumbbell = ['rock', 'plastic', 'iron']
toothpick = ['paper', 'hut', 'wood']
milk = ['water', 'flower', 'sponge']
carpet = ['rock', 'hut', 'sponge']
trolley = ['mountain', 'car', 'football']
grape = ['strawberry', 'flower', 'sponge']
mallet = ['rock', 'hut', 'wood']
graph = ['paper', 'plastic', 'sponge']
nose = ['coconut', 'flower', 'mammal']
bike = ['mountain', 'plastic', 'iron']
gravel = ['rock', 'moon', 'iron']
woman = ['rock', 'flower', 'mammal']
string = ['paper', 'hut', 'sponge']
dollar = ['paper', 'plastic', 'sponge']
blanket = ['rock', 'plastic', 'sponge']
screwdriver = ['rock', 'plastic', 'iron']
spoon = ['rock', 'hut', 'iron']
legos = ['rock', 'plastic', 'sponge']
school = ['mountain', 'car', 'football']
cable = ['rock', 'car', 'sponge']
policeman = ['rock', 'flower', 'mammal']
brother = ['rock', 'flower', 'mammal']
gum = ['strawberry', 'plastic', 'sponge']
sand = ['paper', 'moon', 'sponge']
sidewalk = ['mountain', 'car', 'iron']
cookies = ['strawberry', 'hut', 'sponge']
fence = ['rock', 'hut', 'wood']
crow = ['coconut', 'flower', 'mammal']
sign = ['rock', 'hut', 'wood']
chef = ['rock', 'flower', 'mammal']
wife = ['rock', 'flower', 'mammal']
acid = ['water', 'flower', 'bubble']
panda = ['rock', 'flower', 'mammal']
sun = ['mountain', 'moon', 'sponge']
stool = ['rock', 'hut', 'wood']
net = ['rock', 'hut', 'sponge']
bird = ['coconut', 'flower', 'mammal']
body = ['rock', 'flower', 'mammal']
leg = ['coconut', 'flower', 'mammal']
kangaroo = ['rock', 'flower', 'mammal']
water = ['water', 'moon', 'sponge']
witch = ['rock', 'hut', 'mammal']
sink = ['mountain', 'plastic', 'wood']
pancake = ['strawberry', 'hut', 'sponge']


