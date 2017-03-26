#!/usr/bin/python

import os
import sys
import requests
import hashlib
import virustotal

MAX_UPLOAD_SIZE = 32000000
API_KEY = 'be2c60b986bf1cc0fbc80fe5fd2382f2a5e25384ebac14fcbd4701346749f4ca'


def verify_file(file_toverify):
    filesize = os.path.getsize(file_toverify)
    v = virustotal.VirusTotal(API_KEY)
    print "Scanning file ", file_toverify
    if filesize < MAX_UPLOAD_SIZE:
        report = v.scan(file_toverify)
    else:
        #if filesize is greater than the max upload size use the MD5 hash
        filehash = hashlib.md5(open(file_toverify,"rb").read()).hexdigest()
        report = v.get(filehash)
    #wait for the report to be ready
    report.join()
    assert report.done == True
    vt_report = {}
    vt_report['total'] = report.total
    vt_report['positives'] = report.positives
    return vt_report


if __name__ == "__main__":
    filename = sys.argv[1]
    url = sys.argv[2]
    download_folder = sys.argv[3]
    dns_id = (download_folder.split('/')[-3]).split('_')[-1]
    vt_report = verify_file(filename)
    if not vt_report['positives']==0:
        #final virus total result
        record = str(vt_report['positives']) + '/' + str(vt_report['total']) +'\n'
        #file containing VT result if found malicious
        vt_filepath = "./../../" + 'virus_total' + filename.rsplit('.', 1)[0]
        #file to dump url to later fetch the dns record
        tmp_dumpurl = "./../../" + 'tmp_dumpurl_' + dns_id
        with open(vt_filepath, 'w+b') as vt_file, open(tmp_dumpurl, 'w+b') as tmp:
            vt_file.write(record)
            tmp_record = dns_id + ' ' + url
            tmp.write(tmp_record)
        vt_file.close()
        tmp.close()
