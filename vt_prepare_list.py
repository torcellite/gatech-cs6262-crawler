#!/usr/bin/python

##
#Helper script to prepare a list of binaries to be scanned with Virus total
#path is : crawled_websites/<date>/crawl_lists/website_list_<pid>/<url>
##

import os
import sys
import time

if __name__ == "__main__":
    date = sys.argv[1]
    vt_list_file = "crawled_websites/" + date + "/vt_list"
    with open(vt_list_file, "w+b") as vt_list:
        crawl_lists_path = "crawled_websites/" + date + "/crawl_lists"
        for weblist_dir in os.listdir(crawl_lists_path):
            weblist_path = os.path.join(crawl_lists_path, weblist_dir)
            for site_dir in os.listdir(weblist_path):
                site_path = os.path.join(weblist_path, site_dir)
                root, dirs, files = next(os.walk(site_path))
                for f in files:
                    if "tmp_dumpurl_" in f:
                        tmp_file_path = os.path.join(site_path, f)
                        path = tmp_file_path + "\n"
                        vt_list.write(path)
    vt_list.close()
