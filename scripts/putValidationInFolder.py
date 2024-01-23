import os
print(len(os.listdir("bioProjectIds/validationProjs")))
import shutil
filesToMove = set()
with open("bioProjectIds/validationRandomSample.tsv", "r") as readFile:
    for line in readFile:
        line = line.rstrip()
        fileName = line + ".tsv"
        filesToMove.add(fileName)
print(filesToMove)
destination_path = 'bioProjectIds/validationProjs'
for file in filesToMove:
    source_path = 'bioProjectIds/unlabeledColumns/' + file
    # Check if the file already exists in the destination directory
    if not os.path.exists(os.path.join(destination_path, os.path.basename(source_path))):
        # Move the file
        shutil.move(source_path, destination_path)
    else:
        print("File already exists in the destination directory.")
print(len(os.listdir("bioProjectIds/validationProjs")))