import joblib
import numpy as np
import random
import sys
from sklearn.ensemble import RandomForestClassifier

random.seed(1)
xInput = []
bioProjectList = []

with open ("/bioProjectIds/masterInputUnlabeled1.tsv", "r") as readFile:
    header = readFile.readline()
    ngrams = header.split("\t")[3:]
    for line in readFile:
        line = line.rstrip("\n")
        line = line.split("\t")
        bioProjid = line[0]
        columnName = line[1]
        futureTensor = line[3:]
        xInput.append(futureTensor)
        bioProjectList.append(bioProjid + " " + columnName)
listedLists = xInput
xInput = np.array(xInput)

for metadataFocus in ["race", "sex", "tumor_stage"]:
    rf = joblib.load(f"/models/{metadataFocus}/random_forest_model.joblib")
    predictions = rf.predict(xInput)
    prediction_probabilities = rf.predict_proba(xInput)[:, 1] #Only for the positive class!
    print("Boo yah kcha")
    with open(f"/predictions/{metadataFocus}/predictions.tsv", "w") as writeFile:
        writeFile.write(f"BioProject_ID\tBioSample_Attribute_Name\tClass_Probability\n")
        for i, project in enumerate(bioProjectList):
            projectID = project.split(" ")[0]
            column = " ".join(project.split(" ")[1:])
            writeFile.write(f"{projectID}\t{column}\t{prediction_probabilities[i]}\n")