#!/bin/bash

REDIS_PRC_BASE=/cs/redis-prc
REDIS_CLI=$REDIS_PRC_BASE/bin/redis-cli

# Get the proper config file based on service name
CONFIG_FILE="$REDIS_PRC/etc/redis.conf"

# Use awk to retrieve host, port from config file
HOST=`awk '/^[[:blank:]]*bind/ { print $2 }' $CONFIG_FILE | tail -n1`
PORT=`awk '/^[[:blank:]]*port/ { print $2 }' $CONFIG_FILE | tail -n1`
PASS=`awk '/^[[:blank:]]*requirepass/ { print $2 }' $CONFIG_FILE | tail -n1`

HOST=${HOST:-127.0.0.1}
PORT=${PORT:-6379}

# Setup additional parameters
# e.g password-protected redis instances
[ -z "$PASS"  ] || ADDITIONAL_PARAMS="-a $PASS"

$REDIS_CLI -h $HOST -p $PORT $ADDITIONAL_PARAMS shutdown
