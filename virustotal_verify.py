#!/usr/bin/python

import os
import sys
import requests
import hashlib
import virustotal

MAX_UPLOAD_SIZE = 32000000
API_KEY = 'be2c60b986bf1cc0fbc80fe5fd2382f2a5e25384ebac14fcbd4701346749f4ca'

def verify_file(filepath):
    filesize = os.path.getsize(filepath)
    v = virustotal.VirusTotal(API_KEY)

    print "Scanning file ", filepath
    if filesize < MAX_UPLOAD_SIZE:
        report = v.scan(filepath)
    else:
        #if filesize is greater than the max upload size use the MD5 hash
        filehash = hashlib.md5(open(filepath,"rb").read()).hexdigest()
        report = v.get(filehash)
    #wait for the report to be ready
    report.join()
    assert report.done == True
    print "Resource's status:", report.status
    print "Antivirus' total:", report.total
    print "Antivirus's positives:", report.positives
    if report.positives > 0:
        return True
    else:
        return False


if __name__ == "__main__":
    filepath = sys.argv[1]
    print verify_file(filepath)
