#!/usr/bin/env bash

service=$1
password=$ADMIN_PWD

echo "Starting DB"
if [ $service = "webserver" ]
then
  airflow db check
  airflow db init
  airflow users create -e admin@test.com -f admin -l admin -p "$password" -u admin -r Admin
fi
echo "Starting" $service
airflow $service
