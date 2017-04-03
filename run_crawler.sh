#!/bin/bash
while IFS= read -r line; do
    website=`echo "$line"`
    echo "Crawling "$website
    start_time=`date +%s`
    bash start.sh $website crawled_websites/$website
    end_time=`date +%s`
    time_taken=$((end_time-start_time))
    echo "Crawled "$website" in "$time_taken" seconds" >> log
done < website_list
