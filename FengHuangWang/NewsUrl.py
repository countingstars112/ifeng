# coding: utf-8
import re
import time
import requests


def Run():
    html = ''
    finance_URL = 'http://finance.ifeng.com/'
    ent_URL = 'http://ent.ifeng.com/'
    sports_URL = 'http://sports.ifeng.com/'
    URL = [ent_URL, sports_URL, finance_URL]
    # otherStyle = now.strptime("%Y-%m-%d")
    # re_ = '(http://[fes]{1}.{2,6}.ifeng.com/a/2017\d*?/.*?.shtml)'
    now = time.strftime("%Y%m%d")
    re_ = '(http://[fes]{1}.{2,6}.ifeng.com/a/'+now+'/.*?.shtml)'
    url_list = []
    for url in URL:
        while 1:
            try:
                html = requests.get(url, timeout=30).content
                break
            except Exception as e:
                print e

        url_list += re.findall(re_, html)
    url_list_true = set(url_list)
    for news_url in url_list_true:
        yield news_url


class NewsUrl(object):
    def __init__(self):
        pass


if __name__ == '__main__':
    Run()
