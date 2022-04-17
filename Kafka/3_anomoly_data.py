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

KAFKA_HOST = "b-2.msk-workshop-cluster.ue9jbs.c22.kafka.us-east-1.amazonaws.com:9092,b-1.msk-workshop-cluster.ue9jbs.c22.kafka.us-east-1.amazonaws.com:9092" # Or the address you want
KAFKA_TOPIC = "ApplicationMetricTopic"

number_of_log_messages_to_send = 10000

'''
Step 2 - Create sample data + send it to Kafka 
'''

# Produce a baseline of normal data for the last 6 months
start = datetime.today() - relativedelta(months=+36)
end = datetime.today()

number_of_anomaly_to_create = 90

document_id_start_position = 10000

application_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

client = KafkaClient(hosts = KAFKA_HOST)
topic = client.topics[KAFKA_TOPIC]
    
with topic.get_sync_producer() as producer:
    
    for application_id in application_ids:
        
        anomaly_counter = 0
        
        while anomaly_counter < number_of_anomaly_to_create:
            
            messages_per_anomaly = random.randint(500,1000)
            messages_sent = 0

            while messages_sent < messages_per_anomaly:
    
                eventtime = str(random_date(start, end).strftime('%Y-%m-%d'))
            
                rel_start = eventtime + ' 12:00 AM'
                rel_start_object = datetime.strptime(rel_start, '%Y-%m-%d %I:%M %p')
                
                rel_end = eventtime + ' 12:00 PM'
                rel_end_object = datetime.strptime(rel_end, '%Y-%m-%d %I:%M %p')
            
                random_date(rel_start_object, rel_end_object)
                
                document_id_start_position = document_id_start_position + 1
                
                document = {
                    "message_id": document_id_start_position,
                    "eventtime": str(random_date(start, end).strftime('%Y-%m-%d %I:%M:%S')),
                    "application_id": 'Application ' + str(application_id),
                    "cpu_util": random.randint(85,100),
                    "memory_util": random.randint(1,25),
                    "disk_util": random.randint(1,25)
                }
          
                message = str(document)
                encoded_message = message.encode("utf-8")
                producer.produce(encoded_message)

                messages_sent = messages_sent + 1
            
                print('Application # '+ str(application_id) + '/10 | Anomaly # ' + str(anomaly_counter) + '/' + str(number_of_anomaly_to_create) + ' Messages sent for Anomaly ' + str(anomaly_counter) + ' # ' + str(messages_sent) + '/' + str(messages_per_anomaly))
            
            anomaly_counter = anomaly_counter + 1
            
            