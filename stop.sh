#!/bin/bash

##
# Clean up script to stop inotifywait for a single instance crawler
##

# Kill request file watcher
ps aux | grep inotifywait | awk '{print $2}' > pid
while read -r PID; do
    kill -9 $PID
done < pid

rm pid
