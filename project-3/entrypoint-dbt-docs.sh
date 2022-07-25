#!/usr/bin/env bash

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
cd /dbt-docs/star_schema
if dbt debug ; then
    echo "The 'dbt debug' verification succeeded"
else
    echo "The 'dbt debug' verification failed. Check if the profiles.yml, project.yml are valid and git is installed"
    exit 1
fi

dbt docs serve --port 5555 --target dev --profiles-dir ~/.dbt --profile star_schema