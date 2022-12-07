import os
import time
import json
import collections
import DatasetProcessor
import ReadMeRelevanceCalculator
import StarRelevanceCalculator


DSP = DatasetProcessor.DatasetProcessor()
SRC = StarRelevanceCalculator.StarRelevanceCalculator()
RRC = ReadMeRelevanceCalculator.ReadMeRelevanceCalculator()
bugD, projD = DSP.GetSstubData()

for subdir, dirs, files in os.walk(os.getcwd() + "/JSONs"):
    completedJsons = files

# count = 0
for subdir, dirs, files in os.walk(os.getcwd() + "/Processed-ReadMe-Files"):
    for currentProject in files:
        # count += 1
        start = time.time()
        if currentProject.replace(".txt", ".json") in completedJsons or currentProject == "CurrentReadMe.txt":
            continue

        cleanedCurrProj = currentProject.replace(".txt", "")
        print("CURRENT PROJECT:", cleanedCurrProj)
        distSum = {}
        for bugType in bugD:
            distSum[bugType] = 0

        for project in files:
            # count += 1
            if project == currentProject:
                continue
            print("Now comparing " + currentProject + " to " + project)
            readMeRelevance = RRC.CalculateRelevance(currentProject, project)
            starRelevance = SRC.CalculateRelevance(currentProject, project)
            projectRelevance = readMeRelevance * starRelevance
            print("Project Relevance:", projectRelevance)

            for bug in bugD:
                try:
                    projectBugWeight = projD[project.replace(".txt", "")][bug] * projectRelevance
                    distSum[bug] += projectBugWeight
                except KeyError:
                    continue

            # if count == 5: break

        distSumTotal = sum(distSum.values())
        projDSumTotal = sum(projD[cleanedCurrProj].values())

        accuracySum = 0
        for key in distSum:
            if distSumTotal != 0:
                distSum[key] = distSum[key]/distSumTotal * 100
            try:
                projD[cleanedCurrProj][key] = projD[cleanedCurrProj][key]/projDSumTotal * 100
            except KeyError:
                projD[cleanedCurrProj][key] = 0.0
            except ZeroDivisionError:
                continue

            accuracySum += (100 - abs(distSum[key] - projD[cleanedCurrProj][key]))

        accuracy = accuracySum / len(distSum)

        distSum = DSP.SortDictionary(distSum)
        projD[cleanedCurrProj] = DSP.SortDictionary(projD[cleanedCurrProj])

        print(distSum)
        print(projD[cleanedCurrProj])
        print("Accuracy:", accuracy)

        with open('JSONs/' + cleanedCurrProj + '.json', 'w') as projectJson:
            projectJson.write("{\n\t")
            projectJson.write('"Accuracy" : "' + str(accuracy) + '",\n')
            projectJson.write('\t"Prediction" : [{\n\t\t')
            i = 0
            for key in distSum:
                projectJson.write('"' + key + '" : "' + str(distSum[key]) + '"')
                if i != 15:
                    projectJson.write(',\n\t\t')
                else:
                    projectJson.write('\n\t}],\n')
                i += 1

            projectJson.write('\t"Actual" : [{\n\t\t')
            i = 0
            for key in projD[cleanedCurrProj]:
                projectJson.write('"' + key + '" : "' + str(projD[cleanedCurrProj][key]) + '"')
                if i != 15:
                    projectJson.write(',\n\t\t')
                else:
                    projectJson.write('\n\t}]\n')
                i += 1
            projectJson.write('}')

        end = time.time()
        print("The time of execution of above program is :", (end-start), "s\n")

# DSP.PlotBarForTwoDict(distSum, projD['zhihu.Matisse'])



