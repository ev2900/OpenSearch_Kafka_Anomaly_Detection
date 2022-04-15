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
    - 

4. Create OpenSearch index

5. Configure Lambda

6. Send data to OpenSearch via. MSK + Lambda

7. Create + run OpenSearch anomaly detector
