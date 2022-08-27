# -*- coding: UTF-8 -*-
import os
import re
import threading
import time
import shutil
import requests
from bs4 import BeautifulSoup

headers = {
  'authority': 'xxx.com',
  'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
  'sec-ch-ua-mobile': '?0',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'sec-fetch-site': 'none',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-user': '?1',
  'sec-fetch-dest': 'document',
  'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
  'Connection': 'close'
}
topheaders = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Host': 'www.xxx.com',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.xxx.com/index.php',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
    'Connection': 'close'
}

# requests.DEFAULT_RETRIES = 5
# requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
s = requests.session()
s.keep_alive = False # 关闭多余连接
# 代理
s.proxies = {"http":"127.0.0.1:10809"}

# 每页视频地址
def topPage():
    topurl = "http://www.xxx.com"
    tophtml = s.get(url=topurl, headers=topheaders)
    toptext = tophtml.text
    tophtml.close()
    # 正则提取内容
    allurl = re.findall(r"href=\"(http://www.xxx.com/view_video.php\?viewkey=\S+)\"", toptext, flags=re.S)
    #print(allurl)
    return allurl

# 视频页视频文件
def getVideoId(url):
    print(url)
    tophtml = s.get(url=url, headers=topheaders, )
    tophtml.encoding = "utf-8"
    toptext = tophtml.text
    tophtml.close()
    # 正则提取内容
    allurl = re.findall(r"div id=VID style=\"display:none;\">(\d+)</div>", toptext, flags=re.S)

    # 获取页面内容
    soup = BeautifulSoup(toptext, 'html.parser')

    # 查找对应标签
    div = soup.find_all('h4', class_="login_register_header")

    # 获取最后一个标签值
    allTitle = div[0].text.strip()

    if len(allurl) > 0:
        return [allurl[0], allTitle]
    return ""

# 下载视频
def downVideo(videoid_name):
    if len(videoid_name) <= 0:
        print("url为空")
        return;

    videoid = videoid_name[0]
    dirpath = "E:\\Movie\\ts\\" + videoid
    url_prifix = "https://xxx.com/m3u8/" + videoid + "/"
    url = "https://xxx.com/m3u8/" + videoid + "/" + videoid + ".m3u8"

    # 获取m3u8文件
    ress = s.get(url=url, headers=headers)
    res = ress.text
    ress.close()
    # 正则提取内容
    ts=re.findall(r"(\d+).ts",res,flags=re.S)
    #print(ts)
    lastTs = videoid_name[1]
    # 从网页上复制下来的请求头
    if os.path.exists("E:\\Movie\\ts\\mp4\\" + lastTs + ".mp4"):
        print(lastTs + ".mp4已存在")
        return

    def downTs(i, url, headers):
        try:
            rr = requests.get(url=url, headers=headers)
        except Exception as e:
            time.sleep(3)
            downTs(i, url, headers)
            return;
        r = rr.content
        print(i, url)
        # 二进制写入到本地
        if os.path.exists(dirpath) == False:
            os.mkdir(dirpath)
        with open(dirpath + '\\'+i+'.ts',mode="wb") as file:
            file.write(r)
        rr.close()


    for i in ts:
        # 拼接完整的ts文件下载链接
        u = url_prifix + i + ".ts"
        try:
            t = threading.Thread(target=downTs, args=(i, u, headers, ))
            #线程准备就绪，随时等候cpu调度
            t.start()
        except Exception as msg:
            print(msg)
        time.sleep(0.3)

    while True:
        allDown = True
        for i in ts:
            if os.path.exists(dirpath + "\\" + i + ".ts") == False:
                print(dirpath + "\\" + i + ".ts不存在")
                allDown = False
                break
        time.sleep(5)
        if allDown:
            time.sleep(5)
            # 将.ts文件合成为mp4格式
            mp4 = open("E:\\Movie\\ts\\mp4\\" + lastTs + ".mp4", 'wb')
            for i in ts:
                ts = open(dirpath + "\\" + i + ".ts", "rb")
                mp4.write(ts.read())
                ts.close()
            print(lastTs + ".mp4，转换成功")
            mp4.close()
            time.sleep(5)
            # 删除原ts文件
            # for i in ts:
            #     os.remove(dirpath + "\\" + i + ".ts")
            # os.remove(dirpath)
            shutil.rmtree(dirpath)
            break

# 获取当前页视频地址
allUrl = topPage()
# 遍历所有地址
for i in allUrl:
    # 获取视频页视频地址
    videl_id = getVideoId(i)
    # 进行下载
    #downVideo(videlurl)
    # 多线程下载
    t = threading.Thread(target=downVideo, args=(videl_id, ))
    t.start()
    time.sleep(2)
