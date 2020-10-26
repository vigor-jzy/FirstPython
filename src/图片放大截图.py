from PIL import Image
import os
path = "D:\Studio\MyEclipse2015Project\FirstPython\img\\"
name = 1
img1 = "{}{}.jpg".format(path, name)
img11 = "{}{}1.png".format(path, name)
img11 = "{}{}11.png".format(path, name)
# 放大比例
scale = 1.25
oldw = 1440
oldh = 1080
wid = int(0.5625 * scale * 2208)
hei = int(0.5625 * scale * 2208 / 0.5625)
sizex = 1242
sizey = 2688
x = (wid - sizex) / 2
y = 0
print("{}___{}".format(wid, hei))
print(scale, wid, hei)

# 文件所属文件夹
# print(os.path.dirname(img1))

# Image.open(img1).resize((wid, hei)).save(img11)

# 截图4个参数依次为（距离左边的宽度，距离上边的宽度，距离左边的宽度+要截图的宽度，距离上边的宽度+要截图的宽度）
#Image.open(img11).crop((x, y, sizex + x, sizey)).save(img11)

# 缩小，放大图片

def smallImg(path, scale):
    print(path)
    img = Image.open(path)
    newPath = os.path.dirname(path) + "\\new.jpg"
    print("{}____{}".format(img.size[0], newPath))
    img.resize((int(img.size[0] * scale), int(img.size[1] * scale))).save(newPath)
    pass

smallImg(img1, 0.5)