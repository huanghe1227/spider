import requests
from lxml import etree

def get_html():
    url = 'http://top.hengyan.com/haokan/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
    res = requests.get(url=url, headers=headers).text
    res_etree = etree.HTML(res)
    result = res_etree.xpath('//div[@class="list"]/ul')
    # print(result,len(result))
    for li in result:
        if li.xpath('.//li[@class="bookname"]/a'):
            list = []
            num = li.xpath('.//li[@class="num"]/text()')[0]
            list.append(num)
            bookname = li.xpath('.//li[@class="bookname"]/a[1]/text()')[0]
            list.append(bookname)
            link = li.xpath('.//li[@class="bookname"]/a[1]/@href')[0]
            list.append(link)
            if li.xpath('.//li[@class="bookname"]/a[2]'):
                section = li.xpath('.//li[@class="bookname"]/a[2]/text()')[0]
                list.append(section)
            else:
                list.append(' ')
            author = li.xpath('.//li[@class="author"]/text()')[0]
            list.append(author)
            length = li.xpath('.//li[@class="length"]/text()')[0]
            list.append(length)
            click = li.xpath('.//li[@class="click"]/text()')[0]
            list.append(click)
            update = li.xpath('.//li[@class="update"]/text()')[0]
            list.append(update)
            print(list)
        else:
            pass

get_html()
