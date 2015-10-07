#!/bin/bash

targetServer="$1"
app="$2"

echo "Health Checking $targetServer for $app "

url="http://$targetServer:8080/$app/healthcheck"

response_colon_status_code=`curl -s $url -w ':%{http_code}'`

status_code=`echo $response_colon_status_code | sed 's/^.*:\([[:digit:]]*\)$/\1/'`

response=`echo $response_colon_status_code | sed 's/:[[:digit:]]*$//'`

healthcheck="PASSED"

if [ "$status_code" != "200" ]
then
   echo "Healthcheck failed for $url, expected status '200' but got '$status_code'"
   healthcheck="FAILED"
fi

if [ "$response" != "OK" ]
then
   echo "Healthcheck failed for $url, expected response 'OK' but got '$response'"
   healthcheck="FAILED"
fi

if [ "$healthcheck" == "FAILED" ]
then
   exit 1
fi

echo "Health Check OK"
