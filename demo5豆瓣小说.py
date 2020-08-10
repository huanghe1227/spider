import requests
from lxml import etree
import threading
import time
import xlwt


def get_html(data, n):
    print('正在爬取第{}页信息'.format(n + 1))
    url = "https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start={}&type=T".format(n * 20)  # 网址
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    }  # 请求头，以浏览器的身份访问该网站
    res = requests.get(url=url, headers=headers).text  # 获取网页源码
    res_etree = etree.HTML(res)  # 解析
    # 下面就需要分析网页源码，找到获取信息的方式
    result = res_etree.xpath('//li[@class="subject-item"]')  # 使用xpath规则获取所有的li标签，这只是一个网页下的
    for li in result:
        list = []  # 这里定义一个列表把每一部小说的所有信息都放入其中
        if li.xpath('.//span[@style="font-size:12px"]'):  # 这里是用来判断小说的名字是否有副标题
            title = li.xpath('.//div[@class="info"]/h2/a/@title')[0] + li.xpath('.//span[@style="font-size:12px"]')[0]
            list.append(title)
        else:
            title = li.xpath('.//div[@class="info"]/h2/a/@title')[0]
            list.append(title)
        link = li.xpath('.//div[@class="info"]/h2/a/@href')[0]  # 小说链接
        list.append(link)
        img_link = li.xpath('.//a[@class="nbg"]/img/@src')[0]  # 图片链接
        list.append(img_link)
        main_info = li.xpath('.//div[@class="pub"]/text()')[0].strip()  # 主要信息
        list.append(main_info)
        score = li.xpath('.//div[@class="info"]/div/span[2]/text()')[0].strip()  # 评分
        list.append(score)
        score_num = li.xpath('.//div[@class="info"]/div/span[3]/text()')[0].strip()  # 评分人数
        list.append(score_num)
        if li.xpath('div[@class="info"]/p/text()'):  # 这里判断小说的简介是否存在，如果存在就写入列表，不存在就要加一个空格
            introduction = li.xpath('div[@class="info"]/p/text()')[0].strip()
            list.append(introduction)
        else:
            list.append(' ')  # 这里加空格的目的是，防止在存入excel时出现位置错乱的情况

        data.append(list)
        # return list
        # print(list, len(list)) #成功，每一部小说的主要信息都存入到一个列表中，其中有一些空格会出现在一些信息的前面或者后面，这里使用strip()取出两端空格


# 下面写一个多页爬取的函数

def get_all_pages():
    data = []  # 这里定义一个新列表，接下来要做的是把上面的每一个小列表都存入到这个大列表中
    for n in range(0, 20):  # 这里是需要使用n来改变网页网址，从而达到爬取每一页信息的目的，所以需要将这个函数与上面函数建立联系，这里可将data和n这两变量放入到第一个函数的正确位置
        t = threading.Thread(target=get_html, args=(data, n))  # 爬取多页是为了提高速度，采用一个简单的多线程爬取，导入了一个threading库
        t.start()
        time.sleep(0.5)
    return data


# data = get_all_pages()
# print(data)

# 下面是如何自动写入Excel
def download_excel():
    data = get_all_pages()
    workbook = xlwt.Workbook("utf-8")  # 创建工作簿，utf-8为解码方式，让exc可以正常写入中文
    sheet = workbook.add_sheet("豆瓣小说爬虫")  # 创建一个sheet
    col = ['书名', '书籍链接', '图片链接', '主要信息', '评价', '评价人数', '简介']  # 这个作为首行信息，将其写入Excel第一行
    for i in range(0, 7):
        sheet.write(0, i, col[i])
    for i in range(0, len(data)):  # 这里使用data的长度来确定i的范围，这里的i和上面的i不是同一个
        new_data = data[i]  # 将data中的每一小条单独去取出，逐条写入到Excel的每一行
        for j in range(0, 7):
            sheet.write(i + 1, j, new_data[j])  # 第一行已经写入信息了，需要从第二行开始
    workbook.save('D:\pythonProject\豆瓣小说爬虫.xls')  # 保存位置
    print("保存完毕")


def main():
    download_excel()


if __name__ == "__main__":
    main()
