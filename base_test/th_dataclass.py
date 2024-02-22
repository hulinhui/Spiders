
# -------------------------------------------------------------------------------
# Name:         dataclass类
# Description:
# Author:       hulinhui779
# Date:      2023/12/9 22:13
# -------------------------------------------------------------------------------
"""
dataclasses.dataclass(*, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False)
1、init【指定是否自动生成__init__，默认自动生成，如果已经有定义同名方法则忽略这个值，也就是指定为False也不会自动生成】
2、repr【同init，指定是否自动生成__repr__；自动生成的打印格式为class_name(arrt1:value1, attr2:value2, ...)】
3、eq  【同init，指定是否生成__eq__；自动生成的方法将按属性在类内定义时的顺序逐个比较，全部的值相同才会返回True】
4、order【自动生成__lt__，__le__，__gt__，__ge__，比较方式与eq相同；如果order指定为True而eq指定为False，将引发ValueError；如果已经定义同名函数，将引发TypeError】
5、unsafehash【同init，指定是否自动生成__repr__；自动生成的打印格式为class_name(arrt1:value1, attr2:value2, ...)】
6、frozen【设为True时对field赋值将会引发错误，对象将是不可变的，如果已经定义了__setattr__和__delattr__将会引发TypeError】
"""

from dataclasses import dataclass, asdict, astuple, is_dataclass


@dataclass(order=True)
class Lang:
    """a dataclass that describes a programming language"""
    name: str = 'python'
    strong_type: bool = True
    static_type: bool = False
    age: int = 28


@dataclass
class Python(Lang):
    tab_size: int = 4
    is_script: bool = True


@dataclass
class Base:
    x: float = 28.0
    y: int = 0


@dataclass
class C(Base):
    z: int = 10
    x: int = 15


if __name__ == '__main__':
    print(Lang())
    print(Lang('java'))
    print(Lang('js', False, True, 23))
    print(Lang('python', True, False, 28) == Lang())  # 数据类是否相等【默认存在等于魔术方法】
    print(Lang('python', True, False, 23) == Lang())  # 数据类是否相等【默认存在等于魔术方法】
    print(Lang('python', True, False, 23) > Lang())  # 数据类大小比较【默认不存在大小比较魔术方法,根据order=True生成】
    print(asdict(Lang()))  # 将数据类实例数据转化为字典
    print(astuple(Lang()))  # 将数据类实例数据转化为元祖
    print(is_dataclass(Lang()))  # 判断一个实例对象是否是数据类
    print(is_dataclass(Lang))  # 判断一个类是否是数据类
    print(Python())  # Python(name='python', strong_type=True, static_type=False, age=28, tab_size=4, is_script=True)
    print(C())  # 子类中的field与基类同名，那么子类将会无条件覆盖基类[C(x=15, y=0, z=10)]
