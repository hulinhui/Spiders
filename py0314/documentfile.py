import os
from pathlib import Path

dir_path = 'C:/Users/hlh/Downloads/Documents'  # 需要整理的文件路径

FILE_FORMATS = {
    "图片资料": [".jpg", ".jpeg", ".bpm", ".png", ".png", ".gif"],
    "文档资料": [".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt", ".md"],
    "视频资料": [".mp4", ".avi", ".wmv"],
    "音频文件": [".mp3", ".flac"],
    "压缩文件": [".rar", ".zip", ".tar", ".gz", ".7z", ".bz"],
    "脚本文件": [".ps1", ".sh", ".bat", ".py", ".js"],
    "可执行文件": [".exe", ".msi"],
    "网页文件": [".html", ".xml", ".mhtml", ".html"],
    "快捷方式": [".link"]

}


def organize_file():
    for myfile in os.scandir(dir_path):
        if myfile.is_file():
            file_path = Path(os.path.join(dir_path, myfile.name))
            lower_file_name = file_path.suffix.lower()
            if lower_file_name:
                for file_type in FILE_FORMATS:
                    if lower_file_name in FILE_FORMATS[file_type]:
                        new_filepath = Path(os.path.join(dir_path, file_type))
                        new_filepath.mkdir(exist_ok=True)
                        file_path.rename(new_filepath.joinpath(myfile.name))
            else:
                print(f'{myfile.name}不是标准文件，无后缀名')
        else:
            print(f"{myfile.name}:是文件夹")
    print("文件整理完毕！")


def restore_files():
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            old_filepath = Path(os.path.join(root, file))
            old_filepath.rename(Path(dir_path).joinpath(file))
    remove_dir()
    print(f'全部文件已恢复到整理前的文件夹')


def remove_dir():
    for files in os.scandir(dir_path):
        if files.is_dir():
            if files.name in FILE_FORMATS.keys():
                os.rmdir(os.path.join(dir_path, files.name))
                print(f'删除整理的文件夹：{files.name}')
            else:
                continue
        else:
            continue


def restore_files_2(path):
    for my_files in os.scandir(path):
        if my_files.is_file():
            old_filepath = Path(os.path.join(path, my_files.name))
            new_filepath = Path(os.path.join(dir_path, my_files.name))
            old_filepath.rename(new_filepath)
        elif my_files.is_dir():
            dirpath = os.path.join(path, my_files.name)
            restore_files_2(dirpath)
        else:
            print("未知文件类型")


if __name__ == '__main__':
    organize_file()  # 整理文件
    # restore_files()            #还原文件
    # restore_files_2(dir_path)
