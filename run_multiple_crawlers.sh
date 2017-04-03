#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "Usage is bash run_multiple_crawlers.sh number_of_instances";
    exit 1;
fi

for i in `seq 1 $1`; do
    bash run_crawler.sh crawl_lists/website_list_$i &
done
