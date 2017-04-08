import csv
import os
import sys
from os import listdir
from os.path import isfile, join

#getting list of crawled websites
dir_path = "crawled_websites/"+sys.argv[1]+"/"
base_dirs = next(os.walk(dir_path))[1]
dirs = []
for base_dir in base_dirs:
    web_dirs = next(os.walk(dir_path+base_dir))[1]
    for dir in web_dirs:
        dirs.append(dir_path+base_dir+"/"+dir)

for dir in dirs:
    files = [f for f in listdir(dir) if isfile(join(dir, f))]
    if "sample.csv" not in files:
        dns_files = []
        for file in files:
            if "dns_record_" in file:
                dns_files.append(file)
        dns_files = sorted(dns_files)

#open stats.csv
        if "stats.csv" in files and dns_files:
            stat_file = open(dir+"/stats.csv")
            stats_reader = csv.reader(stat_file)
            stats_out = stats_reader.next()
            stat_file.close()
#create output file
            out_file = open(dir+"/sample.csv", "w")
            out_writer = csv.writer(out_file)

#writing stats+dns data into output file
            for file in dns_files:
                dns_file = open(dir+"/"+file)
                dns_reader = csv.reader(dns_file)
                ignore = dns_reader.next()
                for row in dns_reader:
                    out_writer.writerow(stats_out+row)
            out_file.close()
