import os
import shutil
# 重命名
# os.rename('test1.py','test.py')

# 创建文件夹，只支持单级创建，必须存在父目录
# os.mkdir('tanke/aa')

# 多级创建文件夹
# os.makedirs('tanke/aa/bb')

# 删除单个文件夹，只能是空的
# os.rmdir('tanke')

# 删除多级文件夹，从最底层往上开始删除，为空才能删除
# os.removedirs('tanke/aa/bb')

# 删除多级文件夹，不为空也能删除
# shutil.rmtree('tanke')

# 当前绝对路径
# print(os.getcwd())

# 路径函数
# print(os.path)

# 路径拼接
# print(os.path.join(os.getcwd(), 'feiji'))

# 路径分隔符
# print(os.sep)

# 遍历文件夹下的目录
# print(os.listdir('d:/'))

# 此方法也可以获取目录
with os.scandir('d:/') as dirs:
    for dir in dirs:
        # os.path.isfile是否是文件
        # os.path.isdir是否是目录
        print(dir.path, '文件：{}'.format(os.path.isfile(dir.path)), '文件夹：{}'.format(os.path.isdir(dir.path)))