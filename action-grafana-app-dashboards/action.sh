# !/bin/bash

# make sure the script can be called from anywhere
DIRECTORY=$(cd `dirname $0` && pwd)

# Exit if context is not set
if [ -z "$GRAFANA_API_KEY" ]; then
  echo GRAFANA_API_KEY is not set
  exit 1
fi

if [ -z "$GRAFANA_HOST" ]; then
  echo GRAFANA_HOST is not set
  exit 1
fi

if [ -z "$GRAFANA_USER" ]; then
  echo GRAFANA_USER is not set
  exit 1
fi


if [ -z "$GRAFANA_PWD" ]; then
  echo GRAFANA_PWD is not set
  exit 1
fi

if [ -z "$SOURCE_FOLDER_ID" ]; then
  echo SOURCE_FOLDER_ID is not set
  exit 1
fi

# Exit if arguments are not set
if [ -z "$1" ]; then
  echo arg1 is not set
  exit 1
fi

if [ -z "$2" ]; then
  echo arg2 is not set
  exit 1
fi


python3 ${DIRECTORY}/create_app.py "$1" "$2"
