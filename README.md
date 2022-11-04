# telnet_scp_wiki_scraper
## Scraps scp wiki with the specific scp over telnet.

<a title="The original SCP logo was designed by far2, based on a free asset from Adobe Illustrator&#039;s &quot;Mad Science&quot; asset library, which in turn was based on the electrostatic discharge warning symbol. The first high-resolution PNG version of the logo was made by Aelanna, based on the original SCP logo., CC BY-SA 3.0 &lt;https://creativecommons.org/licenses/by-sa/3.0&gt;, via Wikimedia Commons" href="https://commons.wikimedia.org/wiki/File:SCP_Foundation_(emblem).svg"><img width="128" alt="SCP Foundation (emblem)" src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/SCP_Foundation_%28emblem%29.svg/128px-SCP_Foundation_%28emblem%29.svg.png"></a>

It creates a telnet-server that makes it look like an old SCP Foundation Database. In reality, it just asks for the specific SCP name or ID and search it in the https://scp-wiki.wikidot.com/ Website.


## Installation
1. Check if you have latest version of Python 3 (im using python 3.8.10).<br>
    If you dont have the latest version of Python 3 or you dont have Python at all then go to the Python Website (https://www.python.org/) and Download it
2. Clone or download the Project in your local Maschine. <br>
    for clone ```git clone <project url here>``` (it must be done in the project folder)
3. Install all the Requirements for the Project by typing this in the Terminal ```pip install -r requirements.txt```
4. Start the Server with ```python3 main.py```

## Using it
If you want to change the default telnet port (23) to something else, then it must be done in the environment.
- UNICODE: str (default ascii)


## Docker Version
1. Clone or download the Project in your local Maschine. <br>
    for clone ```git clone <project url here>```

2. Build the docker image in the Terminal ```docker build . -t telnet_scp``` (it must be done in the project folder)

3. Run the build image with ```docker run telnet_scp```

## Setting up a work environment
1. Check if you have latest version of Python 3 (im using python 3.8.10).<br>
    If you dont have the latest version of Python 3 or you dont have Python at all then go to the Python Website (https://www.python.org/) and Download it
2. Install all the Requirements for the Project by typing this in the Terminal ```pip install -r requirements.txt``` (it must be done in the project folder)

## Bug reports
In case of a bug that you like to report to me or to the comunity then do it on the Issues Tap.


## TODOS/IDEAD
- [ ] Add a cache system in tmp folder, for caching the scp report text.