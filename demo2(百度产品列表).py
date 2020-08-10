# ------------------------------------------------1.导包
import requests

# -------------------------------------------------2.确定url
base_url = 'https://www.baidu.com/more/'

# ----------------------------------------------3.发送请求，获取响应
response = requests.get(base_url)

# -----------------------------------------------4.查看页面内容,可能出现 乱码
# print(response.text)
# print(response.encoding)
# ---------------------------------------------------5.解决乱码
# ---------------------------方法一：转换成utf-8格式
# response.encoding='utf-8'
# print(response.text)
# -------------------------------方法二：解码为utf-8
with open('index.html', 'w', encoding='utf-8') as fp:
    fp.write(response.content.decode('utf-8'))
print(response.status_code)
print(response.headers)
print(type(response.text))
print(type(response.content))