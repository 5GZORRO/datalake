#!/usr/bin/env python3

import sys
import json

import ingest
from s3_api import S3_Proxy, set_s3_proxy


def main():
    # extract paramters from argv[1]
    if len(sys.argv) > 1:
        args = sys.argv[1]
    else:
        args = '{}'
    s3_proxy = S3_Proxy()
    set_s3_proxy(s3_proxy)
    ingest.Ingest(args)
    print(args)



if __name__ == '__main__':
    main()

