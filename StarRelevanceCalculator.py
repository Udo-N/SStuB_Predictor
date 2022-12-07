import json


class StarRelevanceCalculator:
    @staticmethod
    def CalculateRelevance(project1, project2):
        f = open("projectStargazers.json")
        fJson = json.load(f)
        f.close()
        relevance = len(set(fJson[project1]).intersection(set(fJson[project2]))) / len(set(fJson[project1]).union(set(fJson[project2])))
        return relevance
