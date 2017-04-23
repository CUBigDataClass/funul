#!/bin/bash
nohup /home/ec2-user/kafka_producer.py > /home/ec2-user/kafka_producer.log 2>&1 &
nohup /home/ec2-user/kafka_consumer.py > /home/ec2-user/kafka_consumer.log 2>&1 &
