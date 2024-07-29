# Ponte Config Merger
Python script for merging ponte config files of multiple people into one. 

Keep in mind that the name of the config file will become the prefix of the tag after merging so name the files as you want the prefix to be. 

Running the tool again will regenerate the file. 

> :warning: The tool merges ALL json files in the folder except the `merged-config.json`. If you rename the `merged-config.json` to something else and run it again, things will get messed up.  

### Pre-requisites 
Must have Python 3 installed in the system.

To check if you have it installed, open the terminal and try `python --version` or `python3 --version`.

If the first one gives you something like `2.x.y` (where x and y are other numbers) then please run the second command and the response **should** be something like `Python 3.x.y` (where x and y are, again, some numbers. in my case it is `3.9.6`)

Depending on which one gave the right response, that is what you should use when running the script. 

If both of these give an error, follow the instructions here: [Download Python](https://www.python.org/downloads/)


### How to use
1. Clone the repo
2. Copy the ponte config files into this folder. 
3. Open a terminal window in the folder. 
4. Run the command `python3 ./main.py` or `python ./main.py` (whichever worked for you earlier)
5. This should give you a `merged-config.json` fie in the directory. Use that with ponte. 
