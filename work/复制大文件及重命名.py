import os
import time
import datetime as dt
# 复制文件
def copyFile():
    with open('F:/Bloody5.zip', 'rb') as oldF, open('F:/Bloody5_1.zip', 'wb') as newF:
        while True:
            line = oldF.read(1024)
            #print(line, len(line))
            newF.write(line)
            if len(line) < 1024:
                break


# 重命名
def renameFile():
    path = 'F:/Movie/ajajx'
    list = os.listdir(path)
    for file in list:
        print(file.split('_'))
        # os.rename(os.path.join(path, file), os.path.join(path, '{}_{}'.format('0304', file)))
        # os.rename(os.path.join(path, file), os.path.join(path, file.split('_')[1]))

# 字母文件二合一，排序后存入新文件
def twoInOneFile():
    with open('F:/a.txt') as a, open('F:/b.txt') as b, open('F:/c.txt', 'w') as c:
        line = a.read()
        line += b.read()
        print(len(line))
        line = sorted(line)
        print(len(line))
        c.write(''.join(line))

# 字母排序
def sortList():
    line = [('b','1'),('c','3'),('a','2')]
    # lambda x,y : x + y 等价于 def(x, y): return x + y
    print(sorted(line, key=lambda x:x))

if __name__ == '__main__':
    # renameFile()
    # print(time.time(), time.altzone, time.timezone, time.time_ns(), time.process_time(), time.asctime())
    # twoInOneFile()
    sortList()
