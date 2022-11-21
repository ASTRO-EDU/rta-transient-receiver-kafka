## Description

rta-transient-receiver-kafka is a simplified way for handling VoEvents notices provided in xml format by gcn kafka. 
The program extract the data from the xml file, then writes the notices in a MySQL database and performs several processes for detecting a possible correlation among instruments. Then it sends an email alert to the team for further analysis. 
More information about how the incoming voevent is manipulated can be found in the repo: https://github.com/ASTRO-EDU/rta-transient-receiver 

## Download
This repo contain a submodule so, clone the repo then download the submodules
```
git clone git@github.com:ASTRO-EDU/rta-transient-receiver-kafka.git
git submodule update --init --recursive
```

## Installation

The dependencies are listed in the file requirement.txt. It is recommended to install them into a virtual enviromnent.

For creating and install a new virtual enviroment: https://docs.python.org/3/library/venv.html

### Obtaining gcn nasa credentials
Obtaining gcn nasa credential is really easy. You can use the link https://gcn.nasa.gov/quickstart for registration and gcn kafka client credential generation. 

### Steps for installation:
First of all is important fill the 2 config.json template with the required information. You can find this file in the path 
```
kafkareceiver/config/config.json (requires gcn kafka logins informations)
rta-transient-receiver/voeventhandler/config/config.json (requires email and databases informations)
```

Then create a new virtual enviroment in a folder (for example) named venv whith the following command:
```
python3 -m venv venv
```
Now activate the virtual enviroment whit the command:
```
source venv/bin/activate
```
Then install the dependency contained in the file requirements.txt in the new virtual enviroment.
```
pip install -r rta-transient-receiver/requirements.txt
pip install -r requirements.txt
```
And use the following command for excecute the file setup.py contained in the voeventhandler folder
```
pip install rta-transient-receiver/
```
## Run code
For run the code from the current folder use the command: 
```
python3 kafkareceiver/kafkareceiver.py
```
Seing the displayed error: "Subscribed topic not available: *topic* : Broker: Unknown topic or partition" is normal and is something related to the gcn kafka working. 
You can find more information at the link: https://gcn.nasa.gov/docs/faq#what-does-the-warning-subscribed-topic-not-available-gcnclassictextagile_grb_ground-broker-unknown-topic-or-partition-mean

## Important email
The code provides a special function for establish if a voevent is important and sholud be marked in a special way during the email notification. You can find this function in the path voeventhandler/emailnotifier.py and it's name is is_important(). From deafault configuration this class return False, but you can build yuor own rule creating conditional operations usign the field of the voeventdata object.  For a fast look to what this field are look at the class voeventdata contained at path kafkareceiver/voeventhandler/emailnotifier.py.  The important email subject tag can be modified in the config file.

## Exceptions during excecution
If an exception occurre during excecution of the voevent handling the receiver won't stop running.
For checkong if something went wrong during excecution is been created a file in the path kafkareceiver/log/log.txt. 