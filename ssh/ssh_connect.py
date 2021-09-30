import sys

from paramiko import AuthenticationException
from paramiko.client import SSHClient, AutoAddPolicy
from paramiko import SFTPClient
from paramiko.ssh_exception import NoValidConnectionsError
import logging


class SshClient():
    def __init__(self):
        # 连接客户端
        self.client = SSHClient()

    def ssh_login(self, host_ip, username, password):
        # 登录服务器
        try:
            self.client.set_missing_host_key_policy(AutoAddPolicy())
            self.client.connect(hostname=host_ip, username=username, password=password)
        except AuthenticationException:
            logging.warning('usrname or password error')
            return 1001
        except NoValidConnectionsError:
            logging.warning('connect time out')
            return 1002
        except:
            print("Unexpected error", sys.exc_info()[0])
            return 1003
        return 1000

    def ssh_execute_command(self, command='pwd'):
        # 执行命令行
        stdin, stdout, stderr = self.client.exec_command(command=command)
        print(stdout.read().decode())

    def sftp_put_file(self, local_path, remote_path):
        sftp_client = self.client.open_sftp()
        sftp_info = sftp_client.put(localpath=local_path, remotepath=remote_path, confirm=True)
        if sftp_info:
            print('上传成功')
        else:
            print('上传失败！！')

    def sftp_get_file(self, remote_path, local_path):
        sftp_client = self.client.open_sftp()
        sftp_client.get(remotepath=remote_path, localpath=local_path)
        print("下载完成")

    def sftp_put_or_get(self, local_path, remote_path, mode):
        if mode == 2:
            self.sftp_put_file(local_path, remote_path)
        else:
            self.sftp_get_file(remote_path, local_path)

    def run(self, local_path):
        while True:
            type_name = int(input("请输入查询模式[1、执行命令行 2、上传 3、下载 4、非123即退出]:"))
            if type_name == 1:
                command = input("请输入命令:")
                self.ssh_execute_command(command)
            elif type_name==2 or type_name==3:
                remote_path = input("请输入服务器文件路径:")
                self.sftp_put_or_get(local_path, remote_path, type_name)
            else:
                break

    def ssh_logout(self):
        # 退出客户端
        self.client.close()


def get_hostinfo():
    with open('./serverinfo.txt', 'r') as f:
        hostip, username, password, local_path = f.read().split(',')
        return hostip, username, password, local_path


def main():
    ssh_client = SshClient()
    hostip, username, passwd, local_path = get_hostinfo()
    if ssh_client.ssh_login(hostip, username, passwd) == 1000:
        print('主机连接成功！！！')
        ssh_client.run(local_path)
        ssh_client.ssh_logout()
    else:
        print("主机连接失败")
    print('执行完毕')


if __name__ == '__main__':
    main()
