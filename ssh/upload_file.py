import os
from ruamel import yaml as ryaml
from ssh.ssh_connect import SshClient


def get_server_info(filename=None):
    if filename is None:
        dir_path = os.path.dirname(__file__)
        yaml_path = os.path.join(dir_path, 'serverinfo.yaml')
    else:
        yaml_path = filename
    data = save_read_file(yaml_path)
    return data


def execute_put_file(obj, server_info, put_flag=True):

    if put_flag:
        # 修改本地文件,返回文件名
        file_name = modify_file(obj, server_info)
        # 上传
        obj.sftp_put_file(file_name)
        # 执行命令
        obj.ssh_execute_command()
    else:
        # 执行命令
        obj.ssh_execute_command()


def save_read_file(yaml_path, yaml_data=None, is_read=True):
    if is_read:
        with open(yaml_path, encoding='utf-8') as fp:
            result = fp.read()
            dict_data = ryaml.load(result, Loader=ryaml.RoundTripLoader)
            return dict_data
    else:
        with open(yaml_path, 'w', encoding='utf-8') as fp:
            ryaml.dump(yaml_data, fp, Dumper=ryaml.RoundTripDumper, allow_unicode=True, default_flow_style=True)


def modify_file(ssh, info):
    local_path = info['path'][0]
    file_name = os.path.basename(local_path)
    proxy_info = get_server_info(local_path)
    proxy_text = proxy_info['changeRequest'][0]['proxy']
    if proxy_text and len(proxy_text.split(',')) > 1:
        proxy_info['changeRequest'][0]['proxy'] = 'proxy[星空]'
        ssh.logger.info(f'修改前代理为：{proxy_text};')
        ssh.logger.info('修改后代理为:proxy[星空];')
    else:
        proxy_info['changeRequest'][0]['proxy'] = 'proxy[巨量],proxy[yyy],proxy[携趣]'
        ssh.logger.info(f'修改前代理为：{proxy_text};')
        ssh.logger.info('修改后代理为:proxy[巨量],proxy[yyy],proxy[携趣];')
    save_read_file(local_path, proxy_info, is_read=False)
    ssh.logger.info(f'本地文件{file_name}:内容修改成功！')
    return file_name


def main():
    # 获取服务器信息及命令、上传文件路径
    server_info = get_server_info()
    # 获取服务器对象
    ssh = SshClient(**server_info)
    # 连接服务器
    if ssh.ssh_login() == 1000:
        ssh.logger.info('主机连接成功！！！')
        execute_put_file(ssh, server_info, put_flag=True)
        # 退出
        ssh.ssh_logout()
    else:
        ssh.logger.error("主机连接失败")


if __name__ == '__main__':
    main()
