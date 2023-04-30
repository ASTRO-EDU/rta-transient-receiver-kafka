import json
import argparse
import datetime
from gcn_kafka import Consumer
import voeventparse as vp
from voeventhandler.voeventhandler import VoeventHandler

def removeNotAvailableTopics(subscribeSet, availableVoEventTopics):
    notAvailableTopics = []
    for topic in subscribeSet:
        if topic not in availableVoEventTopics:
            notAvailableTopics.append(topic)
    if len(notAvailableTopics) > 0:
        print("The following topics are not available: ")
        for topic in notAvailableTopics:
            print(topic)
            # remove from subscribeSet to avoid segmentation fault
            subscribeSet.remove(topic)
    return subscribeSet, notAvailableTopics


def main():
    parser = argparse.ArgumentParser(description='Kafka Receiver')
    parser.add_argument('--config-file', type=str, required=True, help='The configuration file')
    parser.add_argument('--log-file', type=str, required=True, help='The path to the output log file')
    args = parser.parse_args()

    # read credential from config file
    with open(args.config_file) as f:
        config = json.load(f)
        client_id = config['kafka_client_id']
        client_secret = config['kafka_client_secret']

    with open(args.log_file, "a") as f:
        f.write(f"{datetime.datetime.now()} Kafka receiver is starting.. \n")

    # consumer creation
    consumer = Consumer(
                    client_id=client_id,
                    client_secret=client_secret,
                    domain='gcn.nasa.gov'
                )


    subscribeSet = config["topics_to_subscribe"]

    voEventAvailableTopics = sorted([topic for topic in consumer.list_topics().topics if "voevent" in topic])

    # check if the topics to subscribe are available
    subscribeSet, notAvailable = removeNotAvailableTopics(subscribeSet, voEventAvailableTopics)

    with open(args.log_file, "a") as f:
        f.write(f"{datetime.datetime.now()} The following topics are not available: {notAvailable}\n")

    # Subscribe to topics and receive alerts
    consumer.subscribe(subscribeSet)

    # class used to perform action when a voevent is recived
    voeventhandle = VoeventHandler(args.config_file)

    with open(args.log_file, "a") as f:
        f.write(f"{datetime.datetime.now()} Kafka receiver is on! \n\n\n")

    while True:

        for message in consumer.consume():
            f = open(args.log_file, "a")
            f.write(f"{datetime.datetime.now()} --------------------------------------------------------------------------------------------- \n")
            try:
                inserted, mail_sent, voeventdata, correlations = voeventhandle.handleVoevent(vp.loads(message.value()))
                f.write(f"Voevent               = {voeventdata}\n") 
                f.write(f"Saved in the database = {inserted}\n") 
                f.write(f"Mail sent             = {bool(mail_sent)}\n") 

            except Exception as e:
                f.write(f"{datetime.datetime.now()} Error: {e}\n\n{message.value()}")

            finally:
                f.write("---------------------------------------------------------------------- \n\n")
                f.close()
            

if __name__ == '__main__':
    main()