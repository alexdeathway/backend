#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


cd /app/vanderval
#python3 manage.py collectstatic --noinput
python3 manage.py makemigrations
python manage.py migrate

if [[ "$DEBUG" == "True" ]]; then
  if [ -f "db.json" ]; then
    echo "Loading dummy database..."
    python manage.py loaddata --exclude auth.permission --exclude contenttypes db.json
  else
    echo "looks like there is no dummy database or fixture to load..."
  fi
else
  echo "This is not a drill...."
fi

exec "$@"
