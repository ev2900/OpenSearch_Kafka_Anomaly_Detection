# --------------
# Prerequisite
# --------------
# If you have not already installed the requests package and/or the json package 
# a. pip install requests
# b. pip install json

import requests
import json
import datetime

from datetime import datetime
from random import randrange
from datetime import timedelta
from dateutil.relativedelta import relativedelta

# Define functions to be used later in the code ...
def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

# --------------
# Step 1 - Update this URL with your domain endpoint
# --------------
os_url = 'https://search-workshop-domain-77uiopkggujcnt6dfn7fcena6m.us-east-1.es.amazonaws.com'

# --------------
# Step 2 - Create anomoly detector
# --------------
create_detector_body = {
  "name": "high-cpu",
  "description": "High CPU Anomaly Detector",
  "time_field": "eventtime",
  "indices": [
    "infa-logs*"
  ],
  "feature_attributes": [
    {
      "feature_name": "test",
      "feature_enabled": True,
      "aggregation_query": {
        "test": {
          "sum": {
            "field": "cpu_util"
          }
        }
      }
    }
  ],
  "detection_interval": {
    "period": {
      "interval": 1440,
      "unit": "Minutes"
    }
  },
  "window_delay": {
    "period": {
      "interval": 1,
      "unit": "Minutes"
    }
  },
  "category_field": [
    "application_id"
  ]
}

create_detector_r = requests.post(os_url + '/_plugins/_anomaly_detection/detectors', auth=('OSMasterUser', 'AwS#OpenSearch1'), headers= {'Content-type': 'application/json'}, data=json.dumps(create_detector_body))

print('------ Created an anomoly detector ------')
print(create_detector_r.text)

create_detector_r_json = create_detector_r.json()

# --------------
# Step 3 - Histroical analysis
# --------------

now_seconds_since_epoch = int((datetime.now().strftime("%s"))) * 1000
thrity_six_months_ago_seconds_since_epoch = int(((datetime.today() - relativedelta(months=+36)).strftime("%s"))) * 1000

#print(now_seconds_since_epoch)
#print(thrity_six_months_ago_seconds_since_epoch)

train_body = {
  "start_time": thrity_six_months_ago_seconds_since_epoch,
  "end_time": now_seconds_since_epoch
}

#print(os_url + '/_plugins/_anomaly_detection/detectors/' + str(create_detector_r_json['_id']) + '/_start')

train_detector_r = requests.post(os_url + '/_plugins/_anomaly_detection/detectors/' + str(create_detector_r_json['_id']) + '/_start', auth=('OSMasterUser', 'AwS#OpenSearch1'), headers= {'Content-type': 'application/json'}, data=json.dumps(train_body))

print('------ Started historical analysis ------')
print(train_detector_r.text)

# --------------
# Step 4 - Real-time detector
# --------------

real_time_detector_r = requests.post(os_url + '/_plugins/_anomaly_detection/detectors/' + str(create_detector_r_json['_id']) + '/_start', auth=('OSMasterUser', 'AwS#OpenSearch1'), headers= {'Content-type': 'application/json'})

print('------ Started real-time detector ------')
print(real_time_detector_r.text)