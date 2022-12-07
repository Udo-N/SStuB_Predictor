**Note: The ReadMe Extractor, Stargazer Extractor and Bug predictor do not need to be run as they each take several hours to execute and the files generated from those scripts are already included in this repository**

# Pre-requirements
- Python 3.10 (May work with some older versions)
- Optional: A GitHub account

# ReadMe Extractor
The ReadMe Extractor is used to extract the ReadMe files of the projects in the `sstub_files/sstbsLarge.json` dataset and remove all the stopwords. 
To execute simply run `ReadMeExtractor.py`. The folders `ReadMe-Files/` and `Processed-ReadMe-Files/` should be cretaed while the script is executing. `ReadMe-Files/` will contain all the ReadMe files while `Processed-ReadMe-Files/` will contain the ReadMe files with the stopwords removed.

# Stargazer Extractor
The Stargazer Extractor is used to extract the list of stargazers for each project into the JSON file `projectStargazers.json`. This program will take several hours to execute and will need to be restarted every few minutes to get past GitHub's rate limiter. A GitHub account is also required to run this script. To execute:
- Make sure to run the ReadMe extractor first if the `Processed-ReadMe-Files/` is empty or does not exist
- Run `StarGazerExtractor.py`
- Enter your GitHub Username
- Enter your personal access token (To learn more about Github personal access tokens, [go here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token))
- Monitor the program every few minutes. When it is done executing, run it again after an hour to see if it has more stargazer information to add to `projectStargazers.json`

# Bug Predictor
This script generates a JSON file for each project in `Processed-ReadMe-Files/` or `projectStargazers.json` and stores them in the `JSONs` folder. The JSON files contain the predicted distribution, the actual distribution and the accuracy of the prediction. This script will also take several hours to execute. 
To run, simply run `BugPredictor.py`. If the JSON file for a project in `Processed-ReadMe-Files/` or `projectStargazers.json` already exists in `JSONs`, then it will be skipped. 

# Specific Bug Predictor
This functions similarly to the bug predictor, but instead of only generating distributions for the projects in `Processed-ReadMe-Files/` or `projectStargazers.json`, it generates distributions for any GitHub repository with a valid ReadMe file. To run:
- Run `SpecifiedBugPredictor.py`
- Enter the GitHub repository you wish to generate a distribution for like this: `<Repositry_owner>/<Repository_name>`
- Optional: Enter your Github Username and Personal Access token (To learn more about Github personal access tokens, [go here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token))
- The program should take 5-6 minutes to execute and a file called `tempfile.json` will be generated containing the predicted distribution along with a bar chart for the distribution