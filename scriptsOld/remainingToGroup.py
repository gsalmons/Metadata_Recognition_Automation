termSet = set()
with open("bioProjectIds/toGroupSex2.tsv", "r") as readFile:
    header = readFile.readline()
    for line in readFile:
        termSet.add(line.rstrip().split("\t")[0].rstrip())

alreadyAnnotated = set()
with open("bioProjectIds/manuallyCuratedFiles/quantify/sex.tsv", "r") as readFile:
    header = readFile.readline()
    for line in readFile:
        alreadyAnnotated.add(line.rstrip().split("\t")[0].rstrip())

print(len(termSet))
print(len(alreadyAnnotated))
print(len(termSet - alreadyAnnotated))
with open("bioProjectIds/dontForgetSex.tsv", "w") as writeFile:
    for attribute in (termSet-alreadyAnnotated):
        writeFile.write(f"{attribute}\n")
# print(termSet - alreadyAnnotated)