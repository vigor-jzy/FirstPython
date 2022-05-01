# with open("feiji/test.txt", "wb") as f:
    # f.write("时代峰峻\n".encode("utf-8"))
    # f.write("第二行\n".encode("utf-8"))
    # f.write("第三行\n".encode("utf-8"))
    # f.write("第四行\n".encode("utf-8"))

# read 整个读取，大文件时，参数：可以指定读取长度依次往后读取
# readline 一行一行的读取，参数：可以指定读取多少字节
# readlines 整个读取，返回所有行数内容，参数：指定字节数，当前行的字节总数小于该值时，返回改行，大于等于改行字节数时，返回该行及下一行
with open("feiji/test.txt", "r", encoding="utf-8") as f:
    # print(f.read(10))
    # print(f.readline(2))
    # print(f.readline(2))
    # print(f.readline())
    # print(len(f.readlines(7)[1]))
    print(f.readlines(7))