#!/usr/bin/python

import os
import sys
import csv

def get_malicious_data(url, download_folder):
    dns_id = (download_folder.split('/')[-3]).split('_')[-1]
    dnscsv_file = 'dns_record_' + str(dns_id) + '.csv'
    with open(dnscsv_file) as dns_file:
        reader = csv.DictReader(dns_file)
        for row in reader:
            if url in row['url']:
                with open('stats.csv', 'a') as stats_file:
                    writer = csv.writer(stats_file)
                    writer.writerow((row['url'], row['ip_address'], row['asn'], row['asn_country_code'],
                    row['soa_serial'], row['soa_mname'], row['soa_rname'], row['soa_refresh'],
                    row['soa_retry'], row['soa_expire'], row['soa_minimum']))
                break


if __name__ == "__main__":
    url = sys.argv[1]
    download_folder = sys.argv[2]
    os.chdir('./../..')
    vt_file = 'virus_total'
    if os.path.isfile(vt_file):
        get_malicious_data(url, download_folder)
