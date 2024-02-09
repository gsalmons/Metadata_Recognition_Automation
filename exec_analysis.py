#!/usr/bin/env python

import subprocess
import os
def callFunction(script_path, commandType="python", arguments=None):
    command = []
    if arguments:
        command = [commandType, script_path, arguments]
    else:
        command = [commandType, script_path]
    # Run the external Python script
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output, error = process.communicate()
    return_code = process.returncode
    if return_code == 0:
        print(f"{script_path} executed successfully.")
        print("Output:")
        print(output)
    else:
        print(f"{script_path} failed with return code {return_code}.")
        print("Error:")
        print(error)

    with open("/bioProjectIds/test.txt", "w") as wFile:
        wFile.write("It worked!")
    return

###Step 1
# callFunction("/scripts/bioProjToBioSamp.py")

# ###Step 2
# callFunction("/scripts/getBioSampleFromJson.py")

# ###Step 3
# callFunction("/scripts/getRandomIds.py")

# ###Step 4
# callFunction("/scripts/IdentifyBiosamplesToLabel.py")

###Step 5 
#Download the biosamples for our randomly picked BioProjects

# fileSizeChanging = True
# fileSize = 0
# while fileSizeChanging:
    #fileSizeChanging = False
    # callFunction("/scripts/download.py", "python", "jsons")
    # for current_file in os.listdir('/bioSamples'):
    #     if current_file.startswith('keep'):
    #         print(f" - Downloading RunInfos -- biosamples present in {current_file}")
    #         os.system(f"metatools_download biosamples -l /bioSamples/{current_file} /bioSamples/jsons/")
    # callFunction("/scripts/retitling.py")
    # callFunction("/scripts/download.py", "python", "jsons")
    ##See if downloading continues to be successfull...
    # with open("/bioSamples/keepLoading.txt", "r") as readFile:
    #     newSize = len(readFile.read().rstrip().split("\n"))
    #     if newSize != fileSize:
    #         fileSizeChanging = True
    #         fileSize = newSize


# fileSizeChanging = True
# fileSize = 0

# while fileSizeChanging:
    # fileSizeChanging = False
#     callFunction("/scripts/download.py", "python", "allJsons")
    # for current_file in os.listdir('/bioSamples'):
    #     if current_file.startswith('keep'): 
    #         print(f" - Downloading RunInfos -- biosamples present in {current_file}")
    #         os.system(f"metatools_download biosamples -l /bioSamples/{current_file} /bioSamples/allJsons/")

    # callFunction("/scripts/retitling.py")
    # callFunction("/scripts/download.py", "python", "allJsons")
    ##See if downloading continues to be successfull...
    # with open("/bioSamples/keepLoading.txt", "r") as readFile:
    #     newSize = len(readFile.read().rstrip().split("\n"))
    #     if newSize != fileSize:
    #         fileSizeChanging = True
    #         fileSize = newSize

###The above step takes time because only so many requests can be run at a time...

# Step 6
# callFunction("/scripts/getColumnsForInitial.py")
# callFunction("/scripts/getColumnsForOther.py")

# Step 7
# callFunction("/scripts/uniqueTabDictionary.py")
# callFunction("/scripts/createMasterInputFile.py")
# callFunction("/scripts/createbettermasterfile.py") #in scripts old. TODO: Ask Piccolo if we should get rid of this one

# Step 8
# callFunction("/scripts/createMasterInputWithCount.py")
# callFunction("/scripts/raceWithCount.py")
# callFunction("/scripts/ourkfold.py")
# callFunction("/scripts/tumor_stage_kfold.py")
# callFunction("/scripts/sexKFold.py")

# callFunction("/scripts/usingEmbeddings.py")
# callFunction("/scripts/imbalancedRaceKFold.py")
# callFunction("/scripts/usingEmbeddingsWholeProject.py")
# callFunction("/scripts/wholeProjectRace.py")
# callFunction("/scripts/wholeProjectSexNgrams.py")
# callFunction("/scripts/wholeProjectTumorNgrams.py")
# callFunction("/scripts/sexembeddingwholeproj.py")
# callFunction("/scripts/tumorStageEmbeddingWholeProj.py")

# Step 9
# callFunction("/scripts/trainAndSaveModel.py")

# callFunction("/scripts/ultimateKFoldFile.py")
# callFunction("/scripts/generatePredictions.py")
# callFunction("/scripts/includeValues.py")
# callFunction("/scripts/getGeoSeriesId.py")
# callFunction("/scripts/doAll2000HaveGeo.py")
# callFunction("/scripts/quickViz.py")
# callFunction("/scripts/compareErrorsMachineHuman.py")
# callFunction("/scripts/compareSexErrors.py")
callFunction("/scripts/Quantify.py")
# print("IT WORKS")