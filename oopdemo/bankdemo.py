# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         bankdemo
# Description:  面向对象高级实战演练之银行系统
# Author:       hlh
# Date:      2024/5/2 15:52

# 1 - 银行管理员(使用管理员密码)查看所有用户信息
# 2 - 进入银行系统提示功能
# 3 - 用户密码管理
# 4 - 账户开户/销户
# 5 - 存款/取款
# 6 - 用户间转账
# 7 - 用户余额查询
# 8 - 常见错误检查和提示
# -------------------------------------------------------------------------------
import random
import string


class aAccount:
    def __init__(self, name, pwd, money):
        self.name = name
        self.password = pwd
        self.money = money
        self.user_id = self.__get_random_char(6)

    def __str__(self):
        return f'''成功创建账户! 
        【账户ID】: {self.user_id}
        【账户名】:  {self.name}
        【账户余额】: {self.money}'''

    @staticmethod
    def __get_random_char(num):
        all_str = string.ascii_uppercase + string.digits
        str_list = random.choices(all_str, k=num)
        return ''.join(str_list)


class Bank(object):
    def __init__(self, bank_name, bank_pwd):
        self.name = bank_name
        self.pwd = bank_pwd
        self.accounts = dict()
        self.api_map = None

    def add_order_set(self, func_map):
        setattr(self, 'api_map', func_map)
        self.query_support_func(custom=True)

    def query_support_func(self, custom=False, *args):
        if not custom:
            print(f"""
                            ===== 欢迎进入【{self.name}银行】系统 =====
                            【本银行支持以下业务】:
                                <查询可办理的业务>
                                <查询余额>
                                <存取款>
                                <转账>
                                <账户开户>
                                <账户销户>
                        """)
        elif custom and isinstance(self.api_map, dict):
            menu_str = f'''
            ===== 欢迎进入【{self.name}银行】系统 =====
            <本银行支持以下业务>:
 
            【指令】\t\t=>\t\t【功能说明】
            '''
            for custom_order, func_tuple in self.api_map.items():
                if isinstance(custom_order, (int, str)) and len(func_tuple) == 2 and isinstance(func_tuple[1], str):
                    menu_str += f"""{custom_order}\t\t=>\t\t"{func_tuple[1]}"\n\t\t\t\t"""
                else:
                    print('''自定义指令集格式错误，请按如下格式设置指令集:
                        {
                            操作指令1:(功能函数1, 功能描述1),
                            操作指令2:(功能函数2, 功能描述2),
                            .....
                        }
                    ''')
            print(menu_str)
        else:
            print("自定义指令集格式错误")

    def api(self, order_no):
        if not isinstance(self.api_map, dict):
            print('请先添加接口指令集！')
            return
        func_tuple = self.api_map.get(order_no)
        if func_tuple and isinstance(func_tuple, tuple):
            func_tuple[0]()
        else:
            print(f"指令 {order_no} 暂未收录, 请在先在接口指令集中添加指令！")

    def query_all_user(self, input_num=2, *args):
        for _ in range(input_num):
            pwd = input('请输入管理员密码：')
            if self.pwd == pwd:
                print(f'共计 {len(self.accounts)} 名用户；名单如下: ')
                for index, account in enumerate(self.accounts.values(), 1):
                    print(f'{index} >>【账户ID】: {account.user_id}  【账户名】: {account.name}  【账户余额】: {account.money}')
                break
            else:
                print(f"密码输出错误, 请重新输入！")
        else:
            print('密码输入错误超过尝试次数！')

    def query_money(self, account_id=None, *args):
        print("\n-------------------【正在查询】-------------------")
        account_id = account_id or input('请输入查询用户ID：')
        account = self.checkout_account_by_id(account_id)
        if not account or not self.check_pwd_correct_by_AccountID(account_id):return
        print(f'''
        【账户ID】: {account.user_id}
        【账户名】:  {account.name}
        【账户余额】: {account.money}
        ''')

    def add_money(self, account_id=None, a_money=None, *args):
        print("\n-------------------【正在存入】-------------------")
        account_id = account_id or input("请输入存入账户ID: ")
        account = self.checkout_account_by_id(account_id)
        if not account: return
        money = a_money or input('请输入存款金额:')
        account.money += int(money)
        print(f"用户 {account.name} 名下账户【{account_id}】成功存入 {money} 元,【账户余额】:{account.money}")
        return money

    def reduce_money(self, account_id=None, r_money=None, *args):
        print("\n-------------------【正在支取】-------------------")
        account_id = account_id or input('请输入支取账户ID: ')
        account = self.checkout_account_by_id(account_id)
        money = r_money or input('请输入支取金额: ')
        money = int(money)
        if not account or not self.check_pwd_correct_by_AccountID(account_id) or not money: return
        if account.money < money:
            print("账户余额不足!")
            return
        account.money -= money
        print(f"用户 {account.name} 账户【{account_id}】成功支取 {money} 元,【账户余额】:{account.money}")
        return money

    def transfer_money(self, *args):
        print("\n-------------------【转账中..... 】-------------------")
        out_account_id = input('请输入金额转出账户ID:')
        out_account = self.checkout_account_by_id(out_account_id)
        if not out_account: return
        in_account_id = input("请输入金额转入账户ID: ")
        in_account = self.checkout_account_by_id(in_account_id)
        if not in_account: return
        money = self.reduce_money(out_account_id)
        if money is not None:
            self.add_money(in_account_id, money)
        else:
            print('转账金额有误')

    def create_account(self, *args):
        name = input('请输入账户名: ')
        password = input('请输入账户密码: ')
        account = aAccount(name, password, money=0)
        print(account)
        self.accounts[account.user_id] = account
        return account

    def del_account(self, *args):
        account_id = input('请输入账户ID: ')
        account = self.checkout_account_by_id(account_id)
        if not account or not self.check_pwd_correct_by_AccountID(account_id): return
        if account.money:
            print('账户余额不为0,请先取出余额以后再操作!')
            return
        self.accounts.pop(account_id)
        print(f'账户【{account_id}】成功销户')
        return True

    def checkout_account_by_id(self, account_id=None, *args):
        if account_id in self.accounts:
            return self.accounts.get(account_id)
        else:
            print(f"未查询到该账号在本银行的账户信息！请先开户或重新确认银行账号！")

    def check_pwd_correct_by_AccountID(self, account_id=None, input_num=3, *args):
        account_id = account_id or input('请输入账户ID:')
        account = self.checkout_account_by_id(account_id)
        if not account: return False
        for _ in range(input_num):
            pwd = input('请输入操作密码:')
            if account.password == pwd:
                return True
            else:
                print(f"账户 {account.user_id} 密码输出错误, 请重新输入！")
        else:
            print("密码输入错误超过尝试次数！")
            return False


def custom():
    print("这里是自定义功能函数!")


if __name__ == '__main__':
    kylin = Bank('麒麟', '999999')
    func_map = {
        # 操作指令：（功能函数，功能描述）
        "admin": (kylin.query_all_user, "管理员操作"),
        "业务办理": (kylin.query_support_func, "查询可办理的业务"),
        "余额查询": (kylin.query_money, "查询余额"),
        "存款": (kylin.add_money, "存款"),
        "取款": (kylin.reduce_money, "取款"),
        "转账": (kylin.transfer_money, "转账"),
        "开户": (kylin.create_account, "账户开户"),
        "销户": (kylin.del_account, "账户销户"),
        "其他业务": (custom, "其他业务办理"),

    }
    kylin.add_order_set(func_map)
    while True:
        order_no = input('请选择您需要办理的业务:')
        if order_no.upper() == 'Q':
            break
        kylin.api(order_no)
