#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: duanliangcong
# Mail: 137562703@qq.com
# Created Time:  2022-11-02 15:00:00
#############################################

# pip install twine
# python setup.py sdist
# twine upload dist/*

#############################################
#################使用方法#####################
#############################################
'''
目录结构
UPSDIST
    ddreport        库文件夹
    MANIFEST.in     配置
    setup.py        当前文件

1.cmd进入UPSDIST目录
2.执行命令：python setup.py sdist
3.执行命令：twine upload dist/*
'''



#### 每次更新需要修改 version 字段

from setuptools import setup, find_packages, find_namespace_packages

setup(
    name = "ddreport",
    version = "4.2",
    keywords = ("pip", "pytest", "testReport"),
    description = "pytest测试报告",
    long_description = "1.解决动态参数化逻辑判断bug；2.环境变量db改写mysql，方便以后区分各种类型的配置；3.新增json_in、json_contain两类型断言；",
    license = "MIT Licence",

    url = "https://blog.csdn.net/weixin_43975720/article/details/130559489",
    author = "duanliangcong",
    author_email = "137562703@qq.com",
    entry_points={"pytest11": ["test_report=ddreport.testReport"]},

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["requests", "jsonpath", "deepdiff"],
)
