class Game(object):
    age=18
    def __init__(self,name,blood,sex):
        self.name=name
        self.blood=blood
        self.__sex = sex;
        pass
    def set_sex(self, sex):
        print('设置-------')
        self.__sex = sex
        pass
    def get_sex(self):
        print('获取-------')
        return self.__sex
        pass

    sex = property(get_sex,set_sex)

n = Game('123',555,'女fs')
n.sex="ffdfsjdfj"
print(n.sex)

# 第二种方法
class Game1(object):
    age=18
    def __init__(self,name,blood,sex):
        self.name=name
        self.blood=blood
        self.__sex = sex;
        pass
    @property
    def sex(self):
        print('获取')
        return self.__sex

    @sex.setter
    def sex(self, paras):
        print('设置')
        self.__sex=paras

n1 = Game1('123',555,'女fs')
n1.sex="ffdfsjdfj"
print(n1.sex)