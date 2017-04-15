#!/usr/bin/python

import csv
import os
import sys

rank_dict = {}

feature_file_name = "../classifier_features/" + sys.argv[1] + "_features.csv"

def traverse_rankfile(date):
    rank_file_name = date + "-top-1m-urls.csv"
    rank_file_path = os.path.join('../alexa-processor/csv/', rank_file_name)
    print rank_file_path
    with open(rank_file_path, "r") as rank_file:
        rank_file_reader = csv.reader(rank_file)
        for line in rank_file_reader:
            rank_dict[line[1]] = line[0]
    rank_file.close()


def get_rank(filepath):
    url = filepath.split('/')[-1]
    if url in rank_dict.keys():
        return rank_dict[url]
    else:
        return None


def get_stats_data(filepath):
    stats_file_path = os.path.join(filepath, "stats.csv")
    if os.path.isfile(stats_file_path):
        with open(stats_file_path, "r") as stats_file:
            stats_file_reader = csv.reader(stats_file)
            stats_out = next(stats_file_reader)
            if "NaN" in stats_out:
                stats_out = [s.replace("NaN", "?") for s in stats_out]
        stats_file.close()
        return stats_out
    else:
        return None


def get_dnsfiles(filepath):
    dns_files_list = []
    root, dirs, files = next(os.walk(filepath))
    for f in files:
        if "dns_record_" in f:
            dns_file_path = os.path.join(site_path, f)
            dns_files_list.append(dns_file_path)
    return dns_files_list


def get_vt_record(filepath):
    vt_record_list = []
    root, dirs, files = next(os.walk(filepath))
    for f in files:
        if "virus_total_" in f:
            vt_file = os.path.join(site_path, f)
            id = '_' + vt_file.split("_")[2] + "."
            vt_record_list.append(id)
    return vt_record_list


def merge_data(filepath):
    sample_file_path = os.path.join(filepath, "sample.csv")
    with open(feature_file_name, "a+") as feature_file, open(sample_file_path, "w") as sample_file:
        feature_writer = csv.writer(feature_file, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
        sample_file_writer = csv.writer(sample_file, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
        stats_out = get_stats_data(site_path)
        rank = [get_rank(site_path)]
        #rank = ['?']

        dns_files_list = get_dnsfiles(filepath)
        vt_records = get_vt_record(filepath)
        if len(vt_records) > 0:
            vt_record_exists = True
        else:
            vt_record_exists = False

        for dnsfile in dns_files_list:
            vt_flag = False
            #check VT records and collect the malicious URLs
            malicious_url_list = []
            count = 0
            for id in vt_records:
                if id in dnsfile:
                    vt_flag = True
                    tmp_filename = dir + "/tmp_dumpurl" + id.rstrip('.')
                    with open(tmp_filename, 'r+') as tmp_file:
                        for line in tmp_file:
                            l = line.split(' ')
                            malicious_url_list.append(l[1])
                    tmp_file.close()
                    break

            with open(dnsfile, "r") as dns_file:
                dns_reader = csv.reader(dns_file)
                next(dns_reader)
                for row in dns_reader:
                    vt_stats = []
                    if vt_flag and vt_record_exists:
                        vt_stats.append(1)
                        if row[0] in malicious_url_list:
                            vt_stats.append(1)
                        else:
                            vt_stats.append(0)
                    elif vt_record_exists:
                        vt_stats.append(1)
                        vt_stats.append(0)
                    else:
                        vt_stats.append(0)
                        vt_stats.append(0)
                    #write data into output file
                    try:
                        row[0] = '\"' + row[0] + '\"'
                        row[1] = '\"' + row[1] + '\"'
                        row[3] = '\"' + row[3] + '\"'
                    except:
                        pass
                    try:
                        if row[5] is not '?':
                            row[5] = '\"' + row[5] + '\"'
                        if row[6] is not '?':
                            row[6] = '\"' + row[6] + '\"'
                    except:
                        pass
                    sample_file_writer.writerow(stats_out+row+rank+vt_stats)
                    feature_writer.writerow(stats_out+row+rank+vt_stats)
            dns_file.close()
    sample_file.close()
    feature_file.close()


if __name__ == "__main__":
    date = sys.argv[1]
    traverse_rankfile(date)
    crawl_lists_path = "crawled_websites/"+ sys.argv[1] + "/crawl_lists/"
    for weblist_dir in os.listdir(crawl_lists_path):
        weblist_path = os.path.join(crawl_lists_path, weblist_dir)
        for site_dir in os.listdir(weblist_path):
            site_path = os.path.join(weblist_path, site_dir)
            merge_data(site_path)
