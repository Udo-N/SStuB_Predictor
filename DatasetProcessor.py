import json
import collections
import numpy as np
import matplotlib.pyplot as plt


class DatasetProcessor:
    @staticmethod
    def BugNameConverter(keys):
        newKeys = []
        for key in keys:
            separatedKey = key.split("_")
            newKey = separatedKey[0][0:2] + '_' + separatedKey[1][0:2]
            if newKey in newKeys and len(separatedKey) > 2:
                newKey += '_' + separatedKey[2][0:2]
            elif newKey in newKeys:
                newKey = separatedKey[0][0:2] + '_' + separatedKey[1][0:3]
            newKeys.append(newKey)

        return newKeys

    @staticmethod
    def PlotBarForDict(dict):
        plt.bar(range(len(dict)), list(dict.values()), align='center')
        plt.xticks(range(len(dict)), list(DatasetProcessor.BugNameConverter(dict.keys())))
        plt.show()

    @staticmethod
    def PlotBarForTwoDict(predicted, actual):
        X = np.arange(len(predicted))
        ax = plt.subplot(111)

        ax.bar(X, predicted.values(), width=0.2, color='b', align='center')
        ax.bar(X - 0.2, actual.values(), width=0.2, color='g', align='center')
        ax.legend(('Predicted', 'Actual'))

        plt.xticks(X, predicted.keys())
        plt.show()

    @staticmethod
    def SortDictionary(dictionary):
        return {k: dictionary[k] for k in sorted(dictionary)}
        # sortedDictionary = {}
        # sortedKeys = sorted(dictionary)
        # for key in sortedKeys:
        #     sortedDictionary[key] = dictionary[key]
        #
        # return sortedDictionary

    @staticmethod
    def GetSstubData():
        f = open('sstub_files/sstubsLarge.json', encoding='utf-8')

        bugFixes = json.load(f)
        bugTypeDict = {}            # Dictionary containing how often each bug appears
        projectDict = {}            # Dictionary containing how often bugs appear in each project

        # print(data[0]['bugType'])
        for fix in bugFixes:
            try:
                bugTypeDict[fix['bugType']] += 1
            except KeyError:
                bugTypeDict[fix['bugType']] = 1

            try:
                var = projectDict[fix['projectName']]
                try:
                    projectDict[fix['projectName']][fix['bugType']] += 1
                except KeyError:
                    projectDict[fix['projectName']][fix['bugType']] = 1
            except KeyError:
                projectDict[fix['projectName']] = {}

            bugTypeDict = {k: bugTypeDict[k] for k in sorted(bugTypeDict)}

        for project in projectDict:
            projectDict[project] = {k: projectDict[project][k] for k in sorted(projectDict[project])}

        f.close()
        return bugTypeDict, projectDict


# bugDictionary, projDictionary = DatasetProcessor.GetSstubData()
# print(projDictionary['apache.camel'])

# PlotBarForDict(bugDictionary)
# DatasetProcessor.PlotBarForTwoDict(bugDictionary, projDictionary['apache.camel'])
