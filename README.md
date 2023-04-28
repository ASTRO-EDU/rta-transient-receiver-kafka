## Description

rta-transient-receiver-kafka is a simplified way for handling VoEvents notices provided in xml format by gcn kafka. 

This program extract the data from the xml file, then writes the notices in a MySQL database and performs several processes for detecting a possible correlation among instruments. Then it sends an email alert to the team for further analysis. 

This program uses the following library as base layer: https://github.com/ASTRO-EDU/rta-transient-receiver 


## Installation

### Singularity container
[Singularity 2.6](https://docs.sylabs.io/guides/2.6/user-guide/quick_start.html) has been used to create the containers. 

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

Singularity 2.6 will automatically bind the following directories: $HOME,/tmp,/proc,/sys,/dev; If you want to specify a different path for the log file you have to bind it during the start of the container service: 
```
singularity instance.start -B output/dir/for/kafka:/output kafka_receiver.simg kafka_receiver
singularity run --app kafka_receiver instance://kafka_receiver $HOME/config.json /output/kafka_receiver.log
```

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
To run start the deamon use command: 
```
nohup kafkareceiver --config-file /path/to/config.json --log-file /path/to/kafka_receiver.log > /path/to/kafka_receiver_nohup.log 2>&1 &
```

## Configuration file
A configuration file is mandatory to run the software. It contains the credentials to connect
to the database and the Kafka topics, customize the behaviour of the email sender and decides how to handle the test notices. 
The file `rta-transient-receiver/config.template.json` shows the required key-values pairs.

* Section 1: Database
    * `database_user`: the username to connect to the database.
    * `database_password`: the password to connect to the database.
    * `database_host`: the host of the database.
    * `database_port`: the port of the database.
    * `database_name`: the name of the database.
    * `disable_test_notices_seconds`: the number of seconds to wait before processing the test notices.
* Section 2: Email sender
    * `enabled`: if true the email sender is enabled.
    * `packet_with_email_notification`: if true the email sender is enabled for the packet with the given id.
    * `skip_ligo_test`: if true the email sender is disabled for the notices with the ligo test flag.
    * `skip_ste`: if true the email sender is disabled for the notices with the sub-threshold flag (i.e. not-significant for LIGO).
    * `sender_email`: the email address of the sender.    
    * `sender_email_password`: the password of the sender email.  
    * `email_receivers`: the list of the email receivers.
    * `developer_email_receivers`: an email is sent to this list if any runtime exception occurs.
* Section 3: Brokers
    * You can use [this link](https://gcn.nasa.gov/quickstart) for registration and the kafka client credentials generation.
    * `kafka_client_id`: the client id to connect to the Kafka topics.
    * `kafka_client_secret`: the client secret to connect to the Kafka topics.
    * `topics_to_subscribe`: the list of the topics to subscribe.
 

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