#!/usr/bin/python

##
#Script to collect all dns information based on the resources requested by the site
##

import os
import sys
import re
import json
import csv
import time
import dns.resolver
from ipwhois import IPWhois
from ipwhois.net import Net
from ipwhois.asn import IPASN
from urlparse import urlparse
import tldextract

contentTypeWhitelist = ['application/json',
                        'application/javascript',
                        'application/x-javascript',
                        'application/font-woff',
                        'image', 'font', 'css']

urls_visited = []

#Resolve DNS request
def resolveDns(url):
    dns_record = {}
    if url.startswith('http'):
        dns_record['url'] = url
        domain_name = urlparse(url).hostname
        if domain_name:
            resolver = dns.resolver.Resolver()
            try:
                #fetch dns A-record
                dns_ans = resolver.query(domain_name, 'A')
                #Store DNS record only for the first IP address to avoid redundant data
                r = dns_ans[0]
                if str(r) in urls_visited:
                    return None
                else:
                    net = Net(r)
                    obj = IPASN(net)
                    results = obj.lookup()
                    urls_visited.append(url)
                    dns_record['ip_address'] = str(r)
                    dns_record['asn'] = results['asn']
                    dns_record['asn_country_code'] = results['asn_country_code']
            except:
                #if A-record is not found mark it as unknown '?'
                dns_record['ip_address'] = '?'
                dns_record['asn'] = '?'
                dns_record['asn_country_code'] = '?'
            #Collect the SOA records
            try:
                soa_record = resolver.query(domain_name, "SOA")
                for s in soa_record:
                    dns_record['soa_serial'] = s.serial
                    dns_record['soa_mname'] = s.mname
                    dns_record['soa_rname'] = s.rname
                    dns_record['soa_refresh'] = s.refresh
                    dns_record['soa_retry'] = s.retry
                    dns_record['soa_expire'] = s.expire
                    dns_record['soa_minimum'] = s.minimum
            except:
                #extract the domain name and try fetching the SOA record
                ext = tldextract.extract(url)
                domain = ext.domain + '.' + ext.suffix
                try:
                    soa_record = resolver.query(domain, "SOA")
                    for s in soa_record:
                        dns_record['soa_serial'] = s.serial
                        dns_record['soa_mname'] = s.mname
                        dns_record['soa_rname'] = s.rname
                        dns_record['soa_refresh'] = s.refresh
                        dns_record['soa_retry'] = s.retry
                        dns_record['soa_expire'] = s.expire
                        dns_record['soa_minimum'] = s.minimum
                except:
                    dns_record['soa_serial'] = '?'
                    dns_record['soa_mname'] = '?'
                    dns_record['soa_rname'] = '?'
                    dns_record['soa_refresh'] = '?'
                    dns_record['soa_retry'] = '?'
                    dns_record['soa_expire'] = '?'
                    dns_record['soa_minimum'] = '?'
            return dns_record
    else:
        return None

#fetch resorces requested by the crawler and sump the ns records  into a file
def get_resource(path):
    dnsrecord_id = path.split('/')[-2]
    res_file = path + 'resources.json'
    dnscsv_file = path +'/../' + 'dns_record_' + dnsrecord_id.split('_')[-1] + '.csv'
    with open(res_file) as resource_file, open(dnscsv_file, 'wb') as csvfile:
        fieldnames = ['url', 'ip_address', 'asn', 'asn_country_code',
        'soa_serial', 'soa_mname', 'soa_rname', 'soa_refresh',
        'soa_retry', 'soa_expire', 'soa_minimum']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        resource = json.load(resource_file)
        for url in resource:
            if 'response' in resource[url]:
                whitelisted = 0
                for contentType in contentTypeWhitelist:
                    if contentType in str(resource[url]['response']['contentType']):
                        whitelisted = 1
                        break
                if whitelisted == 0:
                    dns_record = resolveDns(url)
                    if dns_record is not None:
                        writer.writerow(dns_record)


if __name__ == "__main__":
    start_time = time.time()
    path = sys.argv[1]
    get_resource(path)
    #print "Time taken ", (time.time() - start_time)
