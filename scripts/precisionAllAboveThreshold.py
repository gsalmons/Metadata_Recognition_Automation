import matplotlib.pyplot as plt

toVisualize = dict()
thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
for grouping in ["race", "sex", "tumor_stage"]:
    if grouping == "race":
        filePath = "/bioProjectIds/racePredictionLabels.tsv"
    elif grouping == "sex":
        filePath = "/bioProjectIds/sexPredictionLabels.tsv"
    else:
        filePath = "/bioProjectIds/tumor_stagePredictionLabels.tsv"
    group = []
    for threshold in thresholds:
        tp = 0
        fp = 0
        with open(filePath, "r") as readFile:
            #Looks like this: BioProject_ID	BioSample_Attribute_Name	Class_Probability	BioSample_Attribute_Unique_Terms	Manual_Accuracy_Check
            header = readFile.readline()
            for line in readFile:
                line = line.split("\t")
                try:
                    if float(line[2]) >= threshold:    
                        if int(line[-1].rstrip()) == 1:
                            tp += 1
                        else:
                            fp += 1
                except:
                    print(line)
        precision = float(tp)/float(tp+fp)
        recall = float(tp)/float(tp+fn)
        print(grouping, threshold, tp, fp, precision)
        group.append(precision)
    toVisualize[grouping] = group

with open("/results/Thresholds.tsv", "w") as writeFile:
    writeFile.write("Threshold\tRace Precision\tSex Precision\tTumor Stage Precision\n")
    for i in range(len(thresholds)):
        racVal = toVisualize["race"][i]
        sexVal = toVisualize["sex"][i]
        tumVal = toVisualize["tumor_stage"][i]
        writeFile.write(f"{thresholds[i]}\t \
                        {racVal}\t \
                        {sexVal}\t \
                        {tumVal}\n")

print(toVisualize)
plt.plot(thresholds, toVisualize["race"], label = "Race Precision", color='blue', linestyle='-', marker='o')
plt.plot(thresholds, toVisualize["sex"], label = "Sex Precision", color='red', linestyle='--', marker='x')
plt.plot(thresholds, toVisualize["tumor_stage"], label = "Tumor Stage Precision", color='black', linestyle='-.', marker='+')
plt.legend()
plt.title('Precision by Threshold')
plt.xlabel('Threshold for Classification as Relevant')
plt.ylabel('True Positives / (True Postives + False Positives)')
plt.savefig("/results/precisionByThreshold.png")
plt.show()