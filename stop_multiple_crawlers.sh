#!/bin/bash

# Kill all the crawlers (run_crawler.sh and any straggling crawler.js processes)
ps aux | grep -e "run_crawler.sh" -e "crawler.js" | awk '{print $2}' > crawler_pids
while read -r PID; do
    kill -9 $PID
done < crawler_pids

rm crawler_pids

# Kill all inotify events
ps aux | grep inotifywait | awk '{print $2}' > pid
while read -r PID; do
    kill -9 $PID
done < pid

rm pid

# Echo the completed websites
DATE=`date +"%m-%d-%y"`
for dir in `ls -1 crawled_websites/$DATE/crawl_lists`; do
    ls -1 crawled_websites/$DATE/crawl_lists/$dir
done
