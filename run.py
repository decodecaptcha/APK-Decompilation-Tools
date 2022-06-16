# -*- coding: utf-8 -*-

import os
import time
import zipfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_APK_DIR = os.path.join(BASE_DIR, "input_apk")
TOOLS_DIR = os.path.join(BASE_DIR, "tools")
VIEW_DIR = os.path.join(BASE_DIR, "view")
WRITE_DIR = os.path.join(BASE_DIR, "write")


print(r"""
    _    ____  _  __      _         _      _____           _     
   / \  |  _ \| |/ /     / \  _   _| |_ __|_   _|__   ___ | |___ 
  / _ \ | |_) | ' /     / _ \| | | | __/ _ \| |/ _ \ / _ \| / __|
 / ___ \|  __/| . \    / ___ \ |_| | || (_) | | (_) | (_) | \__ \
/_/   \_\_|   |_|\_\  /_/   \_\__,_|\__\___/|_|\___/ \___/|_|___/
author: aiden2048                                     
address: https://github.com/aiden2048
""")

# 检测目录是否完整
for dir in [BASE_DIR, INPUT_APK_DIR, TOOLS_DIR, VIEW_DIR, WRITE_DIR]:
    if not os.path.exists(dir):
        raise Exception("Error, Not find the directory:" + dir)


# 检测工具目录
tools_name = "dex-tools-2.1-SNAPSHOT"
dex2jar_tools = os.path.join(TOOLS_DIR, tools_name)
if not os.path.exists(dex2jar_tools):
    raise Exception("Error, Not find the directory or file:" + dex2jar_tools)


def read_all_filename(file_dir):
    """读取当前目录下的所有文件名

    :param file_dir: 目标文件目录
    :return: filenames 多文件名
    """
    filenames = []
    for name in os.listdir(file_dir):
        filenames.append(name)
    return filenames


def get_type_file(file_dir, extensions=['.dex']):
    """只获取指定后缀类型的文件

    :param file_dir: 目标文件目录
    :param extensions: 后缀类型, defaults to ['.dex']
    :return: paths: 多文件路径
    """
    paths = []
    for filename in read_all_filename(file_dir):
        file_path = os.path.join(file_dir, filename)
        if os.path.splitext(file_path)[1] in extensions:
            paths.append(file_path)
    return paths


# paths = get_type_file(BASE_DIR)
# print(paths)

# def scan_dir(path, extensions=['.apk']):
#     """递归读取当前目录下的所有文件名

#     :param path: _description_
#     :raises Exception: _description_
#     :return: _description_
#     """

#     dir_list = []
#     for root, dirs, list in os.walk(path):
#         for i in list:
#             dir = os.path.join(root, i)
#             if i[-4:] in extensions:
#                 dir_list.append([i, dir])
#     return dir_list

# paths = scan_dir(INPUT_APK_DIR)
# print(paths)
# input_apk_path = os.path.join(BASE_DIR, "input_apk")
# if not os.path.isdir(input_apk_path):
#     raise Exception("不是有效路径:" + input_apk_path)

# APK_LIST = scan_dir(INPUT_APK_DIR, extensions=['.apk'])
# print(APK_LIST)
# if APK_LIST == []:
#     raise Exception(".apk文件不存在")


def zip_process(apk_tail):
    """apk反编译(查看)

    :param apk_tail: 文件名+后缀，如app.apk 
    """
    name, ext = os.path.splitext(apk_tail)
    dex_dir = os.path.join(VIEW_DIR, name)

    old_file_name = os.path.join(INPUT_APK_DIR, apk_tail)
    new_file_name = os.path.join(INPUT_APK_DIR, name + '.zip')

    # 更改后缀
    os.rename(old_file_name, new_file_name)

    zip_obj = zipfile.ZipFile(new_file_name)
    for file in zip_obj.namelist():
        zip_obj.extract(file, dex_dir)
    zip_obj.close()

    # 恢复后缀
    os.rename(new_file_name, old_file_name)
    print("dex file generation directory:", dex_dir)
    return


def dex2jar(dex, apk_name):
    """dex 转换为 jar

    :param apk_tail: 文件名+后缀，如app.apk 
    """
    dex_head, dex_tail = os.path.split(dex)
    dex_name, ext = os.path.splitext(dex_tail)
    dex_dir = os.path.join(VIEW_DIR, apk_name)

    # 切换工作目录
    os.chdir(dex2jar_tools)

    # jar生成路径
    jar = os.path.join(f'{dex_dir}-jar', f'{apk_name}_{dex_name}.jar')

    os.system(f'd2j-dex2jar.bat -f {dex} -o {jar}')

    if not os.path.exists(jar):
        raise Exception(f"Error, failed to generate jar, apk: {apk_name}")
    else:
        print(f"Successful, jar file: {jar}")
        return


def view_decompile_apk(apk):
    apk_head, apk_tail = os.path.split(apk)
    # ('d:\Code\My-Github-Code\APK-Decompilation-Tools\APK-Decompilation-Tools\input_apk, app4.apk')
    print(apk_head, apk_tail)
    apk_name, ext = os.path.splitext(apk_tail)
    dex_dir = os.path.join(VIEW_DIR, apk_name)
    print(apk_name, ext)  # ('app4', '.apk')

    zip_process(apk_tail)
    dexs = get_type_file(dex_dir, extensions=['.dex'])
    for dex in dexs:
        # 转换
        dex2jar(dex, apk_name)


def write_decompile_apk(apk):
    # name = filename[:-4]
    apk_head, apk_tail = os.path.split(apk)
    apk_name, ext = os.path.splitext(apk_tail)

    decompile_dir = os.path.join(WRITE_DIR, apk_name)
    # 没有目录就新建
    os.path.exists(decompile_dir) or os.mkdir(decompile_dir)

    apktool_jar_path = os.path.join(TOOLS_DIR, "apktool.jar")
    os.chdir(TOOLS_DIR)
    os.system(f'java -jar {apktool_jar_path} d -f {apk} -o {decompile_dir}')

    samli_dir = os.path.join(decompile_dir, 'smali')
    if not os.path.exists(samli_dir):
        raise Exception(f"Error, failed to generate smali, apk: {apk_tail}")
    else:
        print(f"Successful, smali dir: {samli_dir}")
        return


def compile_apk(apk):
    apk_head, apk_tail = os.path.split(apk)
    apk_name, ext = os.path.splitext(apk_tail)

    apktool_jar = os.path.join(TOOLS_DIR, "apktool.jar")
    b_dir = os.path.join(WRITE_DIR, apk_name)
    output_dir = os.path.join(WRITE_DIR, f'{apk_name}-sign')
    output_apk = os.path.join(b_dir, f'{apk_name}-new.apk')

    os.chdir(TOOLS_DIR)
    os.system(f'java -jar {apktool_jar} b -f {b_dir} -o {output_apk}')

    if not os.path.exists(output_apk):
        raise Exception(f"Error, failed to generate apk, apk: {apk_tail}")
    else:
        print(f"Successful, generate apk : {output_apk}")
        return output_apk


def to_apk_sign(apk):
    apk_head, apk_tail = os.path.split(apk)
    apk_name, ext = os.path.splitext(apk_tail)
    # compile_apk_path = os.path.join(WRITE_DIR, apk_name, 'dist', f'{apk_name}-new.apk')

    # 签名apk 保存的文件夹
    output_dir = os.path.join(WRITE_DIR, f'{apk_name}-sign')
    # 没有目录就新建
    os.path.exists(output_dir) or os.mkdir(output_dir)

    # apk 的导出路径
    output_apk = os.path.join(
        WRITE_DIR, f'{apk_name}-sign', f'{apk_name}-sign.apk')
    os.chdir(TOOLS_DIR)
    os.system(
        f'java -jar signapk.jar platform.x509.pem platform.pk8 {apk} {output_apk}')
    if not os.path.exists(output_apk):
        raise Exception(f"Error, failed to sign, apk: {apk}")
    else:
        print(f"Successful, apk sign: {output_apk}")
        return


if __name__ == '__main__':

    while 1:
        extensions = ['.apk']
        apks = get_type_file(file_dir=INPUT_APK_DIR, extensions=extensions)
        print("Find apk: ", apks)
        if apks == []:
            raise Exception(
                f"Error, Not find 'input_apk' directory {extensions}")
        num = input(
            "====== 选择模式 ====== \n1.反编译(查看) 2.反编译(修改) 3.一键打包并签名 0.退出程序\n输入: ")
        if num == '1':
            print("====== 进入反编译-查看模式 ======")
            for apk in apks:
                view_decompile_apk(apk)
            print("Done!")
            time.sleep(2)
            break

        elif num == '2':
            print("====== 进入反编译-修改模式 ======")
            for apk in apks:
                write_decompile_apk(apk)
            print("Done!")
            time.sleep(2)

        elif num == '3':
            print("====== 进入一键打包并签名 ======")
            for apk in apks:
                print("开始打包...")
                output_apk = compile_apk(apk)

                print("开始签名...")
                to_apk_sign(output_apk)
            print("Done!")
            time.sleep(2)
            break

        elif num == '0':
            print("手动退出程序...")
            time.sleep(2)
            quit()

        else:
            print("Failed to input, exit the program.")
            time.sleep(2)
            quit()
