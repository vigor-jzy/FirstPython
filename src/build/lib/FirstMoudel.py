# 通过from xx import *导入时，只能导入__all__变量指定的函数，通过import直接导入则没有限制
__all__ = ['add']

def add(x, y):
    '''
    添加方法
    :param x:
    :param y:
    :return:
    '''
    return x + y

def test():
    print("内部测试方法")


if __name__ == "__main__":
    test()