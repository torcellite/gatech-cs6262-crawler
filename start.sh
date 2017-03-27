#!/bin/bash

# $1 - URL
# $2 - Root directory

mkdir -p $2

# Start request file watcher
inotifywait -r -m $2 -e create -e moved_to |
    while read path action file; do
      if [[ $file == *"request-"* ]]; then
        bash download.sh $path$file &
      fi
      # Start collecting DNS data
      if [[ $file == "resources.json" ]]; then
        python get_dns.py $path &
      fi
    done &

# Start crawler
phantomjs crawler.js $1 $2

# Wait a bit before killing inotifywait,
# so that get_dns.py is fired when resources.json is created
sleep 5;

# Kill request file watcher
ps aux | grep inotifywait | awk '{print $2}' > pid
while read -r PID; do
    kill -9 $PID
done < pid

rm pid
