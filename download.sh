#!/bin/bash

# $1 - Request file name
METHOD=`head -n 1 $1`
URL=`head -n 2 $1 | tail -n 1`
HEADERS=`tail -n +3 $1`
DOWNLOAD_FOLDER=`echo $1 | awk -F'requests' '{print $1}'`

# Navigate into the download folder and download the file
cd $DOWNLOAD_FOLDER
echo 'Downloading file based on '$1
curl -X $METHOD -H "$HEADERS" -O -J $URL > /dev/null 2>&1
