# -*- coding: utf-8 -*-
#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:         arrangement_file
# Description:  
# Author:       hlh
# Date:      2022/3/17 15:58
#说明:传入一个目录路径，安装目录下文件后缀名作为目录名，进行整理文件;顺便复习下logging模块
#-------------------------------------------------------------------------------
import logging
import os
import shutil

def format_file(dir,logger):
    if os.path.isdir(dir):
        logger.info(f"当前目录{dir}:校验成功！")
        paths=[]
        for file_path,dir_names,file_names in os.walk(r''+dir):
            for file_name in file_names:
                file_name_path = os.path.join(file_path, file_name)
                try:
                    new_dir_path=os.path.join(dir,file_name.split('.')[-1])
                    if os.path.exists(new_dir_path):
                        shutil.move(file_name_path,new_dir_path)
                    else:
                        os.makedirs(new_dir_path)
                        shutil.move(file_name_path,new_dir_path)
                    paths.append(os.path.join(new_dir_path,file_name))
                except Exception as e:
                    logger.error(f'[{file_name_path}]移动发生异常,跳过执行下一条！')

        for path in paths:
            logger.info(f'移动完成的文件:{path}')
    else:
        logger.error('输入的文件夹或者目录不存在！')


def recovery_file(dir,logger):
    if os.path.isdir(dir):
        logger.info('回退操作-当前目录{dir}:校验成功！')
        paths=[]
        for root_path,dir_names,file_names in os.walk(r''+dir):
            for dir_name in dir_names:
                dir_path=os.path.join(root_path,dir_name)
                try:
                    print(os.listdir(dir_path))
                    for file_name in os.listdir(dir_path):
                        file_path=os.path.join(dir_path,file_name)
                        if os.path.isfile(file_path):
                            shutil.move(file_path,dir)
                            paths.append(os.path.join(dir,file_name))
                        else:
                            logger.info('當前文件為目録，不執行文件恢復！')
                            continue

                    if not os.listdir(dir_path):
                        shutil.rmtree(dir_path)
                except Exception as e:
                    logger.error(e)

        for path in paths:
            logger.info(f'恢復移动完成的文件:{path}')
    else:
        logger.error("输入的文件夹或者目录不存在！")





def get_logger():
    logger=logging.getLogger('自动归纳文件')
    logging.basicConfig(format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    logger.setLevel(level=logging.DEBUG)
    return logger



def main():
    dir_path=input("请输入需要整理的目录名称：")
    logger=get_logger()
    #format_file(dir_path,logger)     #整理文件
    recovery_file(dir_path,logger)  #恢復正常



if __name__=='__main__':
    main()