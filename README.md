# APK-Decompilation-Tools
A combined tool for APK decompilation.

一个APK反编译的组合工具, 使用 Python 进行简单的集成, 方便快捷地对 APK 包快速反编译与打包.

一、平台: 
    windows 10 下运行

二、依赖:
    python 环境
    java运行环境, 并添加 JAVA_HOME 环境变量
	


三、功能介绍:
    1.反编译(查看) 2.反编译(修改) 3.一键打包并签名 0.退出程序: 
	
	tools 目录: 存放主要模块, 不可修改的

四、使用详细：

	在 input_apk 目录 放入 目标apk, 比如 xxx.apk (必须的)  (理论上支持多个apk同时进行, 目前还在测试中)
	
	执行 run.py
	
	选择功能:
	
		进行 APK 反编译(查看):
			执行1
			在 view 目录下生成 一个项目结构 和 一个 *-jar 目录
			使用主目录的 jd-gui.exe 工具打开 jar 文件 查看源码

		APK 解包再打包并签名:
			先执行2
			再执行3
			在 write 目录下生成 xxx 项目文件 + xxx-sign 文件夹
			xxx-sign.apk 就是可安装的apk

# @Author : 艾登Aiden
# @Email : aidenlen@163.com
# @Date : 2022-01-09


(python_3.6.9) D:\Code\My-Github-Code\APK-Decompilation-Tools\APK-Decompilation-Tools>D:/miniconda3/envs/python_3.6.9/python.exe d:/Code/My-Github-Code/APK-Decompilation-Tools/APK-Decompilation-Tools/run.py
====== 选择模式 ====== 
1.反编译(查看) 2.反编译(修改) 3.一键打包并签名 0.退出程序
输入: 2
== 进入反编译-修改模式 ==
正在生成smali文件夹...
I: Using Apktool 2.6.0 on test.apk
I: Loading resource table...
I: Decoding AndroidManifest.xml with resources...
I: Loading resource table from file: C:\Users\admin\AppData\Local\apktool\framework\1.apk
I: Regular manifest package...
I: Decoding file-resources...
I: Decoding values */* XMLs...
I: Baksmaling classes.dex...
I: Copying assets and libs...
I: Copying unknown files...
I: Copying original files...
Successful smali dir: d:\Code\My-Github-Code\APK-Decompilation-Tools\APK-Decompilation-Tools\write\test\smali
Done!

(python_3.6.9) D:\Code\My-Github-Code\APK-Decompilation-Tools\APK-Decompilation-Tools>D:/miniconda3/envs/python_3.6.9/python.exe d:/Code/My-Github-Code/APK-Decompilation-Tools/APK-Decompilation-Tools/run.py
====== 选择模式 ======
1.反编译(查看) 2.反编译(修改) 3.一键打包并签名 0.退出程序
输入: 3
== 进入一键打包并签名 ==
正在生成apk文件...
正在打包...
I: Using Apktool 2.6.0
I: Smaling smali folder into classes.dex...
I: Building resources...
I: Copying libs... (/lib)
I: Building apk file...
I: Copying unknown files/dir...
I: Built apk...
Successful compile_apk file: d:\Code\My-Github-Code\APK-Decompilation-Tools\APK-Decompilation-Tools\write\test\dist\test-new.apk
正在签名...
Successful 已签名apk file: d:\Code\My-Github-Code\APK-Decompilation-Tools\APK-Decompilation-Tools\write\test-sign\test-new-sign.apk
Done!

