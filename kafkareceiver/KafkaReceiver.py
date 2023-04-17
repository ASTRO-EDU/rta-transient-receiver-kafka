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
    parser.add_argument('--kafka-config-file',           type=str, required=True, help='Kafka configuration file')
    parser.add_argument('--voevent-handler-config-file', type=str, required=True, help='Voevent handler configuration file')
    parser.add_argument('--log-file', type=str, required=True, help='Log file position')
    args = parser.parse_args()

    # read credential from config file
    with open(args.kafka_config_file) as f:
        config = json.load(f)
        client_id = config['client_id']
        client_secret = config['client_secret']

    with open(args.log_file, "a") as f:
        f.write(f"{datetime.datetime.now()} Kafka receiver is starting.. \n")
    print(f"{datetime.datetime.now()} Kafka receiver is starting.. \n")

    # consumer creation
    consumer = Consumer(
                    client_id=client_id,
                    client_secret=client_secret,
                    domain='gcn.nasa.gov'
                )

    # set of topics to subscribe
    # can be found the entire list during the client credentials creation at https://gcn.nasa.gov/quickstart
    # only for testing purpose, the topic 'gcn.classic.voevent.LVC_TEST' send a periodic voevent 
    subscribeSet = [    
        'gcn.classic.voevent.AGILE_MCAL_ALERT',
        'gcn.classic.voevent.FERMI_GBM_FLT_POS',
        'gcn.classic.voevent.FERMI_LAT_MONITOR',
        'gcn.classic.voevent.FERMI_LAT_OFFLINE',
        #'gcn.classic.voevent.ICECUBE_ASTROTRACK_BRONZE',
        #'gcn.classic.voevent.ICECUBE_ASTROTRACK_GOLD',
        'gcn.classic.voevent.INTEGRAL_OFFLINE',
        'gcn.classic.voevent.INTEGRAL_REFINED',
        'gcn.classic.voevent.INTEGRAL_WAKEUP',
        'gcn.classic.voevent.LVC_INITIAL',
        'gcn.classic.voevent.LVC_PRELIMINARY',
        'gcn.classic.voevent.MAXI_KNOWN',
        'gcn.classic.voevent.MAXI_UNKNOWN',
        'gcn.classic.voevent.SWIFT_BAT_QL_POS',
        'gcn.classic.voevent.KONUS_LC'
    ]

    voEventAvailableTopics = sorted([topic for topic in consumer.list_topics().topics if "voevent" in topic])

    # check if the topics to subscribe are available
    subscribeSet, notAvailable = removeNotAvailableTopics(subscribeSet, voEventAvailableTopics)

    with open(args.log_file, "a") as f:
        f.write(f"{datetime.datetime.now()} The following topics are not available: {notAvailable}\n")
    print(f"{datetime.datetime.now()} The following topics are not available: {notAvailable}\n")

    # Subscribe to topics and receive alerts
    consumer.subscribe(subscribeSet)

    # class used to perform action when a voevent is recived
    voeventhandle = VoeventHandler(args.voevent_handler_config_file)

    with open(args.log_file, "a") as f:
        f.write(f"{datetime.datetime.now()} Kafka receiver is on \n")
    print(f"{datetime.datetime.now()} Kafka receiver is on \n")

    while True:

        for message in consumer.consume():
        
            f = open(args.log_file, "a")
            try:
                voeventdata = voeventhandle.handleVoevent(vp.loads(message.value()))
                f.write(f"{datetime.datetime.now()} VoEvent: {voeventdata}") # use a logger!
                print(f"{datetime.datetime.now()} VoEvent: {voeventdata}")

            except Exception as e:
                f.write(f"{datetime.datetime.now()} Error: {e}")
                print(f"{datetime.datetime.now()} Error: {e}")

            finally:
                f.write("----------------------- \n\n")
                f.close()
            

if __name__ == '__main__':
    main()