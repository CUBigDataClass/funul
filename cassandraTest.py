# -*- coding: utf-8 -*-
'''
This script is the a simple functionality test for querying a local cassandra DB using the
DataStax Python Driver for Apache Cassandra. The driver is a modern, feature-rich and highly
tunable Python client library for Apache Cassandra (1.2+) and DataStax Enterprise (3.1+) using
exclusively Cassandra's binary protocol and Cassandra Query Language v3.

The driver supports Python 2.7, 3.3, and 3.4.

Link to driver repo: https://github.com/datastax/python-driver
Getting started with the driver: http://datastax.github.io/python-driver/getting_started.html '''

from cassandra.cluster import Cluster

'''
The set of IP addresses we pass to the Cluster is simply an initial set of contact points.
After the driver connects to one of these nodes it will automatically discover the rest of the
nodes in the cluster and connect to them, so you don’t need to list every node in your cluster. '''
cluster = Cluster() #default connection is with 127.0.0.1
#cluster = Cluster(['192.168.0.1', '192.168.0.2']) #example for connecting to multiple nodes in cluster

session = cluster.connect()

rows = session.execute('SELECT cluster_name, data_center FROM system.local')
for system_row in rows:
    print system_row.cluster_name, system_row.data_center
    

