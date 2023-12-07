# Kafka OpenSearch Anomaly Detection Demo

<img width="275" alt="map-user" src="https://img.shields.io/badge/cloudformation template deployments-76-blue"> <img width="85" alt="map-user" src="https://img.shields.io/badge/views-605-green"> <img width="125" alt="map-user" src="https://img.shields.io/badge/unique visits-200-green">

## Architecture

<img width="900" alt="OpenSearch_demo_Architecture" src="https://github.com/ev2900/Kafka_OpenSearch_Anomaly_Detection/blob/main/Architecture/msk_lambda_opensearch.png">

## Instructions

1. Launch CloudFormation stack

    [![Launch CloudFormation Stack](https://sharkech-public.s3.amazonaws.com/misc-public/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=msk-lambda-opensearch&templateURL=https://sharkech-public.s3.amazonaws.com/misc-public/msk_lambda_opensearch.yaml)

2. Update msk security group to allow inbound traffic from Cloud9 security group

    - Navigate to [Security Group](https://us-east-1.console.aws.amazon.com/vpc/home?region=us-east-1#securityGroups:) page in the AWS console
    - Select ```msk security group```
    - Add inbound bound rule allowing all traffic from the **aws-cloud9** security group

3. Create Kafka topic

    - Navigate to [Cloud9](https://us-east-1.console.aws.amazon.com/cloud9/home?region=us-east-1#) page in the AWS console
    - Open IDE for the msk-workshop-cloud9 enviorment
    - Follow the instructions in [Kafka/1_create_topic.py](https://github.com/ev2900/Kafka_OpenSearch_Anomaly_Detection/blob/main/Kafka/1_create_topic.py)

4. Create OpenSearch index

    - via. Cloud9 update the required section(s) and run [OpenSearch/1_create_index.py](https://github.com/ev2900/Kafka_OpenSearch_Anomaly_Detection/blob/main/OpenSearch/1_create_index.py)

5. Configure Lambda

    - Navigate to [lambda](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/msk-os-lambda?tab=code) function page in the AWS console

    - Create a lambda function
        - Funcation name = ```msk-os-lambda```
        - Runtime = ```python 3.7```
        - Architecture = ```x86_64```
        - Permissions, Execution role = Use an existing role ```Lambda-MSK-OpenSearch-Role```

    - Add MSK trigger
        - MSK cluster = ```msk-cluster-workshop```
        - Batch size = ```500```
        - Batch window = ```30```
        - Topic name = ```ApplicationMetricTopic```
        - Starting position = ```Latest```

    - Add code
        - Copy and past the code from [Lambda/1_lambda_function_code_batch.py](https://github.com/ev2900/Kafka_OpenSearch_Anomaly_Detection/blob/main/Lambda/1_lambda_function_code_batch.py) into the code section of the lambda function
        - Update the ```os_url``` variable in the lambda code with the domain endpoint of the OpenSearch cluster deployed by the CloudFormation stack
        - Deploy the lambda function

6. Send data to OpenSearch

    - Navigate to [Cloud9](https://us-east-1.console.aws.amazon.com/cloud9/home?region=us-east-1#) page in the AWS console

    - Send base data via. Cloud9. Update the required section(s) and run [Kafka/2_base_data.py](https://github.com/ev2900/Kafka_OpenSearch_Anomaly_Detection/blob/main/Kafka/2_base_data.py)

    - Send anomoly data via. Cloud9. Update the required section(s) and run [Kafka/3_anomoly_data.py](https://github.com/ev2900/https://github.com/ev2900/Kafka_OpenSearch_Anomaly_Detection/blob/main/Kafka/3_anomoly_data.py)

7. Create + run OpenSearch anomaly detector

    - via. Cloud9 update the required section(s) and run [OpenSearch/3_create_anomoly_detector.py](https://github.com/ev2900/Kafka_OpenSearch_Anomaly_Detection/blob/main/OpenSearch/3_create_anomoly_detector.py)

8. Login to the OpenSeach dashboard, navigate to the anomoly detection section. Explore the anomolies OpenSearch detected

## Future Improvements Planned for this Repository
* Automate more of the set up ie. try to minimize the number of steps in the instructions
