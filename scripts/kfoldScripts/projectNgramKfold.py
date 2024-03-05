
for metadataFocus in ["race", "sex", "tumor_stage"]:
    if metadataFocus == "race":
        filePath = "/bioProjectIds/yTruthRandomSample.tsv"
    elif metadataFocus == "sex":
        filePath = "/bioProjectIds/sexLabeled.tsv"
    else:
        filePath = "/bioProjectIds/tmpTumorTypeLabeledDoc.tsv"