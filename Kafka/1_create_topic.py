'''
1. yes | sudo yum install java-1.8.0
2. wget https://archive.apache.org/dist/kafka/2.6.2/kafka_2.12-2.6.2.tgz
3. tar -xzf kafka_2.12-2.6.2.tgz
4. cd kafka_2.12-2.6.2

bin/kafka-topics.sh --create --zookeeper <ZookeeperConnectString> --replication-factor 1 --partitions 1 --topic ApplicationMetricTopic

'''
