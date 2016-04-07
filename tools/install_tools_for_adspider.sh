#!/bin/sh
# Install tools which Adspider depends on.
pip install tld
pip install lxml
yum install MySQL-python
pip install python-gflags
pip install scrapy
pip install frontera[distributed,zeromq,sql]
