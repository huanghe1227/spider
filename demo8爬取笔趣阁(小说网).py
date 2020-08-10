import requests
import re

url = "http://www.biquge.info/10_10582/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
response = requests.get(url=url, headers=headers)
response.encoding = 'utf-8'
html_data = response.text

result_list = re.findall('<dd><a href="(.*?)" title="(.*?)">.*</a></dd>',
                         html_data)  # ()表示精确匹配 . 代表匹配除了换行符以外的任意字符 * 匹配前一个字符的0次或者多次 ? 非贪婪模式

for chapter_url, title in result_list:
    try:
        # print(chapter_url,title)
        all_url = "http://www.biquge.info/10_10582/" + chapter_url
        # print(all_url)
        response_2 = requests.get(url=all_url, headers=headers)
        response_2.encoding = 'utf-8'  # 自动识别响应体的编码
        html_data_2 = response_2.text
        # print(html_data_2)

        # 解析章节内部小说文本 解析数据的时候，一切数据以终端为准
        result = re.findall('<div id="content">(.*?)</div>', html_data_2, re.S)
        if result:
            # print(result)
            #     text = result[0].replace('&nbsp;','').replace('<br/>','\n')

            # 4.保存数据
            with open('三寸人间\\' + title + '.txt', mode='w', encoding='utf-8') as f:
                f.write(result[0].replace('&nbsp;', '').replace('<br/>', '\n'))
                print('保存成功：', title)
    except Exception as e:  # 异常捕获
        print(e)
