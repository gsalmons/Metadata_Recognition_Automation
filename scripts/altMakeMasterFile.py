#Optimized with aide from chat gpt
import os
import re

# Pre-compile Regular Expressions
regex_comma = re.compile(",")
regex_dot = re.compile("\.")
regex_space = re.compile(" ")
regex_colon = re.compile(":")
regex_semicolon = re.compile(";")
regex_registered = re.compile("®")
regex_double_underscore = re.compile("__")

# Avoid Redundant Checks
replace_chars = {",": "", ".": "", " ": "_", ":": "", ";": "", "®": "_", "__": "_"}

# Use Set for Faster Membership Check
ngrams_set = set()

# Reset Dictionary Values to 0
def reset0(dictionary):
    for key in dictionary:
        dictionary[key] = 0
    return dictionary

# Optimize String Concatenation
parts = []

for group in ["Unlabeled"]:
    with open("bioProjectIds/uniquePhrases.tsv", "r") as dictFile:
        for line in dictFile:
            line = line.rstrip("\n")
            ngrams[line] = 0
            ngrams_set.add(line)

    with open(f"bioProjectIds/masterInput{group}2.tsv", "w") as writeFile:
        parts.append("BioProjectID\tFieldName\tUniqueValues")
        for gram in sorted(list(ngrams.keys())):
            parts.append("\t" + gram)
        parts.append("\n")

        for current_file in os.listdir(f'bioProjectIds/{group.lower()}Columns'):
            if current_file.endswith(".tsv"):
                bioProjectId = current_file[:-4]

                with open(f"bioProjectIds/{group.lower()}Columns/" + current_file, "r") as readFile:
                    for line in readFile:
                        ngrams = reset0(ngrams)
                        line = line.rstrip("\n")
                        if line == "":
                            continue

                        # Apply the compiled regex patterns
                        line = regex_comma.sub("", line)
                        line = regex_dot.sub("", line)
                        line = regex_space.sub("_", line)
                        line = regex_colon.sub("", line)
                        line = regex_semicolon.sub("", line)
                        line = regex_registered.sub("_", line)
                        line = regex_double_underscore.sub("_", line)

                        line = line.lower()
                        line = line.split("\t")
                        fieldName = line[0]
                        uniqueValues = line[1:]

                        for m in line:
                            for i, character in enumerate(m):
                                if character == "_":
                                    continue
                                if len(m) >= i+3:
                                    if (m[i:i+3]) not in ngrams_set:
                                        print("Couldn't find", (m[i:i+3]))
                                        continue 
                                    ngrams[(m[i:i+3])] = 1
                                elif len(m) == i+2:
                                    if m[i:i+2]+"_" not in ngrams_set:
                                        print("Couldn't find", m[i:i+2]+"_")
                                        continue
                                    ngrams[(m[i:i+2]+"_")] = 1

                        parts.append(f"{bioProjectId}\t{fieldName}\t")
                        uniqueValues = ' '.join(uniqueValues)
                        parts.append(f"{uniqueValues}")
                        for gram in sorted(list(ngrams.keys())):
                            parts.append("\t" + str(ngrams[gram]))
                        parts.append("\n")

        writeFile.write("".join(parts))
