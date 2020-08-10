import requests
from lxml import etree
import threading
import time


def get_html(data, n):
    print('正在爬取第{}页信息'.format(n))
    url = 'https://www.shanbay.com/wordlist/110521/232414/?page={}'.format(n)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
    res = requests.get(url=url, headers=headers).text
    res_etree = etree.HTML(res)
    result = res_etree.xpath('//tbody/tr[@class="row"]')
    for td in result:
        list = []
        word = td.xpath('td[@class="span2"]/strong/text()')[0]
        list.append(word)
        meaning = td.xpath('td[@class="span10"]/text()')[0].strip()
        list.append(meaning)

        data.append(list)


def get_all_pages():
    data = []
    for n in range(1, 4):
        t = threading.Thread(target=get_html, args=(data, n))
        t.start()
        time.sleep(2)
    return data


data = get_all_pages()
print(data)
