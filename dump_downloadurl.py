#!/usr/bin/python

import os
import sys

if __name__=="__main__":
    filename = sys.argv[1]
    url = sys.argv[2]
    download_folder = sys.argv[3]
    dns_id = (download_folder.split('/')[-3]).split('_')[-1]
    tmp_dumpurl = "./../../" + 'tmp_dumpurl_' + dns_id
    print tmp_dumpurl
    with open(tmp_dumpurl, 'a+') as tmp:
        tmp_record = dns_id + ' ' + url + ' ' + filename
        tmp.write(tmp_record)
        tmp.write('\n')
