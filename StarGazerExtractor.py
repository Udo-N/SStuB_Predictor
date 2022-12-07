import nltk
import git
import os
import requests
import json
import math
from string import ascii_letters
from nltk.corpus import stopwords


def AppendList(fileA, listA):
    fileA.write("[")
    for j in range(0, len(listA)):
        f.write(listA[j])
        if j != len(listA) - 1: f.write(", ")
    fileA.write("]")


GitUser = input("Enter Github Username: ")
PAN = input("Enter your Github Personal Access token: ")                # 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

for subdir, dirs, files in os.walk(os.getcwd() + "/Processed-ReadMe-Files"):
    for k in range(0, len(files)):
        file = files[k]
        f = open("projectStargazers.json")
        fJson = json.load(f)
        f.close()
        if file in fJson:
            print("Stargazers already acquired for", file)
            continue

        print("Now getting stargazers for", file)

        apiUrl = "https://api.github.com/repos/" + "/".join(file.split("."))
        apiUrl = apiUrl.replace("/txt", "")
        print(apiUrl)
        response = requests.get(apiUrl, auth=("Udo-N", PAN))

        if response.status_code != 200:
            print("Error retrieving stargazer url. Status code:", response.status_code)
            if response.status_code == 403:
                print("Status code 403, please try again after an hour")
                break
            continue

        stargazerList = []
        i = 0
        while i < 400:
            i += 1
            stargazerUrl = response.json()['stargazers_url'] + "?per_page=100&page=" + str(i)
            try:
                stargazers = requests.get(stargazerUrl, auth=(GitUser, PAN)).json()
            except TimeoutError:
                i -= 1
                continue

            # if no more stargazers
            if len(stargazers) == 0:
                break

            for stargazer in stargazers:
                stargazerList.append(stargazer['login'])

        with open("projectStargazers.json", "rb+") as tempJson:
            tempJson.seek(-1, os.SEEK_END)
            tempJson.truncate()
            tempJson.seek(-1, os.SEEK_END)
            tempJson.truncate()
            tempJson.seek(-1, os.SEEK_END)
            tempJson.truncate()

        f = open("projectStargazers.json", "a")
        f.write(",\n\t")
        f.write('"' + file + '" : "')
        AppendList(f, stargazerList)
        f.write('"\n}')
        f.close()
        print(len(stargazerList))
