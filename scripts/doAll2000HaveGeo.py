import GEOparse
import json
import os

def get_series_id(gsm_id):
    try:
        gse = GEOparse.get_GEO(geo=gsm_id, destdir="./")
        series_id = gse.metadata['series_id'][0]
        return series_id
    except Exception as e:
        print(f"Error processing GSM {gsm_id}: {e}")
        return None
counter = 0
BioProjectBioSample = dict()
with open("/bioProjectIds/bioProjectToBioSample.json", "r") as jfile:
    BioProjectBioSample = json.loads(jfile.read())

for bioProject in os.listdir("/bioProjectIds/oracleColumns"):
    project = bioProject.split(".")[0]
    samples = BioProjectBioSample[project]
    attributes = dict()
    attributes["biosample"] = []
    attributes["geo"] = []
    with open(f"/bioProjectIds/oracleColumns/{project}.tsv", "r") as readFile:
        for line in readFile:
            line = line.rstrip()
            attributes[line.split("\t")[0]] = []
    foundBigGSE = False
    attributes["geo_series"] = "" 
    for sample in samples:
        sampleInfo = dict()
        try:
            with open(f"/bioSamples/jsons/{sample}.json", "r") as jsonFile:
                sampleInfo = json.loads(jsonFile.read())
            
            if not foundBigGSE and "geo" in sampleInfo:
                series_id = get_series_id(sampleInfo["geo"])
                print(series_id)
                if series_id:
                    foundBigGSE = True
                    counter += 1
                    attributes["geo_series"] = series_id
        except:
            print(f"Not in {sample}\n")
print("TOTAL:", counter)