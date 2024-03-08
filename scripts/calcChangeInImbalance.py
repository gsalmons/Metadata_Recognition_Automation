totalNumDatasets = 135406# 25653 unlooked at datasets, 27653 total datasets. 135406 unfiltered attributes
#Number looked through TODO: Change total Num Datasets to total num attributes!
lookedThroughSex = 3785
lookedThroughRace = 1125
lookedThroughTumor = 992

#Recall stats
tenPercentRecallSex = .98
tenPercentRecallRace = .91
tenPercentRecallTumor = .82

#Precision stats
tenPercentPrecisionSex = .91
tenPercentPrecisionRace = .54
tenPercentPrecisionTumor = .28

probContainSex = lookedThroughSex * tenPercentPrecisionSex/ tenPercentRecallSex
probContainRace = lookedThroughRace * tenPercentPrecisionRace/ tenPercentRecallRace
probContainTumor = lookedThroughTumor * tenPercentPrecisionTumor/ tenPercentRecallTumor

numberForSameAccuracySex = tenPercentRecallSex * totalNumDatasets
numberForSameAccuracyRace = tenPercentRecallRace * totalNumDatasets
numberForSameAccuracyTumor = tenPercentRecallTumor * totalNumDatasets

speedUpRace = numberForSameAccuracyRace / (lookedThroughRace)
speedUpSex = numberForSameAccuracySex / (lookedThroughSex)
speedUpTumor = numberForSameAccuracyTumor / (lookedThroughTumor)

# speedUpScratchRace = numberForSameAccuracyRace / (lookedThroughRace + 2000)
# speedUpScratchSex = numberForSameAccuracySex / (lookedThroughSex + 2000)
# speedUpScratchTumor = numberForSameAccuracyTumor / (lookedThroughTumor + 2000)

imbalanceRace = probContainRace / totalNumDatasets
imbalanceSex = probContainSex / totalNumDatasets
imbalanceTumor = probContainTumor / totalNumDatasets

percentMissingRace = 100 - (imbalanceRace * 100)
percentMissingSex = 100 - (imbalanceSex * 100)
percentMissingTumor = 100 - (imbalanceTumor * 100)

print("Percent of attributes not about race:", percentMissingRace)
# print("Race speed up creating model from scratch", speedUpScratchRace)
print("Race speed up if model already trained", speedUpRace)
print("")
print("Percent of attributes not about sex:", percentMissingSex)
# print("Sex speed up creating model from scratch", speedUpScratchSex)
print("Sex speed up if model already trained", speedUpSex)
print("")
print("Percent of attributes not about tumor stage:", percentMissingTumor)
# print("Tumor speed up creating model from scratch", speedUpScratchTumor)
print("Tumor speed up if model already trained", speedUpTumor)