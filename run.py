# -*- coding: utf-8 -*-
# @Author : 艾登Aiden
# @Email : aiden2048@qq.com
# @Date : 2021-11-25

from genericpath import samestat
import os
import time
import zipfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# """ d:\Code\Spider_Armies\APP """
INPUT_APK_DIR = os.path.join(BASE_DIR, "input_apk")
TOOLS_DIR = os.path.join(BASE_DIR, "tools")
VIEW_DIR = os.path.join(BASE_DIR, "view")
WRITE_DIR = os.path.join(BASE_DIR, "write")

for dir in [BASE_DIR, INPUT_APK_DIR, TOOLS_DIR, VIEW_DIR, WRITE_DIR]:
    if not os.path.exists(dir):
        raise Exception("没有文件夹:" + dir)

def scan_dir(path):
    if not os.path.isdir(path):
        raise Exception("不是有效路径:" + path)
    dir_list = []
    for root, dirs, list in os.walk(path): 
        for i in list:
            dir = os.path.join(root, i)
            if i[-4:] in ".apk":
                pass
            dir_list.append([i, dir])
    return dir_list

APK_LIST = scan_dir(os.path.join(BASE_DIR, "input_apk"))
if APK_LIST == []:
    print(".apk文件不存在")
    time.sleep(3)
    raise Exception(".apk文件不存在")


# apk反编译(查看)
def view_decompile_apk(apk_name):

    if apk_name[-4:] not in '.apk':
        raise Exception('Apk文件不存在')
    old_file_name  = os.path.join(INPUT_APK_DIR, apk_name)
    new_file_name  = os.path.join(INPUT_APK_DIR, apk_name[:-4] + '.zip')
    # 更改后缀
    os.rename(old_file_name, new_file_name)
    # print(old_file_name)
    # print(new_file_name)
    name_dir = os.path.join(VIEW_DIR, apk_name[:-4])
    zip_file = zipfile.ZipFile(new_file_name)
    for file in zip_file.namelist():
        zip_file.extract(file, name_dir)
    zip_file.close()
    # 恢复后缀
    os.rename(new_file_name, old_file_name)
    print(f"Classes.dex file: {os.path.join(name_dir, 'classes.dex')}")
    # dex2jar
    dex2jar(name_dir, apk_name[:-4])
    return


def dex2jar(dir, name):
    """
    dir: classes.dex 文件目录
    name: apk名称, 不带.apk后缀
    """
    # dex2jar_tools = "dex-tools-2.1"
    dex2jar_tools = "dex-tools-2.1-SNAPSHOT"
    
    dex2jar_tools_path = os.path.join(TOOLS_DIR, dex2jar_tools)
    classes_dex = "Classes.dex"
    
    # classes.dex 路径
    classes_dex_path = os.path.join(dir, classes_dex)
    # jar生成路径
    jar_path = os.path.join(f'{dir}-jar', f'{name}_{classes_dex}2jar.jar')

    os.chdir(dex2jar_tools_path)
    os.system(f'd2j-dex2jar.bat -f {classes_dex_path} -o {jar_path}')

    if not os.path.exists(jar_path):
            raise Exception(f"错误, 生成 jar 失败, apk: {name}")
    else:
        print(f"Successful jar file: {jar_path}")
    return


def write_decompile_apk(filename):
    name = filename[:-4]
    decompile_dir  = os.path.join(WRITE_DIR, name)
    # 没有目录就新建
    os.path.exists(decompile_dir) or os.mkdir(decompile_dir)

    apktool_jar_path = os.path.join(TOOLS_DIR, "apktool.jar")
    os.chdir(TOOLS_DIR)
    os.system(f'java -jar {apktool_jar_path} d -f {os.path.join(INPUT_APK_DIR, filename)} -o {decompile_dir}')

    samli_dir = os.path.join(decompile_dir, 'smali')
    if not os.path.exists(samli_dir):
            raise Exception(f"错误, 生成 smali 失败, apk: {filename}")
    else:
        print(f"Successful smali dir: {samli_dir}")
    return


def compile_apk(filename):
    name = filename[:-4]
    apktool_jar_path = os.path.join(TOOLS_DIR, "apktool.jar")
    decompile_dir = os.path.join(WRITE_DIR, name)

    compile_apk_path = os.path.join(decompile_dir, 'dist', f'{name}-new.apk')
    # xxx文件夹项目打包成xxx-new.apk安装包
    # java -jar apktool.jar b xxx -o xxx-new.apk
    
    os.chdir(TOOLS_DIR)
    os.system(f'java -jar {apktool_jar_path} b -f {decompile_dir} -o {compile_apk_path}')

    if not os.path.exists(compile_apk_path):
        raise Exception(f"错误, 生成 compile_apk 失败, apk: {filename}")
    else:
        print(f"Successful compile_apk file: {compile_apk_path}")
    return compile_apk_path


def to_apk_sign(filename):
    name = filename[:-4]
    compile_apk_path = os.path.join(WRITE_DIR, name, 'dist', f'{name}-new.apk')
    compile_apk_sign_dir = os.path.join(WRITE_DIR, f'{name}-sign')
    compile_apk_sign_path = os.path.join(WRITE_DIR, f'{name}-sign', f'{name}-new-sign.apk')

    # 没有目录就新建
    os.path.exists(compile_apk_sign_dir) or os.mkdir(compile_apk_sign_dir)
    
    os.chdir(TOOLS_DIR)
    cmd = f'java -jar signapk.jar platform.x509.pem platform.pk8 {compile_apk_path} {compile_apk_sign_path}'
    os.system(cmd)
    if not os.path.exists(compile_apk_sign_path):
        raise Exception(f"错误, 签名失败, apk: {filename}")
    else:
        print(f"Successful 已签名apk file: {compile_apk_sign_path}")
    return


if __name__ == '__main__':

    num = input("====== 选择模式 ====== \n1.反编译(查看) 2.反编译(修改) 3.一键打包并签名 0.退出程序\n输入: ")
    if num == '1':
        print("== 进入反编译-查看模式 ==\n正在生成classes.dex文件...")
        for filename, _ in APK_LIST:
            view_decompile_apk(filename)
        print("Done!")
        time.sleep(4)
        
    elif num == '2':
        print("== 进入反编译-修改模式 ==\n正在生成smali文件夹...")
        for filename, _ in APK_LIST:
            write_decompile_apk(filename)
        print("Done!")
        time.sleep(4)

    elif num == '3':
        print("== 进入一键打包并签名 ==\n正在生成apk文件...")
        for filename, _ in APK_LIST:
            print("正在打包...")
            compile_apk(filename)
            print("正在签名...")
            to_apk_sign(filename)
        print("Done!")

    elif num == '0':
        print("手动退出程序...")
        time.sleep(4)
        quit()

    else:
        print("输入错误, 退出程序...")
        time.sleep(4)
        quit()