import sys
# import matplotlib.pyplot as plt
# from sklearn.metrics import precision_recall_curve, auc

allIdsValidated = set()
validationAnnotations = dict()
with open("bioProjectIds/Consensus Validation Labels - Sheet1.tsv", "r") as readFile:
    header = readFile.readline()
    for row in readFile:
        row = row.split("\t")
        allIdsValidated.add(row[0])
        if row[3] == "1":
            validationAnnotations[row[0]] = row[4].split(" ")
print(validationAnnotations)

machine1human0 = 0
machine1human0set = set()
machine1human1 = 0
machine0human1 = 0
machine0human1set = set()
machine0human0 = 0
ourLabeleingError = 0
numFound = 0
mac1hum0 = []
mac0hum1 = []
aggregate = []
precision = []
recall = []
f1 = []
mac1hum1 = []
checkThese = dict()
thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
ytrue = []
scores = []
for threshold in thresholds:
    machine1human0 = 0
    machine1human1 = 0
    machine0human1 = 0
    machine0human0 = 0
    ourLabeleingError = 0
    numFound = 0
    doubleCheckMe = set()
    #Race
    getscores = False
    if threshold == thresholds[-1]:
        getscores = True
    for filepath in [ "bioProjectIds/sexPredictionLabels.tsv"]: #"/bioProjectIds/racePredictionLabels.tsv",
        with open(filepath, "r") as readFile:
            header = readFile.readline()
            for line in readFile:
                line = line.rstrip("\n").split("\t")
                if line[0] in allIdsValidated:
                    if getscores:
                        if line[0] in validationAnnotations:
                            scores.append(float(line[2]))
                            if line[1] in validationAnnotations[line[0]]:
                                ytrue.append(1)
                            else:
                                ytrue.append(0)
                        else:
                            scores.append(float(line[2]))
                            ytrue.append(0)
                    numFound += 1
                    if float(line[2]) >= threshold:
                        if line[0] in validationAnnotations:
                            if line[1] in validationAnnotations[line[0]]:
                                machine1human1 += 1
                            else:
                                machine1human0 += 1
                                # doubleCheckMe.add((line[0], line[1]))
                        else:
                            machine1human0 += 1
                        #Machine thinks this is relevant
                    else:
                        if line[0] in validationAnnotations:
                            if line[1] in validationAnnotations[line[0]]:
                                machine0human1 += 1
                                doubleCheckMe.add((line[0], line[1]))
                            else:
                                machine0human0 += 1
                        else:
                            machine0human0 += 1

                        #Machine thinks this is not relevant
    checkThese[threshold] = doubleCheckMe
    mac1hum0.append(machine1human0)
    mac0hum1.append(machine0human1)
    mac1hum1.append(machine1human1)
    p = float(machine1human1) / float(machine1human1 + machine1human0)
    rec = float(machine1human1) / float(machine1human1 + machine0human1)
    print("RECALL", rec, machine1human1, machine0human1)
    precision.append(p)
    recall.append(rec)
    aggregate.append(machine1human0 + machine0human1)
    f1.append((p*rec / (p+rec)))
# print(machine0human0, machine1human1, machine1human0, machine0human1)
# print(numFound)
if numFound == (machine0human0 + machine1human1 + machine1human0 + machine0human1):
    print("Exact")
print(mac1hum0, mac0hum1)
print(precision)
for i in range(len(mac1hum0)):
    precision.append(float(mac1hum1[i]) / float(mac1hum1[i] + mac1hum0[i]))
print(precision)
print(recall)
# print(ytrue, scores)
# precis, reca, thresh = precision_recall_curve(ytrue, scores)
# auc_pr = auc(reca, precis)
# print(auc_pr)

# plt.plot(thresholds, precision, label='Precision', color='blue', linestyle='-', marker='o')
# plt.plot(thresholds, recall, label='Recall', color='red', linestyle='--', marker='x')
# plt.plot(thresholds, f1, label='F1', color='black', linestyle='-.', marker='+')

# plt.title('Errors by Threshold')
# plt.xlabel('Threshold for Classification as Relevant')
# plt.ylabel('Number of errors per 3000 datasets')

# # Showing legend
# plt.legend()
# plt.savefig("/results/errorVisualizationSex.png")
# # Display the chart
# plt.show()
# print(checkThese)