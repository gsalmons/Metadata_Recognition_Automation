"""This file is not complete! It will run through all the examples that we need!
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

for levelAnalysis in ["project", "column"]:
    for method in ["embedding", "ngram"]:
        for metadataFocus in ["race", "sex", "tumor_stage"]:
            #If arguments are provided, do just that one. Otherwise do all combinations.
            if len(sys.argv) > 1:
                levelAnalysis = sys.argv[1]
                method = sys.argv[2]
                metadataFocus = sys.argv[3]
            print("Working on:", levelAnalysis, method, metadataFocus)
            #Set truth file path
            labeledFile = "/bioProjectIds/yTruthRandomSample.tsv"
            if metadataFocus == "sex":
                labeledFile = "/bioProjectIds/sexLabeled.tsv"
            elif metadataFocus == "tumor_stage":
                labeledFile = "/bioProjectIds/tmpTumorTypeLabeledDoc.tsv"
            num1 = 0
            allnums = 0
            random.seed(1)
            yTruthDict = dict()
            if levelAnalysis == "project":
                # Load the true labels
                with open(labeledFile, "r") as readFile:
                    header = readFile.readline()
                    for line in readFile:
                        line = line.rstrip("\n")
                        line = line.split("\t")
                        tempDict = dict()
                        if line[1] == "0":
                            tempDict["truth"] = 0
                            tempDict["ngrams"] = []
                            yTruthDict[line[0]] = tempDict
                            allnums += 1
                        elif line[1] == "1":
                            tempDict["truth"] = 1
                            tempDict["ngrams"] = []
                            yTruthDict[line[0]] = tempDict 
                            allnums += 1
                            num1 += 1
                        else:
                            print("Minor problem....", line[0], line[1])               
            else:
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

            #Load the input data
            if method == "embedding" and levelAnalysis == "project":
                model = SentenceTransformer('sentence-transformers/all-roberta-large-v1',device="cpu")
                for file in os.listdir("/bioProjectIds/oracleColumns"):
                    filePath = "/bioProjectIds/oracleColumns/" + file
                    projID = file.split(".")[0]
                    if projID not in yTruthDict:
                        print("MISSING")
                        continue
                    with open(filePath, "r") as readFile:
                        text = readFile.read().rstrip()
                        futureTensor = model.encode(text)
                        xRandomSample.append(futureTensor)
                        yTruthList.append(yTruthDict[projID])
                        bioProjectList.append(projID)
            elif method == "ngram" and levelAnalysis == "project":
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
                        for i, value in enumerate(futureTensor):
                            futureTensor[i] = int(value)
                        if bioProjid in yTruthDict and yTruthDict[bioProjid]['ngrams'] != []:
                            newPart = []
                            for i, presence in enumerate(yTruthDict[line[0]]["ngrams"]):
                                if int(presence) > 0 or int(futureTensor[i]) > 0:
                                    newPart.append(1)
                                else:
                                    newPart.append(0)
                            yTruthDict[line[0]]["ngrams"]=newPart
                        else:
                            yTruthDict[line[0]]["ngrams"] = futureTensor
                for project in yTruthDict:
                    xRandomSample.append(yTruthDict[project]["ngrams"])
                    yTruthList.append(yTruthDict[project]["truth"])
                    bioProjectList.append(project)
            elif method == "ngram":
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
            else:
                model = SentenceTransformer('sentence-transformers/all-roberta-large-v1',device="cpu")
                for file in os.listdir("/bioProjectIds/oracleColumns"):
                    filePath = "/bioProjectIds/oracleColumns/" + file
                    projID = file.split(".")[0]
                    if projID not in yTruthDict:
                        print("MISSING")
                        continue
                    with open(filePath, "r") as readFile:
                        for line in readFile:
                            line = line.rstrip()
                            column = line.split("\t")[0]
                            line = re.sub("\t", " ", line)
                            futureTensor = model.encode(line)
                            xRandomSample.append(futureTensor)
                            bioProjectList.append(projID + " " + column)
                            yl = 0
                            if yTruthDict[projID]["overall"] == 1:
                                if column in yTruthDict[projID]["goodColumns"]:
                                    yl = 1
                                    num1 += 1
                            yTruthList.append(yl)
                            allnums += 1
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

            # # Define the probabilities for 0 and 1
            # probability_0 = (allnums - num1) / allnums  # Probability for 0
            # probability_1 =  num1 / allnums # Probability for 1
            # print(probability_0, probability_1)

            # # Generate a random array based on the specified probabilities
            # random_array = np.random.choice([0, 1], size=bestShape, p=[probability_0, probability_1])

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
                        #TODO: FIXME
                        if levelAnalysis == "project":
                            projOrder.append(bioProjectList[test_index[i]])
                        else:
                            whichColumns.append(bioProjectList[test_index[i]])

            except:
                print(train_index, test_index)
                # Create boxplots for the different cases
            print(len(allytestfold), len(allyscores))
            # continue
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
                    #TODO:FIXME
                    if levelAnalysis == "project":
                        writeFile.write(f"{whichFold[i]}\t{allyscores[i]}\t{allytestfold[i]}\t{projOrder[i]}\n")
                    else:
                        writeFile.write(f"{whichFold[i]}\t{allyscores[i]}\t{allytestfold[i]}\t{whichColumns[i]}\n")
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

            if method == "ngram":
                ###We are attempting to find the most imporant ngrams
                feature_importances = rf.feature_importances_

                # Get the names of the features
                feature_names = np.array(ngrams)

                # Sort features based on importance
                sorted_indices = np.argsort(feature_importances)[::-1]

                # Select the top n-grams
                numTop = 100
                top_ngrams = feature_names[sorted_indices][:numTop]
                top_importances = feature_importances[sorted_indices][:numTop]

                # Plot the top feature importances
                plt.figure(figsize=(10, 6))
                plt.bar(range(len(top_importances)), top_importances)
                plt.xticks(range(len(top_importances)), top_ngrams, rotation=45, ha="right")
                plt.xlabel('N-gram')
                plt.ylabel('Feature Importance')
                plt.title(f'Top {numTop} Feature Importances in Random Forest')
                plt.tight_layout()
                plt.savefig(f'/results/{levelAnalysis}/{method}/{metadataFocus}/mostRelevantNgrams_allsub.png')
                plt.show()

                #Save the ngrams by importance with their frequencies in sex and nonsex. 
                nonraceAverages = [0] * len(listedLists[0])
                numDivN = 0
                numDivR = 0
                raceAverages = [0] * len(listedLists[0])
                for i, columnInfo in enumerate(yTruthList):
                    if columnInfo == 0:
                        numDivN += 1
                        for j, value in enumerate(listedLists[i]):
                            nonraceAverages[j] += int(value)
                    else:
                        for j, value in enumerate(listedLists[i]):
                            raceAverages[j] += int(value)
                        numDivR += 1
                for k, value in enumerate(nonraceAverages):
                    nonraceAverages[k] = value / numDivN
                for k, value in enumerate(raceAverages):
                    raceAverages[k] = value / numDivR

                with open(f"/results/{levelAnalysis}/{method}/{metadataFocus}/ngramFrequencyByCategory.tsv", "w") as writeFile:
                    writeFile.write("Importance\tNgram\tFrequency in Sex Columns\tFrequency in Nonsex Columns\n")
                    for i, index in enumerate(sorted_indices):
                        writeFile.write(f"{i+1}\t{ngrams[index]}\t{raceAverages[index]}\t{nonraceAverages[index]}\n")

                #############################################################################
                ######REMOVING THE TOP X FEATURES WHAT WOULD HAPPEN?????####################
                #############################################################################

                # Remove the top X n-grams. It could be the top 50, 100, 150, etc.
                top_ngrams_to_remove = sorted_indices[:numTop]
                xRandomSample_reduced = np.delete(xRandomSample, top_ngrams_to_remove, axis=1)

                # Re-create the StratifiedKFold object
                skf = StratifiedKFold(n_splits=5, shuffle=True)

                # Initialize the list for accuracy scores
                lst_accu_stratified = []
                try:
                    for train_index, test_index in skf.split(xRandomSample_reduced, yTruthList):
                        x_train_fold, x_test_fold = xRandomSample_reduced[train_index], xRandomSample_reduced[test_index]
                        y_train_fold, y_test_fold = yTruthList[train_index], yTruthList[test_index]
                        rf.fit(x_train_fold, y_train_fold)
                        lst_accu_stratified.append(rf.score(x_test_fold, y_test_fold))

                    # Print the output.
                    print(f'List of possible accuracy without top {numTop} n-grams:', lst_accu_stratified)
                    print(f'\nMaximum Accuracy That can be obtained without top {numTop} n-grams is:', max(lst_accu_stratified) * 100, '%')
                    print(f'\nMinimum Accuracy without top {numTop} n-grams:', min(lst_accu_stratified) * 100, '%')
                    print(f'\nOverall Accuracy without top {numTop} n-grams:', mean(lst_accu_stratified) * 100, '%')
                    print(f'\nStandard Deviation without top {numTop} n-grams is:', stdev(lst_accu_stratified))
                except:
                    print(train_index, test_index)
                y_scores = rf.predict_proba(x_test_fold)[:, 1]  # Probability estimates of the positive class

                y_scores = rf.predict_proba(x_test_fold)[:, 1]  
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
                plt.savefig(f'/results/{levelAnalysis}/{method}/{metadataFocus}/precision_recall_curve_{numTop}_removed.png')

                y_pred = rf.predict(x_test_fold)

                # Compute confusion matrix
                cm = confusion_matrix(y_test_fold, y_pred)

                # Display confusion matrix
                disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[0, 1])

                # Plot confusion matrix
                plt.figure(figsize=(8, 6))
                disp.plot(cmap='Blues', values_format='d')
                plt.title('Confusion Matrix')
                plt.savefig(f'/results/{levelAnalysis}/{method}/{metadataFocus}/confusion_matrix_removed_top{numTop}.png')
                plt.show()
            if len(sys.argv) > 1:
                print("Finished!")
                sys.exit()