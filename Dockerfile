FROM debian:jessie

MAINTAINER Karthik Balakrishnan <karthik.b@gatech.edu>

# Create working directory
RUN mkdir crawler
WORKDIR crawler

# Install essentials
RUN apt-get update && apt-get install -y wget curl python python-pip python-dev build-essential libfontconfig inotify-tools
RUN pip install dnspython ipaddr ipwhois tldextract virustotal
RUN easy_install hashlib

# Install Phantomjs
# Download phantomjs
RUN wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
# Extract phantomjs
RUN tar xvf phantomjs-2.1.1-linux-x86_64.tar.bz2
# Rename extracted folder
RUN mv phantomjs-2.1.1-linux-x86_64 phantomjs
# Remove tar
RUN rm phantomjs-2.1.1-linux-x86_64.tar.bz2
# Export phantomjs to path
ENV PATH "$PATH:/crawler/phantomjs/bin"

# Hashlib frozenset not callable fix
RUN mv /usr/lib/python2.7/lib-dynload/_hashlib.x86_64-linux-gnu.so /usr/lib/python2.7/lib-dynload/_hashlib.x86_64-linux-gnu.so1

# Copy the crawler
COPY . ./
