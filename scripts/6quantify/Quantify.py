import os
import json
import sys

BioProjectBioSample = dict()
with open("bioProjectIds/bioProjectToBioSample.json", "r") as jfile:
    BioProjectBioSample = json.loads(jfile.read())
categories = dict()
categoryCount = dict()
for i in range(10):
    categoryCount[i] = 0
with open("bioProjectIds/manuallyCuratedFiles/quantify/race.tsv", "r") as readFile:
    header = readFile.readline()
    for numberLine, line in enumerate(readFile):
        line = line.rstrip()
        line = line.split("\t")
        term = line[0]
        print(line)
        if len(line) > 1 and line[1].isdigit():
            category = int(line[1])
            categories[term] = category
        else:
            print("error, ending early on line", numberLine)
            sys.exit()
# print(category, categories)
relevantProjectsAndAttributes = dict()
#load in truly relevant to race projects
with open("bioProjectIds/racePredictionLabels.tsv") as readFile:
    header = readFile.readline()
    for line in readFile:
        line = line.rstrip()
        line = line.split('\t')
        # print(len(line))
        if line[-1] == "1" and len(line) > 4:
            if line[0] in relevantProjectsAndAttributes:
                relevantProjectsAndAttributes[line[0]].append(line[1])
            else:
                relevantProjectsAndAttributes[line[0]] = [line[1]]

#Load in our hand labeled 2000 as well!
with open("bioProjectIds/manuallyCuratedFiles/training2000/race.tsv") as readFile:
    header = readFile.readline()
    for line in readFile:
        line = line.rstrip()
        line = line.split('\t')
        # print(len(line))
        if line[-1] == "1":
            if line[0] in relevantProjectsAndAttributes:
                attributeNames = line[2].split(" ")
                for attrib in attributeNames:
                    relevantProjectsAndAttributes[line[0]].append(line[2])
            else:
                attributeNames = line[2].split(" ")
                relevantProjectsAndAttributes[line[0]] = [attributeNames[0]]
                for attrib in attributeNames[1:]:
                    relevantProjectsAndAttributes[line[0]].append(line[2])
print(categories)
#load in every sample value for those relevant attributes
allAttributes = dict()
for bioProject in relevantProjectsAndAttributes:
    samples = BioProjectBioSample[bioProject]
    attributes = dict()
    attributes["all"] = []
    for a in relevantProjectsAndAttributes[bioProject]:
        attributes[a] = []
    for sample in samples:
        sampleInfo = dict()
        try:
            with open(f"bioSamples/allJsons/{sample}.json", "r") as jsonFile:
                sampleInfo = json.loads(jsonFile.read())
            samplesInfo = ""
            for a in attributes:
                if a in sampleInfo:
                    if sampleInfo[a] == "zero":
                        sampleInfo[a] = "0"
                    if sampleInfo[a] == "one":
                        sampleInfo[a] = "1"
                    if sampleInfo[a].isdigit():
                        newer = f"{a}:{sampleInfo[a]} "
                        samplesInfo += newer
                    else:
                        samplesInfo += sampleInfo[a] + " "
            attributes["all"].append(samplesInfo)
            if samplesInfo.rstrip() in categories:
                categoryCount[categories[samplesInfo.rstrip()]] += 1
            elif samplesInfo.isspace() or samplesInfo == "":
                continue
            else:
                print("ERROR with", samplesInfo)
        except:
            print("Something is up")
    allAttributes[bioProject] = attributes["all"]

total = 0
for cat in categoryCount:
    total += categoryCount[cat]
print(total)

with open("results/quantifyRepresentation/race.tsv", "w") as writeFile:
    for cat in categoryCount:
        writeFile.write(f"{cat}\t{categoryCount[cat]}\n")
#ABOVE IS ALL FOR RACE. BELOW IS ALL FOR SEX

# BioProjectBioSample = dict()
# with open("bioProjectIds/bioProjectToBioSample.json", "r") as jfile:
#     BioProjectBioSample = json.loads(jfile.read())
# categories = dict()
# categoryCount = dict()
# for i in range(3):
#     categoryCount[i] = 0
# with open("bioProjectIds/manuallyCuratedFiles/quantify/sex.tsv", "r") as readFile:
#     header = readFile.readline()
#     for numberLine, line in enumerate(readFile):
#         line = line.rstrip()
#         line = line.split("\t")
#         term = line[0]
#         print(line)
#         if len(line) > 1 and line[2].isdigit():
#             category = int(line[2])
#             categories[term] = category
#         else:
#             print("error, ending early on line", numberLine)
#             sys.exit()
# # print(category, categories)
# relevantProjectsAndAttributes = dict()
# #load in truly relevant to sex projects
# with open("bioProjectIds/sexPredictionLabels.tsv") as readFile:
#     header = readFile.readline()
#     for line in readFile:
#         line = line.rstrip()
#         line = line.split('\t')
#         # print(len(line))
#         if line[-1] == "1" and len(line) > 4:
#             if line[0] in relevantProjectsAndAttributes:
#                 relevantProjectsAndAttributes[line[0]].append(line[1])
#             else:
#                 relevantProjectsAndAttributes[line[0]] = [line[1]]
# print(len(relevantProjectsAndAttributes))
# # sys.exit()
# #Load in our hand labeled 2000 as well!
# with open("bioProjectIds/manuallyCuratedFiles/training2000/sex.tsv") as readFile:
#     header = readFile.readline()
#     for line in readFile:
#         line = line.rstrip()
#         line = line.split('\t')
#         # print(len(line))
#         if line[-1] == "1":
#             if line[0] in relevantProjectsAndAttributes:
#                 attributeNames = line[2].split(" ")
#                 for attrib in attributeNames:
#                     relevantProjectsAndAttributes[line[0]].append(line[2])
#             else:
#                 attributeNames = line[2].split(" ")
#                 relevantProjectsAndAttributes[line[0]] = [attributeNames[0]]
#                 for attrib in attributeNames[1:]:
#                     relevantProjectsAndAttributes[line[0]].append(line[2])
# print(categories)
# #load in every sample value for those relevant attributes
# allAttributes = dict()
# for bioProject in relevantProjectsAndAttributes:
#     samples = BioProjectBioSample[bioProject]
#     attributes = dict()
#     attributes["all"] = []
#     for a in relevantProjectsAndAttributes[bioProject]:
#         attributes[a] = []
#     for sample in samples:
#         sampleInfo = dict()
#         try:
#             with open(f"bioSamples/allJsons/{sample}.json", "r") as jsonFile:
#                 sampleInfo = json.loads(jsonFile.read())
#             samplesInfo = ""
#             for a in attributes:
#                 if a in sampleInfo:
#                     if sampleInfo[a] == "zero":
#                         sampleInfo[a] = "0"
#                     if sampleInfo[a] == "one":
#                         sampleInfo[a] = "1"
#                     if sampleInfo[a].isdigit():
#                         newer = f"{a}:{sampleInfo[a]} "
#                         samplesInfo += newer
#                     else:
#                         samplesInfo += sampleInfo[a] + " "
#             attributes["all"].append(samplesInfo)
#             if samplesInfo.rstrip() in categories:
#                 categoryCount[categories[samplesInfo.rstrip()]] += 1
#             elif samplesInfo.isspace() or samplesInfo == "":
#                 continue
#             else:
#                 print("ERROR with", samplesInfo)
#         except:
#             try:
#                 with open(f"bioSamples/jsons/{sample}.json", "r") as jsonFile:
#                     sampleInfo = json.loads(jsonFile.read())
#                 samplesInfo = ""
#                 for a in attributes:
#                     if a in sampleInfo:
#                         if sampleInfo[a] == "zero":
#                             sampleInfo[a] = "0"
#                         if sampleInfo[a] == "one":
#                             sampleInfo[a] = "1"
#                         if sampleInfo[a].isdigit():
#                             newer = f"{a}:{sampleInfo[a]} "
#                             samplesInfo += newer
#                         else:
#                             samplesInfo += sampleInfo[a] + " "
#                 attributes["all"].append(samplesInfo)
#                 if samplesInfo.rstrip() in categories:
#                     categoryCount[categories[samplesInfo.rstrip()]] += 1
#                 elif samplesInfo.isspace() or samplesInfo == "":
#                     continue
#             except:
#                 print(sample, "not found")

#     allAttributes[bioProject] = attributes["all"]

# total = 0
# for cat in categoryCount:
#     total += categoryCount[cat]
# print(total)

# with open("results/quantifyRepresentation/sex.tsv", "w") as writeFile:
#     for cat in categoryCount:
#         writeFile.write(f"{cat}\t{categoryCount[cat]}\n")