import re

import requests


def hello():
    ip = "61.6.191.214:53281"
    r = re.compile(r'\d+\.\d+\.\d+\.\d+:\d+')
    result = r.match(ip)
    print(result.group(0))

if __name__ == "__main__":
    hello()