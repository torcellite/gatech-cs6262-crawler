#!/bin/bash

# $1 - Request file name
METHOD=`head -n 1 $1`
URL=`head -n 2 $1 | tail -n 1`
HEADERS=`tail -n +3 $1`
DOWNLOAD_FOLDER=`echo $1 | cut -d/ -f1-3`
DOWNLOAD_FILE=`echo $URL | rev | cut -d/ -f1 | rev`

curl -X $METHOD -H "$HEADERS" -o $DOWNLOAD_FOLDER/$DOWNLOAD_FILE  $URL > /dev/null 2>&1
echo 'Downloaded '$DOWNLOAD_FILE' based on '$1
