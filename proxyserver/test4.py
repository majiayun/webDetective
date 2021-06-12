# import requests
from lxml import etree
from lxml import etree
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import tkinter
from win32.lib import win32con
import win32gui
import win32print
from win32api import GetSystemMetrics

# 配置浏览器驱动路径
DRIVER_PATH = "D:\\common software\\Google\\Chrome\\Application\\chromedriver.exe"
# url = "https://y.qq.com/n/ryqq/search?w=%E5%BC%A0%E7%A2%A7%E6%99%A8&t=song"
#
# resp = requests.get(url)
# # html = resp.text
# # print(html)
#
# html = resp.content.decode("utf-8")
# print(html)


def get_nodes_xpath(filename):
    nodes_xpath_list = []
    parser = etree.HTMLParser(encoding="utf-8")
    tree = etree.parse(filename, parser=parser)
    for element in tree.iter():
        nodes_xpath_list.append(element.getroottree().getpath(element))

    return nodes_xpath_list


def get_leaf_nodes_xpath(nodes_xpath_list):
    '''
    输入：一个页面的原始xpath路径列表
    输出：只包含页面的叶子节点的xpath列表
    '''
    # one_page_xpath.append('0')
    leaf_allnodes_xpath_list = []
    leaf_nodes_xpath_list = []
    # last_tag_list = []

    for i in range(1, len(nodes_xpath_list)):
        # if 'comment()'in nodes_xpath[i]:
        #     continue
        # else:
        pre_xpath = nodes_xpath_list[i - 1]
        cur_xpath = nodes_xpath_list[i]
        if pre_xpath not in cur_xpath:
            leaf_allnodes_xpath_list.append(pre_xpath)
        else:
            if i == len(nodes_xpath_list) - 1:
                leaf_allnodes_xpath_list.append(cur_xpath)

    # 获得body里除注释节点、脚本节点外的的叶子节点的xpath路径
    for leaf_node_xpath in leaf_allnodes_xpath_list:
        if 'body' in leaf_node_xpath and 'comment()' not in leaf_node_xpath and 'script' not in leaf_node_xpath:
            cur_xpath_list = []
            index = leaf_allnodes_xpath_list.index(leaf_node_xpath)
            cur_xpath_list.append(index)
            cur_xpath_list.append(leaf_node_xpath)
            # cur_xpath_list.append(leaf_node_xpath.rpartition('/')[2])
            leaf_nodes_xpath_list.append(cur_xpath_list)

    return leaf_nodes_xpath_list


li = [[55, '/html/body/div[2]/div[2]/ol/li[1]/a/span'],
      [56, '/html/body/div[2]/div[2]/ol/li[2]/a'],
      [57, '/html/body/div[2]/div[2]/ol/li[3]'],
      [58, '/html/body/div[2]/div[2]/ol/div/span'],
      [59, '/html/body/div[2]/div[2]/div/div[1]/h2/strong'],

      ]


def get_pruning_leaf_nodes_xpath(xpath_list):
    pruning_xpath_list = []

    for xpath in xpath_list:
        temp_list = []
        # 这里需要注意有没有/a开头的其他标签
        if xpath[1].find('/a') != -1:
            temp_list.append(xpath[0])
            index = xpath[1].find('/a')
            temp_list.append(xpath[1][:index])
            pruning_xpath_list.append(temp_list)
        elif xpath[1].find('/i') != -1:
            temp_list.append(xpath[0])
            index = xpath[1].find('/i')
            temp_list.append(xpath[1][:index])
            pruning_xpath_list.append(temp_list)
        elif xpath[1].find('/img') != -1:
            temp_list.append(xpath[0])
            index = xpath[1].find('/img')
            temp_list.append(xpath[1][:index])
            pruning_xpath_list.append(temp_list)
        else:
            pruning_xpath_list.append(xpath)

    return pruning_xpath_list


# print(get_pruning_leaf_nodes_xpath(li))

if __name__ == '__main__':
    filename = r"E:\学习\webDetection\preparation\orig_htmls\zhiwang.html"
    # 设置浏览器
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')  # 无头参数
    options.add_argument('--disable-gpu')
    # 启动浏览器
    driver = Chrome(executable_path=DRIVER_PATH, options=options)

    # get参数还是要换成url
    driver.get(filename)

    nodes_xpath_list = get_nodes_xpath(filename)

    leaf_nodes_xpath_list = get_leaf_nodes_xpath(nodes_xpath_list)
    print(leaf_nodes_xpath_list)
    with open(r'E:\学习\webDetection\proxyserver\zhiwang_leaf_nodes_xpath.txt', 'w') as f1:
        for one_line in leaf_nodes_xpath_list:
            f1.write(str(one_line) + '\n')

    pruning_leaf_nodes_xpath_list = get_pruning_leaf_nodes_xpath(
        leaf_nodes_xpath_list)
    print(pruning_leaf_nodes_xpath_list)
