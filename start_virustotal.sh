#!/bin/bash

##
#script to trigger virus total verification script
#that checks if the downloaded file is malicious on a given date
#
#Merge all the data into a single file on a per day basis
##

# $1 - date as an input

python vt_prepare_list.py $1

VT_LIST="crawled_websites/$1/vt_list"
echo $VT_LIST

while IFS=$'' read -r line; do
    echo $line
    python virustotal_verify.py $line
done < "$VT_LIST"

#trigger the merge script to combine all the data into a single file
python merge.py $1
