from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import numpy as np
import random

random.seed(1)
for metadataFocus in ["race", "sex", "tumor_stage"]:
    #Set truth file path
    labeledFile = "/bioProjectIds/manuallyCuratedFiles/training2000/race.tsv"
    if metadataFocus == "sex":
        labeledFile = "/bioProjectIds/manuallyCuratedFiles/training2000/sex.tsv"
    elif metadataFocus == "tumor_stage":
        labeledFile = "/bioProjectIds/manuallyCuratedFiles/training2000/tumor_stage.tsv"

    # Load the true labels
    yTruthDict = dict() 
    with open(labeledFile, "r") as readFile:
        header = readFile.readline()
        for line in readFile:
            line = line.rstrip("\n")
            line = line.split("\t")
            tempDict = dict()
            if line[1] == "0":
                tempDict["overall"] = 0
                yTruthDict[line[0]] = tempDict
            elif line[1] == "1":
                tempDict["overall"] = 1
                tempDict["goodColumns"] = line[2].split(" ")
                yTruthDict[line[0]] = tempDict 
            else:
                print("Minor problem....", line[0], line[1])               
    bioProjectList = []
    xRandomSample = []
    yTruthList = []
    ngrams = []
    num1 = 0
    allnums = 0

    #Load the input data
    with open("/bioProjectIds/masterInputOracle1.tsv", "r") as readFile:
        header = readFile.readline()
        ngrams = header.split("\t")[3:]
        for line in readFile:
            line = line.rstrip("\n")
            line = line.split("\t")
            bioProjid = line[0]
            if bioProjid not in yTruthDict:
                continue
            columnName = line[1]
            futureTensor = line[3:]
            xRandomSample.append(futureTensor)
            bioProjectList.append(bioProjid + columnName)
            yl = 0
            if yTruthDict[bioProjid]["overall"] == 1:
                if columnName in yTruthDict[bioProjid]["goodColumns"]:
                    yl = 1
                    num1 += 1
            yTruthList.append(yl)
            allnums += 1
    print(sum(yTruthList))
    listedLists = xRandomSample
    xRandomSample = np.array(xRandomSample)

    # Create classifier object.
    rf = RandomForestClassifier(n_estimators=100, random_state=1)
    rf.fit(xRandomSample, yTruthList)

    # joblib for easy save and load (joblib.load())
    joblib.dump(rf, f'/models/{metadataFocus}/random_forest_model.joblib')