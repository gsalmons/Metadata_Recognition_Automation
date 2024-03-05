"""Objective: Get each unique value for each column of a BioProject across all its BioSamples. 
Clean the downloaded biosample data and remove noise. 
Inputs: bioProjectToBioSample.json, unlabeledProjects.tsv
Outputs: unlabeledColumns/{projectId}.tsv for each project ID that has not been chosen to be manually curated
"""
import json

bioProjects = []
allProj = dict()
cellLineTypes = list()
columnsToIgnore = ["sra", "geo", "accession", "id", "biosample"]
unknownVariants = {"", "Not applicable", "not applicable", "not applicable ", "Not Determined", "none", "None", "Not available", "Not Available", "Not determined", "not determined", "Not Applicable", "not collected", "Not Collected", "Not collected", "missing", "not_applicable", ".", "--", "-", "unknown", "Unknown", "not_available", "not available", "UNKNOWN", "n/a", "N/A", "n.a.", "N.A.", "na.", "N.a", "Missing", "na", "NA", "NA."}


with open("/bioProjectIds/bioProjectToBioSample.json", "r") as jFile:
    allProj = json.loads(jFile.read())
print("loaded in alright!")

with open("/bioProjectIds/unlabeledProjects.tsv", "r") as readFile:
    for line in readFile:
        line = line.rstrip()
        bioProjects.append(line)
print("Loaded the second in alright!")

for projectId in bioProjects:
    with open(f"/bioProjectIds/unlabeledColumns/{projectId}.tsv", "w") as writeFile:
        sampleIds = allProj[projectId]
        numSamples = len(sampleIds)
        projectInfo = dict()
        counter = 0
        for id in sampleIds:
            try:
                with open(f"/bioSamples/allJsons/{id}.json", "r") as readFile:
                    colAndVal = json.loads(readFile.read())
                if counter == 0:
                    for column, values in colAndVal.items():
                        projectInfo[column] = {values}
                    counter += 1
                else:
                    for column, values in colAndVal.items():
                        if column.lower() == "cell_line":
                            cellLineTypes.append(values)
                        if column not in projectInfo:
                            projectInfo[column] = {values}
                        else:
                            projectInfo[column].add(values)
            except Exception as e:
                print(f"Problem reading in {id}, {projectId}: {e}")
        firstTime = True
        for info in sorted(list(projectInfo.keys())):
            #Get rid of columns that we know do not contain useful info for the model
            if info in columnsToIgnore:
                continue
            #Get rid of columns that have unique values for each biosample if there is more than one biosample
            #UNLESS that column is description
            if numSamples > 1 and len(projectInfo[info]) == numSamples and info != "description" and info != "title":
                if info == "race" or info == "ethnicity":
                    print("problemo!", projectId)
                continue
            
            if type(next(iter(projectInfo[info]))) == float:
                continue
            relevant = set(projectInfo[info]) - set(unknownVariants)
            if len(relevant) > 0:              
                if firstTime:
                    writeFile.write(info + "\t")
                    firstTime = False
                else:
                    writeFile.write("\n" + info + "\t")
                for value in sorted(list(projectInfo[info])):
                    writeFile.write(value + "\t")