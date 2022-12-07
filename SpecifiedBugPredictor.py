import os
import time
import json
import requests
import collections
import DatasetProcessor
import ReadMeRelevanceCalculator
import StarRelevanceCalculator
from ReadMeExtractor import getNonMdFileType
from ReadMeExtractor import RemoveStopWords

# InputProject = input("Which project would you like to develop a bug prediction for? (Preferred format: author.projectName.txt) ")
# if InputProject[-4:] != ".txt":
#     InputProject += ".txt"

InputProjectLink = input("Enter Github repository owner and name (using the format '<Repositry_owner>/<Repository_name>'): ")
GitUser = input("Enter your Github username (Hit enter to skip if you do not have a Personal Access Token): ")
if GitUser: PAN = input("Enter your Github Personal Access token: ")

start = time.time()
readMeRawUrl = "https://raw.githubusercontent.com/" + InputProjectLink + "/master/README.md"

response = requests.get(readMeRawUrl)
if response.status_code == 404:
    # TODO: Create list of all projects tat could not have readMe retrieved
    readMeRawUrl = readMeRawUrl.replace("README.md", "readme.md")
    response = requests.get(readMeRawUrl)
    if response.status_code == 404:
        readMeRawUrl = readMeRawUrl.replace("readme.md", "README.MD")
        response = requests.get(readMeRawUrl)

        if response.status_code == 404:
            changedUrl = getNonMdFileType(readMeRawUrl)

            if changedUrl == readMeRawUrl:
                print("Github returned 404. ReadMe file not compatible")
                exit()

            response = requests.get(changedUrl)

f = open('ReadMe-Files/CurrentReadMe.txt', 'w', encoding='utf-8')
f.write(response.text)
f.close()

RemoveStopWords('CurrentReadMe.txt')
print("Now getting stargazers for", InputProjectLink)

apiUrl = "https://api.github.com/repos/" + InputProjectLink

if GitUser: response = requests.get(apiUrl, auth=(GitUser, PAN))
else: response = requests.get(apiUrl)

if response.status_code != 200:
    print("Error retrieving stargazer url. Status code:", response.status_code)
    exit()
    if response.status_code == 403:
        print("Status code 403, please try again after an hour")
        exit()

stargazerList = []
i = 0
while i < 400:
    i += 1
    stargazerUrl = response.json()['stargazers_url'] + "?per_page=100&page=" + str(i)
    try:
        if GitUser: stargazers = requests.get(stargazerUrl, auth=("Udo-N", PAN)).json()
        else: stargazers = requests.get(stargazerUrl).json()
    except TimeoutError:
        i -= 1
        continue

    # if no more stargazers
    if len(stargazers) == 0:
        break

    for stargazer in stargazers:
        stargazerList.append(stargazer['login'])

print("Stargazers:", stargazerList)


for subdir, dirs, files in os.walk(os.getcwd() + "/Processed-ReadMe-Files"):
    DSP = DatasetProcessor.DatasetProcessor()
    SRC = StarRelevanceCalculator.StarRelevanceCalculator()
    RRC = ReadMeRelevanceCalculator.ReadMeRelevanceCalculator()
    bugD, projD = DSP.GetSstubData()

    currentProject = ".".join(InputProjectLink.split("/")) + ".txt"
    cleanedCurrProj = currentProject.replace(".txt", "")
    print("CURRENT PROJECT:", cleanedCurrProj)
    distSum = {}
    for bugType in bugD:
        distSum[bugType] = 0

    for project in files:
        if project == currentProject or project == "CurrentReadMe.txt":
            continue
        print("Now comparing " + currentProject + " to " + project)

        readMeRelevance = RRC.CalculateRelevance("CurrentReadMe.txt", project)

        f = open("projectStargazers.json")
        fJson = json.load(f)
        f.close()
        starRelevance = len(set(fJson[project]).intersection(set(stargazerList))) / len(set(fJson[project]).union(set(stargazerList)))

        projectRelevance = readMeRelevance * starRelevance

        print("Project Relevance:", projectRelevance)

        for bug in bugD:
            try:
                projectBugWeight = projD[project.replace(".txt", "")][bug] * projectRelevance
                distSum[bug] += projectBugWeight
            except KeyError:
                continue

    distSumTotal = sum(distSum.values())

    for key in distSum:
        if distSumTotal != 0:
            distSum[key] = distSum[key]/distSumTotal * 100

    distSum = DSP.SortDictionary(distSum)

    print(distSum)

    with open('tempfile.json', 'w') as projectJson:
        projectJson.write("{\n")
        projectJson.write('\t"Prediction" : [{\n\t\t')
        i = 0
        for key in distSum:
            projectJson.write('"' + key + '" : "' + str(distSum[key]) + '"')
            if i != 15:
                projectJson.write(',\n\t\t')
            else:
                projectJson.write('\n\t}]\n')
            i += 1
        projectJson.write('}')

    distSumCleaned = {}
    newKeys = []
    for key in distSum:
        separatedKey = key.split("_")
        newKey = separatedKey[0][0:2] + '_' + separatedKey[1][0:2]
        if newKey in newKeys and len(separatedKey) > 2:
            newKey += '_' + separatedKey[2][0:2]
        elif newKey in newKeys:
            newKey = separatedKey[0][0:2] + '_' + separatedKey[1][0:3]

        distSumCleaned[newKey] = distSum[key]
        newKeys.append(newKey)

    end = time.time()
    print("Execution time :", str(round((end-start), 2)), "s\n")

    DSP.PlotBarForDict(distSumCleaned)
