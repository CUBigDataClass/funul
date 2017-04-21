#!/bin/bash
/opt/kafka/bin/zookeeper-server-start.sh /opt/kafka/config/zookeeper.properties
/opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/server.properties