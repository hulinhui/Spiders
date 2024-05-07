import os
import sys

import yaml
from paramiko import AuthenticationException
from paramiko.client import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import NoValidConnectionsError
from py0314.logger_tools.Handle_Logger import HandleLog


class SshClient:
    def __init__(self, ip, user, pwd, path, command=None):
        # 连接客户端
        self.client = SSHClient()
        self.host_ip = ip
        self.username = user
        self.password = pwd
        self.path = path
        self.command = command
        self.logger = HandleLog()

    def ssh_login(self):
        # 登录服务器
        try:
            self.client.set_missing_host_key_policy(AutoAddPolicy())
            self.client.connect(hostname=self.host_ip, username=self.username, password=self.password)
        except AuthenticationException:
            self.logger.warning('usrname or password error')
            return 1001
        except NoValidConnectionsError:
            self.logger.warning('connect time out')
            return 1002
        except:
            self.logger.error(f"Unexpected error {sys.exc_info()[0]}")
            return 1003
        return 1000

    def ssh_execute_command(self, command=None):
        # 执行命令行
        command = command if command else self.command
        stdin, stdout, stderr = self.client.exec_command(command=command)
        self.logger.info(f'命令行执行结果:{stdout.read().decode()}')

    def sftp_put_file(self, filename=None):
        sftp_client = self.client.open_sftp()
        sftp_info = sftp_client.put(localpath=self.path[0], remotepath=self.path[1], confirm=True)
        if sftp_info:
            self.logger.info(f'{filename}上传成功')
        else:
            self.logger.info(f'{filename}上传失败！！')

    def sftp_get_file(self, filename=None):
        sftp_client = self.client.open_sftp()
        sftp_client.get(remotepath=self.path[1], localpath=self.path[0])
        self.logger.info(f"{filename}下载完成")

    def sftp_put_or_get(self, mode):
        if mode == 2:
            self.sftp_put_file()
        else:
            self.sftp_get_file()

    def execute_opera(self):
        while True:
            type_name = int(input("请输入查询模式[1、执行命令行 2、上传 3、下载 4、非123即退出]:"))
            if type_name == 1:
                command = input("请输入命令:")
                self.ssh_execute_command(command)
            elif type_name == 2 or type_name == 3:
                self.sftp_put_or_get(type_name)
                break
            else:
                break

    def run(self):
        if self.ssh_login() == 1000:
            self.logger.info('主机连接成功！！！')
            self.execute_opera()
            self.ssh_logout()
        else:
            self.logger.error("主机连接失败")

    def ssh_logout(self):
        # 退出客户端
        self.client.close()


def get_server_info():
    dir_path = os.path.dirname(__file__)
    yaml_path = os.path.join(dir_path, 'serverinfo.yaml')
    with open(yaml_path, encoding='utf-8') as fp:
        result = fp.read()
        dict_data = yaml.load(result, Loader=yaml.FullLoader)
        return dict_data


def main():
    server_info = get_server_info()
    ssh_client = SshClient(**server_info)
    ssh_client.run()
    ssh_client.logger.info('执行完毕')


if __name__ == '__main__':
    main()
