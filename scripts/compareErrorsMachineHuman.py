import sys
# from sklearn.metrics import precision_recall_curve, auc
# import matplotlib.pyplot as plt

allIdsValidated = set()
validationAnnotations = dict()
with open("bioProjectIds/Consensus Validation Labels - Sheet1.tsv", "r") as readFile:
    header = readFile.readline()
    for row in readFile:
        row = row.rstrip().split("\t")
        allIdsValidated.add(row[0])
        if row[1] == "1":
            validationAnnotations[row[0]] = row[2].split(" ")
            print("yep")
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
mac1hum1 = []
mac0hum0 = []
aggregate = []
scores = []
ytrue = []
thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
for threshold in thresholds:
    machine1human0 = 0
    machine1human0set = set()
    machine1human1 = 0
    machine0human1 = 0
    machine0human1set = set()
    machine0human0 = 0
    ourLabeleingError = 0
    numFound = 0
    getscores = False
    if threshold == thresholds[-1]:
        getscores = True
    #Race
    with open("bioProjectIds/racePredictionLabels.tsv", "r") as readFile:
        header = readFile.readline()
        for line in readFile:
            line = line.rstrip("\n").split("\t")
            if line[0] in allIdsValidated:
                numFound += 1
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

                if float(line[2]) >= threshold:
                    if line[0] in validationAnnotations:
                        if line[1] in validationAnnotations[line[0]]:
                            machine1human1 += 1
                        else:
                            machine1human0 += 1
                            machine1human0set.add((line[0], line[1]))
                    else:
                        machine1human0 += 1
                    #Machine thinks this is relevant
                else:
                    if line[0] in validationAnnotations:
                        if line[1] in validationAnnotations[line[0]]:
                            machine0human1 += 1
                        else:
                            machine0human0 += 1
                    else:
                        machine0human0 += 1

                    #Machine thinks this is not relevant
    mac1hum0.append(machine1human0)
    mac0hum1.append(machine0human1)
    mac1hum1.append(machine1human1)
    mac0hum0.append(machine0human0)
    # if threshold == 0.5:
    #     rec = float(machine1human1) / float(machine1human1 + machine0human1)
    #     print("REC", rec)
    aggregate.append(machine1human0 + machine0human1)
# print(machine0human0, machine1human1, machine1human0, machine0human1)
# print(numFound)
if numFound == (machine0human0 + machine1human1 + machine1human0 + machine0human1):
    print("Exact")
precision = []
recall = []
for i in range(len(mac1hum0)):
    recall.append(float(mac1hum1[i]) / float(mac1hum1[i] + mac0hum1[i]))
    precision.append(float(mac1hum1[i]) / float(mac1hum1[i] + mac1hum0[i]))
print(recall, precision)
# for i in range(len(mac1hum0)):
#     print(recall[i] * precision[i])

# precis, reca, thresh = precision_recall_curve(ytrue, scores)
# auc_pr = auc(reca, precis)
# print(auc_pr)

# plt.plot(thresholds, mac0hum1, label='Machine 0 Human 1', color='blue', linestyle='-', marker='o')
# plt.plot(thresholds, mac1hum0, label='Machine 1 Human 0', color='red', linestyle='--', marker='x')
# plt.plot(thresholds, aggregate, label='Total errors', color='black', linestyle='-.', marker='+')

# plt.title('Errors by Threshold')
# plt.xlabel('Threshold for Classification as Relevant')
# plt.ylabel('Number of errors per 3000 datasets')

# # Showing legend
# plt.legend()
# plt.savefig("/results/errorVisualizationRace.png")
# # Display the chart
# plt.show()
# print(machine1human0set)