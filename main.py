### Import Space ###

from transformers import pipeline
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt
import csv
import ast
from numpy import sqrt, argmax

### Option Selection ###

# Choose dataset
print("Choose dataset: 1 = PEP, 2 = PAP")
choice_data = int(input())

# Choose whether to use knowledge augmentation
print("Do you want to use augmentation? 1 = No, 2 = Yes")
choice_aug = int(input())
if choice_aug == 2:
  aug_string = "augmented_"
  print("WARNING: YOU CHOSE TO AUGMENT THE EVENTS! THIS MIGHT TAKE LONGER TO CLASSIFY E.G. 2-3 MINUTES!")
else:
  aug_string = "simple_"

# Choose to use model or load saved inferences
print("Choose whether to use model: 1 = New inference, 2 = Load past inference (less time)")
choice_load = int(input())
if choice_load == 2:
  print("WARNING: CONDITIONS MUST BE THE SAME I.E. SAME DATA, MODEL, AUGMENTATION CHOICE!")

# Choose model
# See references for additional credits and source
print("Choose model: 1 = Porada, 2 = Quy")
choice_model = int(input())
if choice_model == 1:
  model_name = "ianporada/roberta_base_plausibility"
  monicker = "Porada"
  #labels = 0/1 = plausible/implausible
elif choice_model == 2:
  model_name = "nguyenhongquy/distilbert-base-uncased-semantic-plausibility"
  monicker = "Quy"
  #labels = PLAUSIBLE/IMPLAUSIBLE

### I. Get Data ###

# Read file to get test X (events i.e. SVO sentences) and test Y (validation i.e. 0/1 plausibility gold labels)
events = []
validation = []

if choice_data == 1:
  data_name = "pep"
else:
  data_name = "pap"

with open(data_name+"test.csv", mode ='r') as file:
  reader = csv.reader(file)
  next(reader)
  for line in reader:
        if data_name == "pep":

          event = line[1]
          gold = int(line[0])

          # If augmentation is on -> enrich line before adding it
          if choice_aug == 2:

            # Add world knowledge

            # Get SVO for easier event modification
            subject = event.split()[0]
            verb = event.split()[1]
            object = event.split()[2]

            replacements = {'masscount':'countable','phase':'solid','rigidity':'rigid',
                            'sentience':'sentient','size':'big','weight':'heavy'}

            # Use saved world knowledge
            with open("wknouns.txt", 'r') as file:
              wkdictionary = ast.literal_eval(file.read())

            # Describe subject and object using their world knowledge categories (if we have them)
            try:
              gotcha = wkdictionary[subject]
              event += f" / {subject} is"
              for category in gotcha:
                addition = f" as {replacements[category]} as {gotcha[category]},"
                event += addition
            except:
              pass
            try:
              gotcha = wkdictionary[object]
              event += f" / {object} is"
              for category in gotcha:
                addition = f" as {replacements[category]} as {gotcha[category]},"
                event += addition
            except:
              pass

          # Add concreteness (all of PEP is concrete)
            addition = f" / {subject} is concrete, {verb} is concrete, {object} is concrete"
            event += addition
            
          # Save line and gold label
          events.append(event)
          validation.append(gold)

        elif data_name == "pap":

          event = line[0]
          gold = int(line[2])

          # If augmentation is on -> enrich line before adding it
          if choice_aug == 2:

            # Get SVO for easier event modification
            subject = event.split()[0]
            verb = event.split()[1]
            object = event.split()[2]

            # Add concreteness using PAP data
            with open("papdata.tsv") as file:
              tsv_reader = csv.reader(file, delimiter="\t")
              next(tsv_reader)
              for tline in tsv_reader:
                if tline[0] == event:
                  concreteness = tline[2].split("-")
                  for i in range(len(concreteness)):
                    if concreteness[i] == "a":
                      concreteness[i] = "abstract"
                    elif concreteness[i] == "c":
                      concreteness[i] = "concrete"
                    elif concreteness[i] == "m":
                      concreteness[i] = "ambiguous"
                  #addition = f" / {subject} is {concreteness[0]}, {verb} is {concreteness[1]}, {object} is {concreteness[2]}"
                  addition = f" / the subject is {concreteness[0]}, the verb is {concreteness[1]}, the object is {concreteness[2]}"
                  event += addition

          # Save line and gold label
          events.append(event)
          validation.append(gold)

print("Got the events!")

### II. Get Predictions ###

# Either use model to get predictions and save results OR load results from previous prediction
if choice_load == 1:
  model = pipeline("text-classification", model=model_name)
  results = model(events)
  with open(model_name[:3] + "_" + aug_string + data_name + "_test.txt", "w") as file:
     file.write(str(results))
elif choice_load == 2:
  with open(model_name[:3] + "_" + aug_string + data_name + "_test.txt", 'r') as file:
    results = ast.literal_eval(file.read())

print("Got the predictions!")

### III. Evaluation of Model Predictions ###
    
# Initiate confusion matrix values with 1s to prevent calculation errors
evaluation = {"tp":1, "tn":1, "fp":1, "fn":1}
# Get all the wrongly classified events to use for the error analysis (need to print at end)
wrong_cases = []
# Used for ROC curve
probabilities = []

# Create confusion matrix
for id, result in enumerate(results):
    
    # Fix prediction scores because we focus on the positive label i.e. convert implausible labels to plausible by subtracting
    if result["label"] == "LABEL_1" or result["label"] == "IMPLAUSIBLE":
       result["score"] = 1 - result["score"]

    prob = float(result["score"])
    probabilities.append(prob)

    # Normalize prediction scores
    # IMPORTANT! You can change the classification threshold here according to the ROC curve
    if prob >= 0.5:
      prob = 1
    else:
      prob = 0

    # Counting for the confusion matrix
    if validation[id] == 1 and prob == validation[id]:
      evaluation["tp"] += 1
    elif validation[id] == 1 and prob != validation[id]:
      evaluation["fn"] += 1
      wrong_cases.append(f"{events[id]} {validation[id]} {prob}")
    elif validation[id] == 0 and prob == validation[id]:
      evaluation["tn"] += 1
    else:
      evaluation["fp"] += 1
      wrong_cases.append(f"{events[id]} {validation[id]} {prob}")

# Math using confusion matrix
      
pl_total = evaluation["tp"] + evaluation["fn"]
pl_prec = evaluation["tp"] / (evaluation["tp"]+evaluation["fp"])
pl_rec = evaluation["tp"] / (evaluation["tp"]+evaluation["fn"])
pl_f1 = (2 * pl_prec * pl_rec)/(pl_prec + pl_rec)

im_total = evaluation["tn"] + evaluation["fp"]
im_prec = evaluation["tn"] / (evaluation["tn"]+evaluation["fn"])
im_rec = evaluation["tn"] / (evaluation["tn"]+evaluation["fp"])
im_f1 = (2 * im_prec * im_rec)/(im_prec + im_rec)

acc = (evaluation["tp"] + evaluation["tn"]) / (pl_total + im_total)
plim_f1 = ( (pl_f1 * pl_total) + (im_f1 * im_total) ) / ( pl_total + im_total )

# Calculate ROC
# This and the threshold calculation were mostly taken from a machinelearningmastery.com article (see references in readme)
fpr, tpr, thresholds = roc_curve(validation, probabilities)

print("Got the evaluation!")

# Get the wrong events here
#for case in wrong_cases: print(case)

# Print/visualize evaluation

# Print confusion matrix
print(f"True Positive = {evaluation['tp']} / False Positive = {evaluation['fp']}")
print(f"False Negative = {evaluation['fn']} / True Negative = {evaluation['tn']}")
print(f"Total Plausible = {pl_total} / Total Implausible = {im_total}")
print(f"Combined/Macro F1 = {plim_f1} / Accuracy = {acc}")
print(f"Plausible F1 = {pl_f1} / Implausible F1 = {im_f1}")
print(f"Plausible Precision = {pl_prec} / Implausible Precision = {im_prec}")
print(f"Plausible Recall = {pl_rec} / Implausible Recall = {im_rec}")

# Print AUC
print(f"Area under ROC: {roc_auc_score(validation, probabilities)}")

# Print optimal threshold
gmeans = sqrt(tpr * (1-fpr))
ix = argmax(gmeans)
print('Best Threshold = %f / G-Mean = %.3f' % (thresholds[ix], gmeans[ix]))

# Visualize ROC
plt.plot(fpr, tpr, linestyle='--', label=monicker)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()
plt.show()
