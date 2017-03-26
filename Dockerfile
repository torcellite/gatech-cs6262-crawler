FROM debian:jessie

MAINTAINER Karthik Balakrishnan <karthik.b@gatech.edu>

# Install essentials
RUN apt-get update && apt-get install -y wget curl python python-pip python-dev build-essential libfontconfig inotify-tools
RUN pip install dnspython ipaddr ipwhois tldextract virustotal
RUN easy_install hashlib

# Copy the crawler
RUN mkdir crawler
WORKDIR crawler
COPY crawler.js get_dns.py download.sh start.sh stop.sh collect_maliciousdata.sh collect_maliciousurl_data.py virustotal_verify.py phantomjs-2.1.1-linux-x86_64.tar.bz2 ./

# Install Phantomjs
# Extract phantomjs
RUN tar xvf phantomjs-2.1.1-linux-x86_64.tar.bz2
# Rename extracted folder
RUN mv phantomjs-2.1.1-linux-x86_64 phantomjs
# Remove tar
RUN rm phantomjs-2.1.1-linux-x86_64.tar.bz2
# Export phantomjs to path
ENV PATH "$PATH:/crawler/phantomjs/bin"
