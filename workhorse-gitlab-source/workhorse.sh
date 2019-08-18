#!/bin/bash

# Exit if context is not set
if [ -z "$GITLAB_URL" ]; then
  echo GITLAB_URL is not set
  exit 1
fi

if [ -z "$GITLAB_TOKEN" ]; then
  echo GITLAB_TOKEN is not set
  exit 1
fi

if [ -z "$GITLAB_PROJECT" ]; then
  echo GITLAB_PROJECT is not set
  exit 1
fi

while true; do
  python process_queue.py
  echo `date +"%Y-%m-%d %H:%M:%S"`: sleeping
  sleep 10
done  
