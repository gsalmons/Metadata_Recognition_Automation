"""Objective: Identify which 3000 bioProjects will be manually curated via random selection for validation purposes
Inputs: No args. bioProjectToBioSample.json, unlabeledProjects.tsv
Outputs: validationRandomSample.tsv and allUnlabeledProjects.tsv
The first file is the 3000 chosen, the second file contains project IDs that were not chosen for this or training. 
"""

import random
import json
#load in all the bioProject IDs
idsWithSamples = []
with open("/bioProjectIds/unlabeledProjects.tsv", "r") as readFile:
    for line in readFile:
        line = line.rstrip()
        idsWithSamples.append(line)

#Pick 3000 of them at random 
random.seed(0)
random_values = random.sample(idsWithSamples, 3000)
print(random_values)

#Save randomly generated IDs to a file
with open("/bioProjectIds/validationRandomSample.tsv", "w") as writeFile:
    for id in random_values:
        writeFile.write(id + "\n")

unlabeled = set(idsWithSamples) - set(random_values)
with open("/bioProjectIds/allUnlabeledProjects.tsv", "w") as writeFile:
    for id in unlabeled:
        writeFile.write(id + "\n")