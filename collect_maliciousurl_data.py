#!/usr/bin/python

import os
import sys
import csv

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


if __name__ == "__main__":
    url_file = sys.argv[1]
    path = url_file.rsplit('/', 1)[0]
    with open(url_file, 'r+') as url_file:
        line = url_file.readline()
        dns_id = line.split(' ')[0]
        url = line.split(' ')[1]
        get_malicious_data(url, dns_id, path)
