# coding:utf8

import argparse
import os
import subprocess
import sys

from tld.utils import update_tld_names
from pudb import set_trace
set_trace()


def ensure_dependencies():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dependency_script = os.path.join(base_dir, "ensure_dependencies.py")

    try:
        subprocess.check_call([sys.executable, dependency_script, base_dir])
    except subprocess.CalledProcessError as e:
        print >>sys.stderr, e
        print >>sys.stderr, "Failed to ensure dependencies being up-to-date!"


def start_spider():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    start_spider_script = os.path.join(base_dir,
                                       "scrapy_spider",
                                       "start_spider.py")
    os.chdir(os.path.join(base_dir, "scrapy_spider"))

    try:
        subprocess.check_call([sys.executable, start_spider_script])
    except subprocess.CalledProcessError as e:
        print >>sys.stderr, e
        print >>sys.stderr, "Failed to start spider!"

    os.chdir(base_dir)


def main():
    ensure_dependencies()
    update_tld_names()
    start_spider()


if __name__ == '__main__':
    main()
