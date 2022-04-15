'''
--------------
Prerequisite
--------------

1. Installed the required python packages 
    a. pip install pykafka

'''

import threading
import random

from datetime import datetime
from random import randrange
from datetime import timedelta
from pykafka import KafkaClient

from dateutil.relativedelta import relativedelta

# Define functions to be used later in the code ...
def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

'''
Step 1 - Update KAFKA_HOST with bootstrap servers URLs
         Update KAFKA_TOPIC with the name of the a topic
         Update number_of_log_messages_to_send with the number of messages you want to send to Kafka
'''

KAFKA_HOST = "b-2.msk-workshop-cluster.dh9wkw.c24.kafka.us-east-1.amazonaws.com:9092,b-1.msk-workshop-cluster.dh9wkw.c24.kafka.us-east-1.amazonaws.com:9092" # Or the address you want
KAFKA_TOPIC = "ApplicationMetricTopic"

number_of_log_messages_to_send = 10000

'''
Step 2 - Create sample data + send it to Kafka 
'''

# Produce a baseline of normal data for the last 6 months
start = datetime.today() - relativedelta(months=+36)
end = datetime.today()
count = 0

# print(message)

client = KafkaClient(hosts = KAFKA_HOST)
topic = client.topics[KAFKA_TOPIC]
    
with topic.get_sync_producer() as producer:
    
    for i in range(number_of_log_messages_to_send):
        
        message_for_kafka = {
            "message_id": count,
            "eventtime": str(random_date(start, end).strftime('%Y-%m-%d %I:%M:%S')),
            "application_id": 'Application ' + str(random.randint(1,10)),
            "cpu_util": random.randint(1,25),
            "memory_util": random.randint(1,25),
            "disk_util": random.randint(1,25)
        }
        
        message = str(message_for_kafka)
        encoded_message = message.encode("utf-8")
        producer.produce(encoded_message)

        print("# " + str(count) + " | Message sent to Kafka | " + str(message_for_kafka))
        
        count = count + 1
        
'''
Helpful notes:

* Kafka has a set of scripts that can be run from the CLI. These are useful for common operations (create topic, console consmer + producer). To install the tools follow the steps below

1. sudo yum install java-1.8.0
2. wget https://archive.apache.org/dist/kafka/2.6.2/kafka_2.12-2.6.2.tgz
3. tar -xzf kafka_2.12-2.6.2.tgz
4. cd kafka_2.12-2.6.2

* Example - Console cosumer

1. cd kafka_2.12-2.6.2/bin/ folder
1. Create client.properties file
2. Put the following in the client.properties

    security.protocol=PLAINTEXT

3. Run the command below

    ./kafka-console-consumer.sh --bootstrap-server <BootstrapBrokerConnectString> --consumer.config client.properties --topic <TopicName>

'''