#!/bin/bash

# $1 - URL
FOLDER_NAME='crawled_websites'

# Start request file watcher
inotifywait -r -m $FOLDER_NAME -e create -e moved_to |
    while read path action file; do
      if [[ $file == *"request-"* ]]; then
        bash download.sh $path$file &
      fi
    done &

# Start crawler
phantomjs crawler.js $1

# Kill request file watcher
ps aux | grep inotifywait | awk '{print $2}' > pid
while read -r PID; do
    kill -9 $PID
done < pid

rm pid
