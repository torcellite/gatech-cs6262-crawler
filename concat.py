import csv
import os
import sys
from os import listdir
from os.path import isfile, join

#getting list of crawled websites
dir_path = "crawled_websites/"+sys.argv[1]+"/crawl_lists/"
base_dirs = next(os.walk(dir_path))[1]
rank_dir = '../alexa-processor/csv/'
target_rank_file = sys.argv[1] + "-top-1m-urls.csv"
dirs = []
for base_dir in base_dirs:
    web_dirs = next(os.walk(dir_path+base_dir))[1]
    for dir in web_dirs:
        dirs.append(dir_path+base_dir+"/"+dir)

for dir in dirs:
    files = [f for f in listdir(dir) if isfile(join(dir, f))]
    if "sample.csv" not in files:
        url = dir.split("/")[-1]

#get rank of the url
        ranking_files = [f for f in listdir(rank_dir) if isfile(join(rank_dir, f))]
        rank = "?"
        if target_rank_file in ranking_files:
	    rank_file = open(rank_dir + target_rank_file)
            rank_reader = csv.reader(rank_file)
            for line in rank_reader:
                if url in line:
                     rank = line[0]
                     break

#get list of dns_files and virustotal_files
        dns_files = []
        virustotal_files = []
        vt_dnsid_list = []
        for file in files:
            if "dns_record_" in file:
                dns_files.append(file)
            if "virus_total_" in file:
                virustotal_files.append(file)
                id = '_' + file.split("_")[2] + "."
                vt_dnsid_list.append(id)
        dns_files = sorted(dns_files)

#open stats.csv
        if "stats.csv" in files and dns_files:
            stat_file = open(dir+"/stats.csv")
            stats_reader = csv.reader(stat_file)
            stats_out = stats_reader.next()
            stat_file.close()
            stats_out.append(rank)

#create output file
            out_file = open(dir+"/sample.csv", "w")
            out_writer = csv.writer(out_file)

#writing stats+dns data into output file
            for file in dns_files:
                vt_flag = False
                #check if there is a downloaded file that was found malicious by VT
                malicious_url_list = []
                vt_score_list = []
                count = 0
                for id in vt_dnsid_list:
                    if id in file:
                        vt_flag = True
                        tmp_filename = dir + "/tmp_dumpurl" + id.rstrip('.')
                        with open(tmp_filename, 'r+') as tmp_file:
                            for line in tmp_file:
                                l = line.split(' ')
                                malicious_url_list.append(l[1])
                                vt_filename = dir +  '/virus_total' + id.rstrip('.') + "_" + (l[4].strip('\n')).rsplit('.', 1)[0]
                                with open(vt_filename, 'r+') as vt_file:
                                    vt_score = vt_file.readline()
                                    vt_score = vt_score.strip('\n')
                                    vt_score_list.append(vt_score)
                                vt_file.close()
                        tmp_file.close()
                        break
                dns_file = open(dir+"/"+file)
                dns_reader = csv.reader(dns_file)
                ignore = dns_reader.next()
                for row in dns_reader:
                    vt_stats = []
                    if vt_flag:
                        vt_stats.append('1')
                        if row[0] in malicious_url_list:
                            idx = malicious_url_list.index(row[0])
                            vt_stats.append('1')
                            vt_stats.append(vt_score_list[idx])
                        else:
                            vt_stats.append('0')
                            vt_stats.append('?')
                    else:
                        vt_stats.append('0')
                        vt_stats.append('0')
                        vt_stats.append('?')
                    out_writer.writerow(stats_out+row+vt_stats)
                dns_file.close()
            out_file.close()
