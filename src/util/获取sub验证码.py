import requests
from flask import Flask
from flask_cors import *
from gevent import pywsgi
from bs4 import BeautifulSoup

# 创建一个服务
app = Flask(__name__)
CORS(app, supports_credentials=True)

# 创建一个接口 指定路由和请求方法 定义处理请求的函数
@app.route(rule='/vigor/get/subcode', methods=['GET'])
def getCode():
    page = requests.get('https://mp.weixin.qq.com/s/vfWg1v3wVLKoLBRE5mFQ7w')
    page.encoding = "utf-8"

    # 获取页面内容
    soup = BeautifulSoup(page.text, 'html.parser')

    # 查找对应标签
    div = soup.find_all('div', class_="rich_media_content")

    # 获取最后一个标签值
    text = div[0].find_all("strong")
    return text[len(text) - 1].text.strip()

# getCode()

if __name__ == '__main__':
    # 启动服务 指定主机和端口
    server = pywsgi.WSGIServer(('127.0.0.1', 8899), app)
    print('server is running...')
    server.serve_forever()