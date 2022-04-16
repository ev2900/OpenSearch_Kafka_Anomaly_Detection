# Kafka OpenSearch Anomaly Detection Demo

## Architecture

## Instructions

1. Launch CloudFormation stack

2. Update msk security group to allow inbound traffic from the Cloud9 security group

    - Navigate to the [Security Group](https://us-east-1.console.aws.amazon.com/vpc/home?region=us-east-1#securityGroups:) page in the AWS console
    - Select the ```msk security group```
    - Add an inbound bound rule allowing all traffic from the aws-cloud9 security group

3. Create Kafka topic

    - Navigate to the [Cloud9](https://us-east-1.console.aws.amazon.com/cloud9/home?region=us-east-1#) page in the AWS console
    - Open IDE for the msk-workshop-cloud9 enviorment
    - Follow the instructions in [Kafka/1_create_topic.py](https://github.com/ev2900/Kafka_OpenSearch_Anomaly_Detection/blob/main/Kafka/1_create_topic.py)

4. Create OpenSearch index

    - via. Cloud9 **update** the required sections and run [OpenSearch/1_create_index.py](https://github.com/ev2900/Kafka_OpenSearch_Anomaly_Detection/blob/main/OpenSearch/1_create_index.py)

5. Configure Lambda

    - Add MSK trigger to the Lambda
        - MSK cluster = ```msk-cluster-workshop```
        - Batch size = ```100```
        - Batch window = ```15```
        - Topic name = ```ApplicationMetricTopic```
        - Starting position = ```Latest```   
    
    - Update the ```os_url``` variable in the Lambda code with the domain endpoint of the OpenSearch cluster deployed by the CloudFormation stack  

6. Send data to OpenSearch via. MSK + Lambda

    - Send base data

    - Send anomoly data

7. Create + run OpenSearch anomaly detector
