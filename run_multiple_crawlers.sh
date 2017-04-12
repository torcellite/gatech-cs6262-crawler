#!/bin/bash

##
# Script to run multiple crawler instances on multiple domain lists
##


if [[ $# -ne 1 ]]; then
    echo "Usage is bash run_multiple_crawlers.sh number_of_instances";
    exit 1;
fi

DATE=`date +"%m-%d-%y"`
mkdir -p logs/$DATE
for i in `seq 1 $1`; do
    # domain list file name convention: website_list_[num]
    # standard output file name convention: log_[num]
    # standard error file name convention: log_error_[num]
    bash run_crawler.sh crawl_lists/website_list_$i >> logs/$DATE/log_$i 2>> logs/$DATE/log_error_$i &
done
