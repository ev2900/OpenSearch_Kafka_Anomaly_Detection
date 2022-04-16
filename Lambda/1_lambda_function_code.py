import json
import base64
import re
import urllib3
import time

def lambda_handler(event, context):
       
    # Decode Kafka message(s)
    partition0 = event['records']
    messages_raw = partition0['ApplicationMetricTopic-0']

    print('Batch size = ' + str(len(messages_raw)) + ' messages')

    for message_raw in messages_raw:
        
        topic = message_raw['topic']
        partition = message_raw['partition']
        offset = message_raw['offset']
        timestamp = message_raw['timestamp']
        timestampType = message_raw['timestampType']
        value = message_raw['value']
                        
        decoded_b64_message_value = base64.b64decode(value)
        decoded_utf8_message_value = decoded_b64_message_value.decode("utf-8")
                        
        decoded_utf8_message_value_dict = json.loads(decoded_utf8_message_value.replace("'", "\""))
        
        print('Raw message from Kafak = ' + str(decoded_utf8_message_value_dict))
        
        # Send message(s) to OpenSearch
                    
        http = urllib3.PoolManager()
                    
        os_url = 'https://search-workshop-domain-mi3d4ubsmispfgpeuchzrdbzna.us-east-1.es.amazonaws.com'
                            
        insert_document_r_body = {
          "eventtime": decoded_utf8_message_value_dict['eventtime'],
          "application_id": decoded_utf8_message_value_dict['application_id'],
          "cpu_util": int(decoded_utf8_message_value_dict['cpu_util']),
          "memory_util": int(decoded_utf8_message_value_dict['memory_util']),
          "disk_util": int(decoded_utf8_message_value_dict['disk_util'])
        }
        
        print('Processing message # ' + str(decoded_utf8_message_value_dict['message_id']))
        
        full_url = os_url + '/infa-logs-1/_doc/' + str(decoded_utf8_message_value_dict['message_id'])

        print('Request URL = ' + full_url)
        print('Request body = ' + str(insert_document_r_body))
            
        auth_header = urllib3.make_headers(basic_auth='OSMasterUser:AwS#OpenSearch1')
        
        resp = http.request(
            'PUT',
            full_url,
            body=json.dumps(insert_document_r_body),
            headers={'Content-Type': 'application/json', 'authorization': auth_header['authorization']}
        )
        
        print('Request sent!')
        print('Response status = ' + str(resp.status))
        print(resp.headers)
        print('Response body = ' + str(resp.data.decode('utf-8')))
        
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }