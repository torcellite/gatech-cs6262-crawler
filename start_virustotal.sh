#!/bin/bash

# $1 - date as an input

find crawled_websites/$1 -type f -name "tmp_dumpurl_*" -print0 |
  while IFS= read -r -d $'\0' line; do
    echo $line
    python virustotal_verify.py $line
  done

python concat.py $1
