# coding:utf8

import argparse
import os
import subprocess
import sys


def ensure_dependencies():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dependency_script = os.path.join(base_dir, "ensure_dependencies.py")

    try:
        subprocess.check_call([sys.executable, dependency_script, base_dir])
    except subprocess.CalledProcessError as e:
        print >>sys.stderr, e
        print >>sys.stderr, "Failed to ensure dependencies being up-to-date!"


def main():
    ensure_dependencies()


if __name__ == '__main__':
    main()
