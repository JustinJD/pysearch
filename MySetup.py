from distutils.core import setup
import py2exe
import os
setup(console=["pySearch.py"])
"""
os.system('python MySetup.py py2exe')
"""
# 用于生成windows可执行文件
# 在控制台输入命令"python MySetup.py py2exe", 程序会在根目录下生成文件夹dist, 里面包含有目标程序的可执行文件
