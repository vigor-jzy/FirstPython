#!/usr/bin/env/python3
# -- coding=utf-8 --
class NumberException(Exception):
    def __init__(self,num):
        self.num = num
        pass

    def __str__(self):
        return '数字为{}'.format(self.num)
        pass


def test():
    num = input('请输入。。')
    try:
        if len(num) > 1:
            raise NumberException(num)
            pass
        pass
    except NumberException as msg:
        print(msg)
        pass

test()