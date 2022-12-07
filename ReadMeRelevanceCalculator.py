import math


class ReadMeRelevanceCalculator:
    @staticmethod
    def GetWeightVector(textFile):
        weightVector = {}
        with open("Processed-ReadMe-Files/" + textFile, encoding='utf-8') as currentFile:
            for line in currentFile:
                line = line.split()
                for word in line:
                    try:
                        weightVector[word] += 1
                    except KeyError:
                        weightVector[word] = 1

        try:
            del weightVector['the']
            del weightVector['github']
        except KeyError:
            return weightVector

        return weightVector

    @staticmethod
    def CalculateRootSumSquare(dictionary):
        total = 0
        for weight in dictionary.values():
            total += weight ** 2

        return math.sqrt(total)

    @staticmethod
    def CalculateRelevance(readMe1, readMe2):
        total = 0
        weightVect1 = ReadMeRelevanceCalculator.GetWeightVector(readMe1)
        weightVect2 = ReadMeRelevanceCalculator.GetWeightVector(readMe2)

        rootSumSquare1 = ReadMeRelevanceCalculator.CalculateRootSumSquare(weightVect1)
        rootSumSquare2 = ReadMeRelevanceCalculator.CalculateRootSumSquare(weightVect2)
        productRSS = rootSumSquare1 * rootSumSquare2

        weightSet1 = set(weightVect1)
        weightSet2 = set(weightVect2)

        for intersectingWord in weightSet1.intersection(weightSet2):
            total += weightVect1[intersectingWord] * weightVect2[intersectingWord]

        return total / productRSS
