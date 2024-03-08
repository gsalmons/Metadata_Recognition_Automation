import GEOparse
import json
import os
import sys

def get_series_id(gsm_id):
    try:
        gse = GEOparse.get_GEO(geo=gsm_id, destdir="./")
        series_id = gse.metadata['series_id'][0]
        return series_id
    except Exception as e:
        print(f"Error processing GSM {gsm_id}: {e}")
        return None

BioProjectBioSample = dict()
with open("/bioProjectIds/bioProjectToBioSample.json", "r") as jfile:
    BioProjectBioSample = json.loads(jfile.read())

project_attribute_values = dict()
for bioProject in os.listdir("/bioProjectIds/unlabeledColumns"):
    project = bioProject.split(".")[0]
    samples = BioProjectBioSample[project]
    attributes = dict()
    foundBigGSE = False
    attributes["geo_series"] = "" 
    for sample in samples:
        sampleInfo = dict()
        try:
            with open(f"/bioSamples/allJsons/{sample}.json", "r") as jsonFile:
                sampleInfo = json.loads(jsonFile.read())

            if not foundBigGSE and "geo" in sampleInfo:
                series_id = get_series_id(sampleInfo["geo"])
                print(series_id)
                if series_id:
                    foundBigGSE = True
                    attributes["geo_series"] = series_id
        except:
            continue


bioProjectToGeoSeries = dict()
for project in project_attribute_values:
    bioProjectToGeoSeries[project] = project_attribute_values[project]["geo_series"]
with open("/bioProjectIds/bioProjectToGeoSeries.json", "w") as writeFile:
    writeFile.write(json.dumps(bioProjectToGeoSeries))
