## Description

rta-transient-receiver-kafka is a simplified way for handling VoEvents notices provided in xml format by gcn kafka. 

This program extract the data from the xml file, then writes the notices in a MySQL database and performs several processes for detecting a possible correlation among instruments. Then it sends an email alert to the team for further analysis. 

This program uses the following library as base layer: https://github.com/ASTRO-EDU/rta-transient-receiver 


## Installation

### Singularity container
Singularity 2.6 has been used to create the containers. 

Download the containers:
```
--> TODO
```
Start the container as a service:
```
singularity instance.start kafka_receiver.simg kafka_receiver
```
Start the application:
```
singularity run --app kafka_receiver instance://kafka_receiver $HOME/config.json $HOME/kafka_receiver.log
```
Two log files will be created: 
* the one passed as argument showing a quick summary of the received notices.
* the `$HOME/kafka_receiver_nohup.log` file with more diagnostic informations.

To enter the container with a shell (for debugging purpose I guess):
```
singularity shell instance://kafka_receiver
```

### Manual installation
Check the dependecies of the `rta-transient-receiver` submodule. 

Clone the repository:
```
git clone --recurse-submodules git@github.com:ASTRO-EDU/rta-transient-receiver-kafka.git
```
It is recommended to install the dependencies into a virtual enviromnent. For creating a  virtual enviroment: https://docs.python.org/3/library/venv.html
```
python3 -m venv kafka-env
source kafka-env/bin/activate
cd rta-transient-receiver-kafka
pip install -r rta-transient-receiver/requirements.lock
pip install -r requirements.txt
pip install rta-transient-receiver/
pip install .
```
To run the code from the current folder use the command: 
```
kafkareceiver --config-file /path/to/config.json --log-file /path/to/kafka_receiver.log
```

## Configuration file
A configuration file is mandatory to run the software. It contains the credentials to connect
to the database and the Kafka topics, customize the behaviour of the email sender and decides how to handle the test notices. 
The file `rta-transient-receiver/config.template.json` shows the required key-values pairs.

### Obtaining gcn NASA credentials to connect to the Kafka topics
You can use [this link](https://gcn.nasa.gov/quickstart) for registration and the kafka client credentials generation. 

## Troubleshooting 
* [Kafka producer FAQs](https://gcn.nasa.gov/docs/faq#what-does-the-warning-subscribed-topic-not-available-gcnclassictextagile_grb_ground-broker-unknown-topic-or-partition-mean)
* Runtime exceptions: If an exception occurrs during the excecution the receiver won't stop running. To check if something went wrong in the output files. 

## Build the Singularity images
Singularity 2.6 has been used.

Build the base layer then the second layer:
```
sudo singularity build basic_layer_for_kafka_receiver.simg basic_layer_for_kafka_receiver.recipe
sudo singularity build kafka_receiver.simg kafka_receiver.recipe
```