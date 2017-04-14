#!/usr/bin/python

import os
import sys
import time
import requests
import hashlib
import virustotal

MAX_UPLOAD_SIZE = 32000000
API_KEY = 'be2c60b986bf1cc0fbc80fe5fd2382f2a5e25384ebac14fcbd4701346749f4ca'

file_ext = ['.woff', '.otf', '.ttf', '.jpg', '.png', '.pdf', '.js', '.json', '.PDF']

def verify_file(path, filename):
    file_toverify = path + '/' + filename
    filesize = os.path.getsize(file_toverify)
    v = virustotal.VirusTotal(API_KEY)
    if not os.path.isdir(file_toverify) and filesize > 10000 and '?' not in file_toverify:
        print "Scanning file ", file_toverify
        #time.sleep(20)
        start_time = time.time()
        current_time = start_time
        #using sleep() does not always work; if a signal is caught it terminates sleep()
        while(current_time < (float(start_time)+16)):
            current_time = time.time()
        try:
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
        except:
            pass
    else:
        return None


def get_malicious_data(url, dns_id, path):
    try:
        dnscsv_file = path + '/dns_record_' + str(dns_id) + '.csv'
        with open(dnscsv_file) as dns_file:
            reader = csv.DictReader(dns_file)
            for row in reader:
                if url in row['url']:
                    stats_file = path + '/stats.csv'
                    with open(stats_file, 'a') as stats_file:
                        writer = csv.writer(stats_file)
                        writer.writerow([])
                        writer.writerow((row['url'], row['ip_address'], row['asn'], row['asn_country_code'],
                        row['soa_serial'], row['soa_mname'], row['soa_rname'], row['soa_refresh'],
                        row['soa_retry'], row['soa_expire'], row['soa_minimum']))
                    break
    except:
        pass


def get_vt_details(tmp_filelist):
    #filename = sys.argv[1]
    with open(filename, 'r+') as tmp_file:
        for line in tmp_file:
            #line = tmp_file.readline()
            l = line.split(' ')
            dns_id = l[0]
            url = l[1]
            path = l[2]
            download_filepath = l[3]
            download_file = l[4].strip('\n')

            vt_verify_flag = 1
            #Do not scan the file if it is a font file
            for ext in file_ext:
                if ext in download_file:
                    vt_verify_flag = 0

            if vt_verify_flag==1:
                vt_report = verify_file(download_filepath, download_file)
                if vt_report and not vt_report['positives']==0:
                    get_malicious_data(url, dns_id, path)
                    #final virus total result
                    record = str(vt_report['positives']) + '/' + str(vt_report['total']) +'\n'
                    #file containing VT result if found malicious
                    vt_filepath = path + '/virus_total_' + dns_id + "_" + download_file.rsplit('.', 1)[0]
                    with open(vt_filepath, 'w+b') as vt_file:
                        vt_file.write(record)
                    vt_file.close()


if __name__ == "__main__":
    filename = sys.argv[1]
    get_vt_details(filename)
