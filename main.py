'''
NB:
1. This script assumes all json files are ponte configs.
2. Please do not commit the json files to the repository.
'''

# Algorithm:
#   add the corresponding contents of each file into that master
#   dump the master into a json file.
#   make sure the


import glob
import json

USER_REPO_INFO = "userRepoInfo"
COMMITS_IN_CODE = "commitsInCode"
CODES_DB = "codesDB"
AUTO_ENCODERS = "autoencoders"
SOURCE_INFO = "sourcesInfo"
ANNOTATIONS = "annotations"


# This variable works like a filter.
# By default it is an empty string so it will just merge all config files that belong to the the same repo.
# but if you want to merge the configs of a specific repo, just copy the `userRepoInfo` value into this string here
# and run the script
SelectedRepo = ""

MERGED_FILE_NAME = "merged-config.json"
MERGED = {USER_REPO_INFO: SelectedRepo,
          COMMITS_IN_CODE: [],
          CODES_DB: [],
          AUTO_ENCODERS: {
              "onChangeEncoders": [],
              "onSubjectEncoders": [],
              "onDevlogEncoders": []
          },
          SOURCE_INFO: [
              {
                  "id": "devlogCompilation",
                  "type": "devlogCompilation",
                  "name": "Devlog compilation"
              },
          ],
          ANNOTATIONS: []}


def validateConfigKeys(json_data):
    config_keys = json_data.keys()
    if not config_keys:
        return False
    elif USER_REPO_INFO not in config_keys:
        return False
    elif COMMITS_IN_CODE not in config_keys:
        return False
    elif CODES_DB not in config_keys:
        return False
    elif AUTO_ENCODERS not in config_keys:
        return False
    elif SOURCE_INFO not in config_keys:
        return False
    elif ANNOTATIONS not in config_keys:
        return False
    else:
        return True


'''
Returns True if config belongs to the same repo as the others
Else returns false to avoid merging configs of different repos.
'''


def addUserRepoInfo(json_data):

    global MERGED

    repoInfo = json_data[USER_REPO_INFO].strip().lower()

    if MERGED[USER_REPO_INFO] == "":
        # initial assignment
        MERGED[USER_REPO_INFO] = repoInfo
        return True

    elif MERGED[USER_REPO_INFO] == repoInfo:
        # if same, dont bother reassigning
        return True
    else:
        # if different repos, dont merge.
        return False


def mergeCommitsInCode(json_data):
    global MERGED
    if json_data[COMMITS_IN_CODE]:
        MERGED[COMMITS_IN_CODE].extend(json_data[COMMITS_IN_CODE])
        return True


def mergeCodesDB(json_data, prefix):
    global MERGED
    db = json_data[CODES_DB]

    for code in db:
        code[1]["value"] = prefix + "--" + code[1]["value"]

    MERGED[CODES_DB].extend(db)
    return True


def mergeAutoEncoders(json_data, prefix):
    global MERGED

    change = "onChangeEncoders"
    subject = "onSubjectEncoders"
    devlog = "onDevlogEncoders"

    changeEncoders = json_data[AUTO_ENCODERS][change]
    subjectEncoders = json_data[AUTO_ENCODERS][subject]
    devlogEncoders = json_data[AUTO_ENCODERS][devlog]

    for ce in changeEncoders:
        ce["code"] = prefix + "--" + ce["code"]

    for se in subjectEncoders:
        if "code" in se.keys():
            se["code"] = prefix + "--" + se["code"]

    for de in devlogEncoders:
        if "code" in de.keys():
            de["code"] = prefix + "--" + de["code"]

    MERGED[AUTO_ENCODERS][change].extend(changeEncoders)
    MERGED[AUTO_ENCODERS][subject].extend(subjectEncoders)
    MERGED[AUTO_ENCODERS][devlog].extend(devlogEncoders)

    return True


def mergeSourcesInfo(json_data, prefix):
    global MERGED
    # the first element is constant so only extend by the slice [1:]
    if len(json_data[SOURCE_INFO]) > 1:
        sources = json_data[SOURCE_INFO][1:]
        for src in sources:
            src["name"] = prefix + "--" + src["name"]

        MERGED[SOURCE_INFO].extend(sources)
    return True


def mergeAnnotations(json_data, prefix):
    global MERGED
    if json_data[ANNOTATIONS]:

        annotations = json_data[ANNOTATIONS]
        for annotation in annotations:
            annotation["content"] = prefix + ": " + annotation["content"]

        MERGED[ANNOTATIONS].extend(annotations)
        return True


def main():
    global MERGED, MERGED_FILE_NAME

    #   Scan the local folder.
    #   Get the names of all the json fles.
    filenames = [name for name in glob.glob(
        "*.json") if name != MERGED_FILE_NAME]

    for file in filenames:
        with open(file) as f:
            data = json.load(f)
            prefix = file.split(".")[0].capitalize()
            if validateConfigKeys(data):
                if addUserRepoInfo(data):
                    mergeCommitsInCode(data)
                    mergeCodesDB(data, prefix)
                    mergeAutoEncoders(data, prefix)
                    mergeSourcesInfo(data, prefix)
                    mergeAnnotations(data, prefix)
            else:
                print("ERROR: The file " + file.upper() +
                      " does not have all the required keys. Regenerate the file from Ponte.")

    json_file = open(MERGED_FILE_NAME, "w")
    json.dump(MERGED, json_file, indent=4)
    json_file.close()


main()
