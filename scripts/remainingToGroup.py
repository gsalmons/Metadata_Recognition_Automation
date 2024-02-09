termSet = set()
with open("bioProjectIds/toGroup.tsv", "r") as readFile:
    header = readFile.readline()
    for line in readFile:
        termSet.add(line.rstrip())

alreadyAnnotated = set()
with open("bioProjectIds/raceGroupings.tsv", "r") as readFile:
    header = readFile.readline()
    for line in readFile:
        alreadyAnnotated.add(line.rstrip().split("\t")[0])

print(len(termSet))
print(len(alreadyAnnotated))
print(len(termSet - alreadyAnnotated))
print(termSet - alreadyAnnotated)