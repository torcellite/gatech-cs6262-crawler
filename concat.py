import csv
import os
from os import listdir,system
from os.path import isfile, join
import sys

#getting list of dns record files
mypath = os.getcwd()
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
dns_files = []
for file in files:
    if "dns_record_" in file:
        dns_files.append(file)
dns_files = sorted(dns_files)

#open stats.csv
stat_file = open("stats.csv")
stats_reader = csv.reader(stat_file)

#create output file
out_file = open("sample.csv", "w")
stats_out = stats_reader.next()

out_writer = csv.writer(out_file)

#writing stats+dns data into output file
for file in dns_files:
    dns_file = open(file)
    dns_reader = csv.reader(dns_file)
    ignore = dns_reader.next()
    for row in dns_reader:
        out_writer.writerow(stats_out+row)
out_file.close()
