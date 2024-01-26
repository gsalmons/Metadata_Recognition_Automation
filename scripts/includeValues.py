import os
import re
import json
import pandas as pd
import sys
import GEOparse


bioProjectToGeoSeries = dict()
with open("/bioProjectIds/bioProjectToGeoSeries.json", "r") as jsonFile:
    bioProjectToGeoSeries = json.loads(jsonFile.read())

BioProjectBioSample = dict()
with open("/bioProjectIds/bioProjectToBioSample.json", "r") as jfile:
    BioProjectBioSample = json.loads(jfile.read())

project_attribute_values = dict()
for bioProject in os.listdir("/bioProjectIds/unlabeledColumns"):
    project = bioProject.split(".")[0]
    samples = BioProjectBioSample[project]
    attributes = dict()
    # attributes["biosample"] = []
    attributes["geo"] = []
    with open(f"/bioProjectIds/unlabeledColumns/{project}.tsv", "r") as readFile:
        for line in readFile:
            line = line.rstrip()
            attributes[line.split("\t")[0]] = []
    foundBigGSE = False
    for sample in samples:
        sampleInfo = dict()
        try:
            with open(f"/bioSamples/allJsons/{sample}.json", "r") as jsonFile:
                sampleInfo = json.loads(jsonFile.read())
            for a in attributes:
                if a in sampleInfo:
                    attributes[a].append(sampleInfo[a])
        except:
            lost = sample
    stylizedAttributes = dict()
    for a in attributes:
        a1 = a
        if "," in a1:
            a1 = re.sub(",", "", a1)
        if "." in a1:
            a1 = re.sub("\.", "", a1)
        if " " in a1:
            a1 = re.sub(" ", "_", a1)
        if ":" in a1:
            a1 = re.sub(":", "", a1)
        if ";" in a1:
            a1 = re.sub(";", "", a1)
        if "®" in a1:
            a1 = re.sub("®", "_", a1)
        if "__" in a1:
            a1 = re.sub("__", "_", a1)
        a1 = a1.lower()
        stylizedAttributes[a1] = attributes[a]
    project_attribute_values[project] = stylizedAttributes

for topic in ["race", "sex", "tumor_stage"]:
    print("doing", topic)
    with open(f"/predictions/{topic}/predictions.tsv", "r") as readFile:
        with open(f"/predictions/{topic}/{topic}_predictions.tsv", "w") as writeFile:
            header = readFile.readline()
            writeFile.write("BioProject_ID\tBioSample_Attribute_Name\tClass_Probability\tBioSample_Attribute_Unique_Terms\tGEO_Series\n")
            for line in readFile:
                line = line.rstrip()
                line = line.split("\t")
                uniqueVals = set(project_attribute_values[line[0]][line[1]])
                sortedListUniqueVals = sorted(list(uniqueVals))
                line.append("|".join(sortedListUniqueVals))
                if line[0] in bioProjectToGeoSeries:
                    line.append(bioProjectToGeoSeries[line[0]])
                else:
                    line.append("")
                newLine = "\t".join(line)
                writeFile.write(f"{newLine}\n")
                
    ### Sort the file
    input_file = f'/predictions/{topic}/{topic}_predictions.tsv'
    output_file = f'/predictions/{topic}/sorted_{topic}_predictions.tsv.gz'

    # Read the TSV file into a DataFrame
    df = pd.read_csv(input_file, sep='\t')

    # Sort the DataFrame by the third column in descending order
    df_sorted = df.sort_values(by=df.columns[2], ascending=False)

    # Save the sorted DataFrame back to a TSV file gzipped!
    df_sorted.to_csv(output_file, sep='\t', index=False, compression='gzip')