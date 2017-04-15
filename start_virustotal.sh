#!/bin/bash

# $1 - date as an input

python vt_prepare_list.py $1

VT_LIST="crawled_websites/$1/vt_list"
echo $VT_LIST

while IFS=$'' read -r line; do
    echo $line
    python virustotal_verify.py $line
done < "$VT_LIST"

python merge.py $1
