# -*- coding: utf-8 -*-

# @Time    : 2019/8/14 14:58
# @Author  : hccfm
# @File    : 图像验证码.py
# @Software: PyCharm

"""
字符图像验证码处理
：使用的tesseract 验证去识别验证码，当图像干扰比较大时，处理时出错大，可进行图像处理。
"""
import requests
from PIL import Image
import pytesseract

url = 'http://my.cnki.net/elibregister/CheckCode.aspx'
url = 'http://fw.cq-cable.com:8762/imgcode/loadCode'

def main():
    response = requests.get(url)
    with open('CheckCode.png','wb') as fw:
        fw.write(response.content)

    img = Image.open('CheckCode.png')
    img.show()
    result = pytesseract.image_to_string(img)
    print("未进行处理，出错机率很大:",result)

    img = img.convert('L')  # 进行灰度处理

    threshold = 128     # 二值化阈值
    t_list = []
    for i in range(256):
        if i < threshold:
            t_list.append(0)
        else:
            t_list.append(1)
    img = img.point(t_list, '1')

    # img.show()
    result = pytesseract.image_to_string(img)
    print("处理后：",result)

if __name__ == '__main__':
    main()