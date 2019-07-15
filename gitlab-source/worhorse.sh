#!/bin/bash

source setenv

while true; do
  python process_queue.py
  echo ==== sleeping ====
  sleep 10
done  
