#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "Usage is bash run_crawler.sh website_list";
    exit 1;
fi

DATE=`date +"%m-%d-%y"`

while IFS= read -r line; do
    # Check flag to continue
    if [[ -f stop_crawling ]]; then
	exit 2;
    fi
    # Strip new line character
    website=`echo "$line"`
    echo "Crawling "$website
    start_time=`date +%s`
    bash start.sh $website crawled_websites/$DATE/$1/$website
    end_time=`date +%s`
    time_taken=$((end_time-start_time))
    echo "Crawled "$website" from "$1" in "$time_taken" seconds"
done < $1
