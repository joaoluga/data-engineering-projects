#!/usr/bin/env bash

service=$1

dbt_setup () {
  mkdir ~/.dbt
  touch ~/.dbt/profiles.yml
  yq e '.star_schema.target = "dev"' -i ~/.dbt/profiles.yml
  yq e '.star_schema.outputs.dev.type = "postgres"' -i ~/.dbt/profiles.yml
  yq e '.star_schema.outputs.dev.host = "pg_analytics"' -i ~/.dbt/profiles.yml
  yq e '.star_schema.outputs.dev.port = 5432' -i ~/.dbt/profiles.yml
  yq e '.star_schema.outputs.dev.user = "admin"' -i ~/.dbt/profiles.yml
  yq e '.star_schema.outputs.dev.password = "admin"' -i ~/.dbt/profiles.yml
  yq e '.star_schema.outputs.dev.dbname = "analytics"' -i ~/.dbt/profiles.yml
  yq e '.star_schema.outputs.dev.schema = "refined"' -i ~/.dbt/profiles.yml
  yq e '.star_schema.outputs.dev.threads = 5' -i ~/.dbt/profiles.yml

  # shellcheck disable=SC2164
  cd /usr/local/airflow/dbt/star_schema
  if dbt debug ; then
      echo "The 'dbt debug' verification succeeded"
  else
      echo "The 'dbt debug' verification failed. Check if the profiles.yml, project.yml are valid and git is installed"
      exit 1
  fi
}


echo "Starting DB"
if [ $service = "webserver" ]
then
  airflow db check
  airflow db init
  airflow connections add 'pg_analytics' \
      --conn-type 'postgresql' \
      --conn-login 'admin' \
      --conn-password 'admin' \
      --conn-host 'pg_analytics' \
      --conn-port '5432' \
      --conn-schema 'trusted'
  airflow users create -e admin@test.com -f admin -l admin -p admin -u admin -r Admin
else
  echo "Executing DBT setup"
  dbt_setup
fi
echo "Starting" $service
airflow $service
