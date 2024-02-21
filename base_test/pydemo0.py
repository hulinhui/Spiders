# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         装饰器、迭代器、上下文管理器
# Description:  
# Author:       hulinhui779
# Date:      2024/2/21 10:40
# -------------------------------------------------------------------------------
# 类装饰器
class Logger:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print(f"Logging: Calling function {self.func.__name__}")
        return self.func(*args, **kwargs)


@Logger
def say_hello(*args, **kwargs):
    print(f'Hello Wrold {sum(args)}!')


# 迭代器
class MyIterator:
    def __init__(self, iterable):
        self.iterable = iterable
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.iterable):
            result = self.iterable[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration


# 上下文管理器
class MyContextManager:
    def __enter__(self):
        print('Entering the context!')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Exiting the context!')
        if exc_type is not None:
            print(f'Exception: {exc_type},{exc_val}')
        return True

    @staticmethod
    def print_data(value):
        print(value)


if __name__ == '__main__':
    # say_hello(2, 3)

    # my_list = [1, 2, 3, 4, 5]
    # myiter = MyIterator(my_list)
    # for _ in myiter:
    #     print(_)
    # my_iterator = iter(my_list)
    # print(next(my_iterator))

    with MyContextManager() as manager:
        manager.print_data('Hello World')
