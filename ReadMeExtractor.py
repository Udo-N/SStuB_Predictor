import nltk
import git
import os
import requests
import json
import math
from string import ascii_letters
from nltk.corpus import stopwords
# nltk.download('stopwords')


# Get list of all projects from SSTUB files
def getProjects(path):
    file = open(path, encoding='utf-8')
    bugFixes = json.load(file)
    file.close()
    projectList = []

    for fix in bugFixes:
        if fix['projectName'] not in projectList:
            projectList.append(fix['projectName'])

    return projectList


# Get README files from list of projects in ProjectList
def getReadMeFiles(projectList):
    for project in projectList:
        print(project)
        try:
            readMeRawUrl = "https://raw.githubusercontent.com/" + project.split('.')[0] + "/" + project.split('.')[1] + "/master/README.md"
        except IndexError:
            print("Format for " + project + " not compatible")
            # countInc += 1
            continue
        except TimeoutError:
            print("Timeout")
            # countTimeout += 1
            continue

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
                        # count404 += 1
                        print("404: " + readMeRawUrl)
                        continue
                    response = requests.get(readMeRawUrl)

        f = open('ReadMe-Files/' + project + '.txt', 'w', encoding='utf-8')
        f.write(response.text)
        f.close()


def getNonMdFileType(url):
    listOfSupportedFileTypes = [".markdown", ".mdown", ".mkdn", ".md", ".textile", ".rdoc", ".org", ".creole", ".mediawiki", ".wiki", ".rst", ".asciidoc", ".adoc", ".asc", ".pod", ".txt"]
    for fileType in listOfSupportedFileTypes:
        newUrl = url.replace("README.MD", "README" + fileType)
        if requests.get(newUrl).status_code == 404:
            newUrl = newUrl.replace("README", "readme")
            if requests.get(newUrl).status_code == 404:
                newUrl = newUrl.replace("readme", "ReadMe")
                if requests.get(newUrl).status_code == 404:
                    continue
        return newUrl
    return url


# Removes stop words from README file and move to new folder
def RemoveStopWords(file):
    with open("ReadMe-Files/" + file, encoding='utf-8') as unprocessedReadMe, open("Processed-ReadMe-Files/" + file, "w+") as processedReadMe:
        for line in unprocessedReadMe:
            if line.strip():
                # Get rid of all Github links
                line = line.replace("https://github.com", "")
                line = line.replace("https", "")
                # Get rid of project name
                line = line.replace(file.split(".")[0], "")
                line = line.replace(file.split(".")[1], "")

                # Get rid of all special characters
                for element in line:
                    if element not in ascii_letters:
                        line = line.replace(element, " ")

                line = line.lower()

                line = line.split()
                for word in line:
                    if word in stopwords.words('english') or word == 'a' or word == 'the':
                        line.remove(word)

                line = " ".join(line)
                processedReadMe.write(line)
                processedReadMe.write('\n')


if __name__ == '__main__':
    if not os.path.exists(os.getcwd() + "/ReadMe-Files"):
        os.mkdir(os.getcwd() + "/ReadMe-Files")

    if not os.path.exists(os.getcwd() + "/Processed-ReadMe-Files"):
        os.mkdir(os.getcwd() + "/Processed-ReadMe-Files")

    listOfProjects = getProjects("sstub_files/sstubsLarge.json")

    getReadMeFiles(listOfProjects)

    ascii_letters += " "
    for subdir, dirs, files in os.walk(os.getcwd() + "/ReadMe-Files"):
        for file in files:
            RemoveStopWords(file)
            print("Stopwords removed for " + file)
