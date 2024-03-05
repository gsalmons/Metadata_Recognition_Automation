import os
import json

BioProjectBioSample = dict()
with open("bioProjectIds/bioProjectToBioSample.json", "r") as jfile:
    BioProjectBioSample = json.loads(jfile.read())
uniqueValDict = dict()

uniqueValSet = set()
relevantProjectsAndAttributes = dict()

labeled3000 = dict()
#Sex we care about column index 1
with open("bioProjectIds/Consensus Validation Labels - Sheet1.tsv", "r") as readFile:
    header = readFile.readline()
    for line in readFile:
        line = line.rstrip().split("\t")
        if int(line[1]) == 0:
            labeled3000[line[0]] = 0
        else:
            tmp = dict()
            for word in line[2].rstrip().split(" "):
                tmp[word] = 1
            labeled3000[line[0]] = tmp


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
        else:
            if line[0] in labeled3000:
                if type(labeled3000[line[0]]) == type(labeled3000):
                    print("SUCESS!")
                    if line[1] in labeled3000[line[0]]:
                        if line[0] in relevantProjectsAndAttributes:
                            relevantProjectsAndAttributes[line[0]].append(line[1])
                        else:
                            relevantProjectsAndAttributes[line[0]] = [line[1]]
#Load in our hand labeled 2000 as well!
with open("bioProjectIds/yTruthRandomSample.tsv") as readFile:
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
            uniqueValDict[samplesInfo] = bioProject
        except:
            print("Something is up")
    allAttributes[bioProject] = attributes["all"]

with open("bioProjectIds/allRelevantAttributeValues.json", "w") as jfile:
    jfile.write(json.dumps(allAttributes))


with open("bioProjectIds/toGroup2.tsv", "w") as writeFile:
    writeFile.write("Value\tBioProject\tCategory\n")
    for uniqueVal in uniqueValDict:
        if uniqueVal == "" or uniqueVal == " ":
            continue
        writeFile.write(f"{uniqueVal}\t{uniqueValDict[uniqueVal]}\t\n")


### Race above, sex below this line

BioProjectBioSample = dict()
with open("bioProjectIds/bioProjectToBioSample.json", "r") as jfile:
    BioProjectBioSample = json.loads(jfile.read())

uniqueValDict = dict()
relevantProjectsAndAttributes = dict()
labeled3000 = dict()
#Sex we care about column index 3
with open("bioProjectIds/Consensus Validation Labels - Sheet1.tsv", "r") as readFile:
    header = readFile.readline()
    for line in readFile:
        line = line.rstrip().split("\t")
        if int(line[3]) == 0:
            labeled3000[line[0]] = 0
        else:
            tmp = dict()
            for word in line[4].rstrip().split(" "):
                tmp[word] = 1

#load in truly relevant to race projects
with open("bioProjectIds/sexPredictionLabels.tsv", "r") as readFile:
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
        else:
            if line[0] in labeled3000:
                if type(labeled3000[line[0]]) == type(dict()):
                    print("SUCESS!")
                    if line[1] in labeled3000[line[0]]:
                        if line[0] in relevantProjectsAndAttributes:
                            relevantProjectsAndAttributes[line[0]].append(line[1])
                        else:
                            relevantProjectsAndAttributes[line[0]] = [line[1]]
            #Need to check if it is in one of the 3000

#Load in our hand labeled 2000 as well!
with open("bioProjectIds/sexLabeled.tsv") as readFile:
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
            uniqueValDict[samplesInfo] = bioProject
        except:
            try:
                with open(f"bioSamples/jsons/{sample}.json", "r") as jsonFile:
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
                uniqueValDict[samplesInfo] = bioProject
            except:
                print("Error", sample)
    allAttributes[bioProject] = attributes["all"]

with open("bioProjectIds/allRelevantAttributeValuesSex.json", "w") as jfile:
    jfile.write(json.dumps(allAttributes))

with open("bioProjectIds/toGroupSex2.tsv", "w") as writeFile:
    writeFile.write("Value\tBioProject\tCategory\n")
    for uniqueVal in uniqueValDict:
        if uniqueVal == "" or uniqueVal == " ":
            continue
        writeFile.write(f"{uniqueVal}\t{uniqueValDict[uniqueVal]}\t\n")