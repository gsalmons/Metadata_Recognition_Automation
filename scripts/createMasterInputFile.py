"""Objectives: Create a file that could be the input for machine learning. Record the presence (1 = present, 0 = absent)
of each tri-gram for each column of each BioProject that has been hand labeled. 
Inputs: uniquePhrases.tsv contents of oracleColumns directory
Outputs: masterInputOracle.tsv
"""

import os
import re
# for group in ["Oracle", "Unlabeled"]: #TODO: change back!
for group in ["Unlabeled"]:
    #CODE TO GENERATE NGRAMS FOR OTHER BIOPROJECTS
    ngrams = dict()
    numProj = 0
    def reset0(dictionary):
        for key in dictionary:
            dictionary[key] = 0
        return(dictionary)

    with open("/bioProjectIds/uniquePhrases.tsv", "r") as dictFile:
        for line in dictFile:
            line = line.rstrip("\n")
            ngrams[line] = 0

    with open(f"/bioProjectIds/masterInput{group}1.tsv", "w") as writeFile:
        writeFile.write("BioProjectID\tFieldName\tUniqueValues")
        for gram in sorted(list(ngrams.keys())):
            writeFile.write("\t" + gram)
        writeFile.write("\n")

        for current_file in os.listdir(f'/bioProjectIds/{group.lower()}Columns'):
            if current_file.endswith(".tsv"):
                bioProjectId = current_file[:-4]

                with open(f"/bioProjectIds/{group.lower()}Columns/" + current_file, "r") as readFile:
                    for line in readFile:
                        ngrams = reset0(ngrams)
                        line = line.rstrip("\n")
                        if line == "" or line == " " or line == "  " or line == "\t" or line == "\n":
                            continue
                        if "," in line:
                            line = re.sub(",", "", line)
                        if "." in line:
                            line = re.sub(".", "", line)
                        if " " in line:
                            line = re.sub(" ", "_", line)
                        if ":" in line:
                            line = re.sub(":", "", line)
                        if ";" in line:
                            line = re.sub(";", "", line)
                        if "®" in line:
                            line = re.sub("®", "_", line)
                        if "__" in line:
                            line = re.sub("__", "_", line)
                        
                        line = line.lower()
                        line = line.split("\t")
                        fieldName = line[0]
                        uniqueValues = line[1:]
                        for m in line:
                            for i, character in enumerate(m):
                                if character == "_":
                                    continue
                                if len(m) >= i+3:
                                    if (m[i:i+3]) not in ngrams:
                                        print("Couldnt find", (m[i:i+3]))
                                        continue 
                                    ngrams[(m[i:i+3])] = 1
                                elif len(m) == i+2:
                                    if m[i:i+2]+"_" not in ngrams:
                                        print("Couldnt find", m[i:i+2]+"_")
                                        continue
                                    ngrams[(m[i:i+2]+"_")] = 1
                        writeFile.write(f"{bioProjectId}\t{fieldName}\t")
                        uniqueValues = ' '.join(uniqueValues)
                        writeFile.write(f"{uniqueValues}")
                        for gram in sorted(list(ngrams.keys())):
                            writeFile.write("\t" + str(ngrams[gram]))
                        writeFile.write("\n")