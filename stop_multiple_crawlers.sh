#!/bin/bash

# Kill all the crawlers (run_crawler.sh and any straggling start.sh, crawler.js processes)
ps aux | grep -e "run_crawler.sh" -e "crawler.js" -e "start.sh" -e "get_dns.py" -e "inotifywait" | awk '{print $2}' > straggler_pids
while read -r PID; do
    kill -9 $PID
done < straggler_pids
rm straggler_pids

# Echo the completed websites
DATE=`date +"%m-%d-%y"`
for dir in `ls -1 crawled_websites/$DATE/crawl_lists`; do
    ls -1 crawled_websites/$DATE/crawl_lists/$dir
done
