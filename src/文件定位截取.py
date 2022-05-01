with open('feiji/test.txt', 'rb') as f:
    f.seek(-5,2)
    print(f.read(3))
    # 当前光标位置,utf8编码一个中文占3个字节，gbk2个字节
    print(f.tell())
    # seek 偏移光标位置时，打开方式为r只能从文件开头进行偏移
    # f.seek(4,0)
    # print(f.read(2))