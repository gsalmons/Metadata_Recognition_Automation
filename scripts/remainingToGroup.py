termSet = set()
with open("bioProjectIds/toGroupSex2.tsv", "r") as readFile:
    header = readFile.readline()
    for line in readFile:
        termSet.add(line.rstrip().split("\t")[0].rstrip())

alreadyAnnotated = set()
with open("bioProjectIds/sexGrouping.tsv", "r") as readFile:
    header = readFile.readline()
    for line in readFile:
        alreadyAnnotated.add(line.rstrip().split("\t")[0].rstrip())

print(len(termSet))
print(len(alreadyAnnotated))
print(len(termSet - alreadyAnnotated))
with open("bioProjectIds/dontForgetRace.tsv", "w") as writeFile:
    for attribute in (termSet-alreadyAnnotated):
        writeFile.write(f"{attribute}\n")
# print(termSet - alreadyAnnotated)