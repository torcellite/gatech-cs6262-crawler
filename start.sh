#!/bin/bash

# $1 - URL
FOLDER_NAME='crawled_websites/'`echo $1 | rev | cut -d/ -f1 | rev`'/downloads/requests'

# Create folders
mkdir -p $FOLDER_NAME

# Start request file watcher
inotifywait -m $FOLDER_NAME -e create -e moved_to |
    while read path action file; do
        bash download.sh $FOLDER_NAME/$file &
    done &

# Start crawler
phantomjs crawler.js $1

# Kill request file watcher
ps aux | grep inotifywait | awk '{print $2}' > pid
while read -r PID; do
    kill -9 $PID
done < pid

rm pid
