#!/usr/bin/python

##
#Script to save the downloaded file name, path and url into a file tmp_dumpurl_*;
#will be used to scan files with VT
##

import os
import sys

if __name__=="__main__":
    filename = sys.argv[1]
    url = sys.argv[2]
    download_folder = sys.argv[3]
    dns_id = (download_folder.split('/')[-3]).split('_')[-1]
    download_folder = os.path.abspath('./')
    os.chdir("./../../")
    tmp_dumpurl = 'tmp_dumpurl_' + dns_id
    path = os.path.abspath('./')
    with open(tmp_dumpurl, 'a+') as tmp:
        tmp_record = dns_id + ' ' + url + ' ' + path + ' ' + download_folder + ' ' + filename
        tmp.write(tmp_record)
        tmp.write('\n')
