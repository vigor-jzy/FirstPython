def copyFile():
    backFile = open("feiji/textBackup.txt", "a", encoding="utf-8")
    with open("feiji/test.txt", "r", encoding="utf-8") as r:
        word = r.readlines()
        print(word)
        backFile.writelines(word)
    pass
    backFile.close()

# 备份大文件
def copyBigFile():
    try:
        with open("feiji/test.txt", "r", encoding="utf-8") as r, open("feiji/back.txt", "a", encoding="utf-8") as w:
            while True:
                content = r.read(3)
                w.write(content)
                if len(content) < 3:
                    break;
    except Exception as msg:
        print(msg)

if __name__ == "__main__":
    #copyFile()
    copyBigFile()