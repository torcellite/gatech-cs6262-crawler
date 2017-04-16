## Crawler

The module crawls the given list of domains. It tries to elicit drive-by downloads by performing grid-based clicks.

  1. The screenshot of the main page and every pop-up is captured.
  2. The resources requested (including drive-by downloads) by the page are downloaded for inspection using a background cURL process.
  3. The infrastructure data for the website and the websites hosting the requested resources are also collected.

### Requirements
  1. [PhantomJS](http://phantomjs.org/download.html)
  2. Python 2.7

Install all the python libraries using `pip install requirements.txt`

### Usage
To crawl one domain like google.com:

`bash start.sh google.com crawled_websites/google.com`

To crawl a list of domains stored in a file called "website_list"

`bash run_crawler.sh website_list`

To spawn multiple crawler instances to crawl multiple files like "website_list"

`bash run_multiple_crawler.sh 8`

The file name convention for the lists is "website_list_[num]" where [num] varies from 1 to the number of instances.

To start verifying all the downloaded files with VT for a given date and merge all the data into a single file.

`bash start_virustotal.sh 04-04-17`
