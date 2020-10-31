### digit 

Exract Endpoints from Git repository for fuzzing 

### Installation

```
git clone https://github.com/aufzayed/digit
pip3 install -r requirements.txt
```

### Usage

```

________    .___    ________  .______________
\______ \   |   |  /  _____/  |   \__    ___/
 |    |  \  |   | /   \  ___  |   | |    |   
 |    `   \ |   | \    \_\  \ |   | |    |   
/_______  / |___|  \______  / |___| |____|   
        \/                \/                 
    Made with ♥ by Abdelrhman(@aufzayed)

usage: digit.py [-h] [--repo-list] [--output]

optional arguments:
  -h, --help    show this help message and exit
  --repo-list   a file containing a list of repos to extract data from them
  --output      output directory

```

### Example 
 ```
 python3 digit.py --repo-list repo_list_file.txt --output /dir/path
 
 cat repo_list_file.txt | python3 digit.py --output /dir/path
 
 ```
 
 ### Credits
 
thanks for awesom regex by [LinkFinder](https://github.com/GerbenJavado/LinkFinder) team
