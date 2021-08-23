from lxml import etree
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import tkinter
from win32.lib import win32con
import win32gui
import win32print
from win32api import GetSystemMetrics
# from collections import Iterable  # 导入Iterable类，以便判断对象是否可迭代
import os
import time

# 配置浏览器驱动路径
DRIVER_PATH = "D:\\common software\\Google\\Chrome\\Application\\chromedriver.exe"


def get_links(filename):
    '''获得当前页面的暗链列表'''
    tree = etree.parse(filename, parser=etree.HTMLParser(encoding="utf-8"))
    # 选取所有的a标签
    res = tree.xpath('//a')
    link_list = []
    for r in res:
        link = r.get('href')
        if link is not None and link != '#' and '?page=' not in link:
            link = 'http://127.0.0.1:8000'+link           
            link_list.append(link)
    return link_list







