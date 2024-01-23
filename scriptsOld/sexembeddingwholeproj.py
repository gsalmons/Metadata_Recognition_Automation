"""Objectives: Perform machine learning on the whole project using embeddings rather than column by column.
Inputs: sexLabeled
Outputs: 
"""
# Code modified from https://www.geeksforgeeks.org/stratified-k-fold-cross-validation/
import sys
# Import Required Modules.
from statistics import mean, stdev
from sklearn import preprocessing
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier  # Import Random Forest Classifier
import numpy as np
from sklearn.metrics import roc_curve, auc, confusion_matrix, precision_recall_curve, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import random
import os
import re
from sentence_transformers import SentenceTransformer 


random.seed(1)
num1 = 0
allnums = 0

levelAnalysis = "project"
method = "embedding"
metadataFocus = "sex"

# Load the true labels
yTruthDict = dict() 
with open("/bioProjectIds/sexLabeled.tsv", "r") as readFile:
    header = readFile.readline()
    for line in readFile:
        line = line.rstrip("\n")
        line = line.split("\t")
        tempDict = dict() 
        if line[1] == "0":
            yTruthDict[line[0]] = 0
            allnums += 1
        elif line[1] == "1":
            yTruthDict[line[0]] = 1 
            allnums += 1
            num1 += 1
        else:
            print("Minor problem....", line[0], line[1])               
bioProjectList = []
xRandomSample = []
yTruthList = []
ngrams = []

#Load the input data
#For each column in each json of each
model = SentenceTransformer('sentence-transformers/all-roberta-large-v1',device="cpu")
for file in os.listdir("bioProjectIds/oracleColumns"):
    filePath = "/bioProjectIds/oracleColumns/" + file
    projID = file.split(".")[0]
    if projID not in yTruthDict:
        print("MISSING")
        continue
    with open(filePath, "r") as readFile:
        text = readFile.read().rstrip()
        # #Should we do this?
        #text = re.sub("\t", " ", text)
        #text = re.sub("\n", " ", text)
        futureTensor = model.encode(text)
        xRandomSample.append(futureTensor)
        yTruthList.append(yTruthDict[projID])
        bioProjectList.append(projID)

print(sum(yTruthList))
listedLists = xRandomSample
xRandomSample = np.array(xRandomSample)

# Create classifier object.
rf = RandomForestClassifier(n_estimators=100, random_state=1)  # You can adjust the parameters as needed

# Create StratifiedKFold object.
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=1)
lst_accu_stratified = []
train_index = 0
test_index = 0
bestShape = xRandomSample.shape

# Define the probabilities for 0 and 1
probability_0 = (allnums - num1) / allnums  # Probability for 0
probability_1 =  num1 / allnums # Probability for 1
print(probability_0, probability_1)

# Generate a random array based on the specified probabilities
random_array = np.random.choice([0, 1], size=bestShape, p=[probability_0, probability_1])

print(bestShape)
yTruthList = np.array(yTruthList)
print(yTruthList.shape)
all_y_scores_0 = []
all_y_scores_1 = []

foldNumber = 0
allyscores = []
allytestfold = []
whichFold = []
whichColumns = []
projOrder = []
try:
    for train_index, test_index in skf.split(xRandomSample, yTruthList):
        x_train_fold, x_test_fold = xRandomSample[train_index], xRandomSample[test_index]
        y_train_fold, y_test_fold = yTruthList[train_index], yTruthList[test_index]
        rf.fit(x_train_fold, y_train_fold)
        y_scores = rf.predict_proba(x_test_fold)
        foldNumber += 1
        y_scores = rf.predict_proba(x_test_fold)[:, 1]  #TODO: use pos class for boxplot probs. 
        precision, recall, _ = precision_recall_curve(y_test_fold, y_scores)
        auc_pr = auc(recall, precision)
        plt.figure(figsize=(8, 6))
        plt.plot(recall, precision, color='darkorange', lw=2, label=f'PR curve (AUC = {auc_pr:.2f})')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Precision-Recall Curve')
        plt.legend(loc='lower left')
        plt.grid(True)
        plt.show()
        plt.savefig(f'/results/{levelAnalysis}/{method}/{metadataFocus}/precision_recall_curve_allsub_{foldNumber}.png')
        for i in range(len(y_scores)):
            allyscores.append(y_scores[i])
        for i in range(len(y_test_fold)):
            allytestfold.append(y_test_fold[i])
            whichFold.append(foldNumber)
            projOrder.append(bioProjectList[test_index[i]])

except:
    print(train_index, test_index)
    # Create boxplots for the different cases

#Precision recall
precision, recall, _ = precision_recall_curve(allytestfold, allyscores)
auc_pr = auc(recall, precision)
plt.figure(figsize=(8, 6))
plt.plot(recall, precision, color='darkorange', lw=2, label=f'PR curve (AUC = {auc_pr:.2f})')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend(loc='lower left')
plt.grid(True)
plt.show() 
plt.savefig(f'/results/{levelAnalysis}/{method}/{metadataFocus}/precision_recall_curve.png')

with open(f"/results/{levelAnalysis}/{method}/{metadataFocus}/projectEmbeddingConfidencesallsub.tsv", "w") as writeFile:
    writeFile.write(f"Fold\tPrediction\tTruth\tProj&Col\n")
    for i in range(len(allytestfold)):
        writeFile.write(f"{whichFold[i]}\t{allyscores[i]}\t{allytestfold[i]}\t{projOrder[i]}\n")

# Calculate the AUC-ROC score
roc_auc = roc_auc_score(allytestfold, allyscores)

# Print or save the AUC-ROC score
print(f'AUC-ROC Score: {roc_auc:.2f}')

# Compute ROC curve and ROC area
fpr, tpr, _ = roc_curve(allytestfold, allyscores)

y_pred = rf.predict(x_test_fold)

# Compute confusion matrix
cm = confusion_matrix(y_test_fold, y_pred)

# Display confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[0, 1])

# Plot confusion matrix
plt.figure(figsize=(8, 6))
disp.plot(cmap='Blues', values_format='d')
plt.title('Confusion Matrix')
plt.savefig(f'/results/{levelAnalysis}/{method}/{metadataFocus}/confusion_matrix_allsub.png')
plt.show()