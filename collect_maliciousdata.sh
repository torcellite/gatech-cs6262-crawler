#!/bin/bash

find . -type f -name "tmp_dumpurl_*" -print0 |
  while IFS= read -r -d $'\0' line; do
    python collect_maliciousurl_data.py $line
  done
