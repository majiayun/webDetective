from lxml import etree
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import re
import tkinter
from win32.lib import win32con
import win32gui
import win32print
from win32api import GetSystemMetrics
import os

# 配置浏览器驱动路径
DRIVER_PATH = "D:\\common software\\Google\\Chrome\\Application\\chromedriver.exe"


def get_nodes_xpath(filename):
    nodes_xpath_list = []
    # 指定了etree.HTMLParser来作为一个parser,同时，etree.HTMLParser可以接受编码作为参数，避免编解码问题带来的错误
    tree = etree.parse(filename, parser=etree.HTMLParser(encoding="utf-8"))
    for element in tree.iter():
        attr = element.get('style')
        if attr:
            attr.replace(' ', '')
            if "display:none" not in attr and 'visibility:hidden' not in attr:
                nodes_xpath_list.append(element.getroottree().getpath(element))
        else:
            nodes_xpath_list.append(element.getroottree().getpath(element))
    return nodes_xpath_list

# filename = r"E:\学习\webDetection\preparation\orig_htmls\gupiao.html"
# options = Options()
# options.add_argument('--no-sandbox')
# options.add_argument('--headless')  # 无头参数
# options.add_argument('--disable-gpu')
# # 启动浏览器
# driver = Chrome(executable_path=DRIVER_PATH, options=options)
#
# # get参数还是要换成url，直接文件名获取的元素大小与浏览网页显示的大小不一致
# driver.get("http://music.163.com/#/song?id=31877470")
# print(type(driver.page_source))
# print(driver.page_source)
# nodes=get_nodes_xpath(filename)
# elements = driver.find_elements_by_xpath('/html/body/div/div[3]')
# for i in elements:
#     print(i.location)
#     print(i.size)


# ll=['/html/body/div[1]/div()', '/html/body/div[1]/div[2]/ul/li()', '/html/body/div[2]/div[1]/div[1]', '/html/body/div[2]/div[1]/div[1]/span', '/html/body/div[2]/div[2]/ol/li()', '/html/body/div[2]/div[2]/ol/div/span', '/html/body/div[2]/div[2]/div/div[1]/h2/strong', '/html/body/div[2]/div[2]/div/div[1]/h2/small', '/html/body/div[2]/div[2]/div/div[2]/form/div[1]/div[1]/div/label', '/html/body/div[2]/div[2]/div/div[2]/form/div[1]/div[1]/div/div', '/html/body/div[2]/div[2]/div/div[2]/form/div[1]/div()/div/label', '/html/body/div[2]/div[2]/div/div[2]/form/div[2]/div[1]/div/label', '/html/body/div[2]/div[2]/div/div[2]/form/div[2]/div[1]/div/div', '/html/body/div[2]/div[2]/div/div[2]/form/div[2]/div[2]/div/div()', '/html/body/div[2]/div[2]/div/div[2]/form/div[2]/div[3]/div/label', '/html/body/div[2]/div[2]/div/div[2]/form/div[2]/div[3]/div/div', '/html/body/div[2]/div[2]/div/div[2]/form/div[2]/div[4]/div/div()', '/html/body/div[2]/div[2]/div/div[2]/form/div[2]', '/html/body/div[2]/div[2]/div/table/thead/tr/th()', '/html/body/div[2]/div[2]/div/table/tbody/tr[1]/td()', '/html/body/div[2]/div[2]/div/table/tbody/tr[1]/td[5]/label()', '/html/body/div[2]/div[2]/div/table/tbody/tr[1]/td()/label', '/html/body/div[2]/div[2]/div/table/tbody/tr[1]/td[8]', '/html/body/div[2]/div[2]/div/table/tbody/tr[2]/td()', '/html/body/div[2]/div[2]/div/table/tbody/tr[2]/td[5]/label()', '/html/body/div[2]/div[2]/div/table/tbody/tr[2]/td()/label', '/html/body/div[2]/div[2]/div/table/tbody/tr[2]/td[8]', '/html/body/div[2]/div[2]/div/table/tbody/tr[3]/td()', '/html/body/div[2]/div[2]/div/table/tbody/tr[3]/td[5]/label()', '/html/body/div[2]/div[2]/div/table/tbody/tr[3]/td()/label', '/html/body/div[2]/div[2]/div/table/tbody/tr[3]/td[8]', '/html/body/div[2]/div[2]/div/table/tbody/tr[4]/td()', '/html/body/div[2]/div[2]/div/table/tbody/tr[4]/td[5]/label()', '/html/body/div[2]/div[2]/div/table/tbody/tr[4]/td()/label', '/html/body/div[2]/div[2]/div/table/tbody/tr[4]/td[8]', '/html/body/div[2]/div[2]/div/table/tbody/tr[5]/td()', '/html/body/div[2]/div[2]/div/table/tbody/tr[5]/td[5]/label()', '/html/body/div[2]/div[2]/div/table/tbody/tr[5]/td()/label', '/html/body/div[2]/div[2]/div/table/tbody/tr[5]/td[8]', '/html/body/div[2]/div[2]/div/div[3]/nav/ul/li()']
# def get_nodes_block_xpath(xpath_list):
#     '''
#     获得节点块的路径
#     '''
#     nodes_xpath_list=[]
#     for xpath in xpath_list:
#         index = xpath.find("(")
#         # 路径包含'('
#         if index != -1:
#             temp_xpath = xpath[:index]
#             front_xpath=temp_xpath.rpartition('/')[0]
#             nodes_xpath_list.append(front_xpath)
#         #单个叶子节点不可能是表格区域，可舍
#         # else:
#         #     nodes_xpath_list.append(xpath)
#     return nodes_xpath_list
#
#
# print(get_nodes_block_xpath(ll))
s='''<div class="page-header" style="margin:3px 0px 3px 0px">         


<h2 style="margin-left: 8px"><strong>分配结果</strong>&nbsp;<small>Meter Allocation Result &gt;&gt;</small></h2>     



</div>'''



# print(re.sub(r'[\r\n\f]{2,}','\n',s))

html_path = os.getcwd() + '\\test_files'
count=0
for file in os.listdir(html_path):
    file_path = os.path.join(html_path, file)
    if  os.path.getsize(file_path) != 0:

        print(file_path)
        count+=1
print(count)