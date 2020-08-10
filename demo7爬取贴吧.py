import requests
import parsel

page_num = 0

for page in range(0, 251, 50):  # 指定页数
    page_num += 1
    print("================正在爬取第{}页数据================ ".format(page_num))

    url = 'https://tieba.baidu.com/f?kw=%E7%BA%A6%E4%BC%9A&ie=utf-8&pn={}'.format(str(page))
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'}
    res = requests.get(url=url, headers=headers).text
    # 解析数据（数据筛选）<两层数据解析>
    html = parsel.Selector(res)
    title_url = html.xpath('//div[@class="threadlist_lz clearfix"]/div/a/@href').getall()

    second_url = 'https://tieba.baidu.com'
    for url in title_url:
        all_url = second_url + url
        print('当前的帖子链接为', all_url)

        # 再次发送请求，请求帖子内部数据
        res_2 = requests.get(url=all_url, headers=headers).text
        # 第二次解析
        res_2_data = parsel.Selector(res_2)
        result_list = res_2_data.xpath('//cc/div/img[@class="BDE_Image"]/@src').getall()
        print(result_list)

        for li in result_list:
            img_data = requests.get(url=li, headers=headers).content
            # 保存数据
            file_name = li.split('/')[-1]
            with open('img\\' + file_name, mode='wb') as fb:
                fb.write(img_data)
                print('正在保存：', file_name)


