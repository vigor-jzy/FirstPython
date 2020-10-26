#!/usr/bin/env/python3
# -- coding=utf-8 --
import types
class Test(object):
    # __slots__ = ('age','name','sex')
    __name='李四'
    pass

    def getName(self):
        return self.__name
        pass

    def test(self):
        print('宋汶霏防守对方' + self.__name)
        pass

def show(self):
    print('show.......')
    pass

t=Test()
t.sex='女'
print(t.getName())

# print(t.__dict__)