# coding:utf-8
# 引入requests包和正则表达式包re
import requests
import re


# 自定义下载页面函数
def load_page(url):
    response = requests.get(url)  # 获取响应
    data = response.content    # 响应数据
    return data


# 自定义保存页面图片函数
def get_image(html):
    regx = r'http://[\S]*jpg'  # 定义图片正则表达式
    pattern = re.compile(regx)  # 编译表达式构造匹配模式
    get_images = re.findall(pattern, repr(html))  # 在页面中匹配图片链接

    num = 1
    # 遍历匹配成功的链接
    for img in get_images:
        image = load_page(img)  # 根据图片链接，下载图片链接
        # 将下载的图片保存到对应的文件夹中
        with open('./spider_picture/%s.jpg' % num, 'wb') as fb:
            fb.write(image)
            print("正在下载第%s张图片" % num)
            num = num + 1
    print("下载完成！")


# 定义爬取页面的链接
url = 'http://p.weather.com.cn/2017/06/2720826.shtml#p=7'
# 调用load_page函数，下载页面内容
html = load_page(url)
# 在页面中，匹配图片链接，并将图片下载下来，保存到对应文件夹
get_image(html)