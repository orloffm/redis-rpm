#!/bin/bash

echo Running as $(whoami).
echo Logs dir:
ls -l /cs/prcuser/redis/log

REDIS_PRC_BASE=/cs/redis-prc

$REDIS_PRC_BASE/bin/redis-server $REDIS_PRC_BASE/etc/redis.conf
