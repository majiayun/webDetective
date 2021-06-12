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
# 获得缩放后的屏幕分辨率，可能与原始分辨率不同
# def get_screen_size():
#     screen = tkinter.Tk()
#     width = screen.winfo_screenwidth()
#     # 获取当前屏幕的宽
#     height = screen.winfo_screenheight()
#     # 获取当前屏幕的高
#     return height, width


def get_real_resolution():
    """获取真实的分辨率"""
    hDC = win32gui.GetDC(0)
    # 横向分辨率
    w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    # 纵向分辨率
    h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return w, h


def get_screen_size():
    """获取缩放后的分辨率"""
    w = GetSystemMetrics(0)
    h = GetSystemMetrics(1)
    return w, h


def diff_str(str1, str2):
    '''
    若两个字符串的差距大于1个字符，返回false，否则返回true
    '''
    count = 0
    index = -1
    if len(str1) != len(str2):
        return False
    else:
        for i in range(len(str1)):
            if count > 1:
                return False
            else:
                if str1[i] != str2[i]:
                    count += 1
                    index = i
        return index

# 使用lxml.etree.parse()解析html文件，该方法默认使用的是“XML”解析器，所以如果碰到不规范的html文件时就会解析错误
# 自己创建html解析器


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

    leaf_allnodes_xpath_list = []
    leaf_nodes_xpath_list = []

    for i in range(1, len(nodes_xpath_list)):
        # if 'comment()'in nodes_xpath[i]:
        #     continue
        # else:
        pre_xpath = nodes_xpath_list[i - 1]
        cur_xpath = nodes_xpath_list[i]
        if pre_xpath not in cur_xpath:
            leaf_allnodes_xpath_list.append(pre_xpath)
        else:
            # 最后一个节点路径
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


def get_pruning_leaf_nodes_xpath(xpath):
    pass


def get_adjacent_same_tag(last_tag_list):
    '''
    得到相邻标签相同的子列表
    '''
    # 去除标签尾部的[]
    last_tag_clean_list = []
    for last_tag in last_tag_list:
        if "[" in last_tag:
            last_tag_clean_list.append(last_tag.partition('[')[0])
        else:
            last_tag_clean_list.append(last_tag)

    same_tag_list = []
    cur_tag_list = []
    for i in range(len(last_tag_clean_list)):
        if i + 1 < len(last_tag_clean_list):
            if last_tag_clean_list[i] == last_tag_clean_list[i + 1]:
                cur_tag_list.append(i)
                cur_tag_list.append(last_tag_clean_list[i])
            else:
                cur_tag_list.append(i)
                cur_tag_list.append(last_tag_clean_list[i])
                same_tag_list.append(cur_tag_list)
                cur_tag_list = []
        else:
            cur_tag_list.append(
                last_tag_clean_list[len(last_tag_clean_list) - 1])
            same_tag_list.append(cur_tag_list)
    return same_tag_list


def get_adjacent_same_xpath(xpath_list):
    '''
    获得叶子节点路径中相邻路径相同的子列表
    '''
    same_xpath_list = []
    cur_xpath_list = []
    simple_same_xpath_list = []

    for i in range(len(xpath_list)):
        if i + 1 < len(xpath_list):
            if xpath_list[i][1].rpartition('[')[0] + '[]' + xpath_list[i][1].rpartition(']')[
                    2] == xpath_list[i + 1][1].rpartition('[')[0] + '[]' + xpath_list[i + 1][1].rpartition(']')[2]:
                # if xpath_list[i][1] == xpath_list[i + 1][1]:
                cur_xpath_list.append(xpath_list[i][0])
                cur_xpath_list.append(xpath_list[i][1].rpartition(
                    '[')[0] + '()' + xpath_list[i][1].rpartition(']')[2])
            else:
                cur_xpath_list.append(xpath_list[i][0])
                cur_xpath_list.append(xpath_list[i][1])
                same_xpath_list.append(cur_xpath_list)
                cur_xpath_list = []
        # 最后一项
        else:
            cur_xpath_list.append(xpath_list[i][0])
            cur_xpath_list.append(xpath_list[i][1].rpartition(
                '[')[0] + '()' + xpath_list[i][1].rpartition(']')[2])
            same_xpath_list.append(cur_xpath_list)
    # print(same_xpath_list)
    # 删去每个子列表中重复的xpath
    for same_xpath in same_xpath_list:
        if len(same_xpath) > 2:
            xpath = same_xpath[1]
            # 删去偶数项
            same_xpath = same_xpath[::2]
            same_xpath.append(xpath)
            simple_same_xpath_list.append(same_xpath)
        else:
            simple_same_xpath_list.append(same_xpath)
    return simple_same_xpath_list

# 另外一种写法，增加了节点个数的判断
# def get_level_same_xpath(xpath_list):
#     '''
#     获得层级路径相同的子列表
#     '''
#     same_xpath_list = []
#     cur_xpath_list = []
#     simple_same_xpath_list=[]
#
#     for i in range(len(xpath_list)):
#         if i + 1 < len(xpath_list):
#             if len(xpath_list[i])==len(xpath_list[i+1]):
#                 if xpath_list[i][-1].rpartition('[')[0] + '[]' + xpath_list[i][-1].rpartition(']')[2] == \
#                         xpath_list[i + 1][-1].rpartition('[')[0] + '[]' + xpath_list[i + 1][-1].rpartition(']')[2]:
#                     for j in range(len(xpath_list[i]) - 1):
#                         cur_xpath_list.append(xpath_list[i][j])
#                     cur_xpath_list.append(
#                         xpath_list[i][-1].rpartition('[')[0] + '()' + xpath_list[i][-1].rpartition(']')[2])
#                 else:
#                     for j in range(len(xpath_list[i]) - 1):
#                         cur_xpath_list.append(xpath_list[i][j])
#                     cur_xpath_list.append(xpath_list[i][-1])
#                     same_xpath_list.append(cur_xpath_list)
#                     cur_xpath_list = []
#             else:
#                 for j in range(len(xpath_list[i]) - 1):
#                     cur_xpath_list.append(xpath_list[i][j])
#                 cur_xpath_list.append(xpath_list[i][-1])
#                 same_xpath_list.append(cur_xpath_list)
#                 cur_xpath_list = []
#         #最后一项
#         else:
#             for j in range(len(xpath_list[i]) - 1):
#                 cur_xpath_list.append(xpath_list[i][j])
#             cur_xpath_list.append(xpath_list[i][-1].rpartition('[')[0]+'()'+xpath_list[i][-1].rpartition(']')[2])
#             same_xpath_list.append(cur_xpath_list)
#     for same_xpath in same_xpath_list:
#         count = 0
#         new_list = []
#         for i in same_xpath:
#             if isinstance(i, int):
#                 new_list.append(i)
#             else:
#                 if count == 0:
#                     new_list.insert(0,i)
#                     count += 1
#         simple_same_xpath_list.append(new_list)
#
#     return simple_same_xpath_list


def get_level_same_xpath(xpath_list):
    '''
    获得层级路径相同的子列表
    '''
    same_xpath_list = []
    cur_xpath_list = []
    simple_same_xpath_list = []

    for i in range(len(xpath_list)):
        if i + 1 < len(xpath_list):
            # if len(xpath_list[i])==len(xpath_list[i+1]):
            if xpath_list[i][-1].rpartition('[')[0] + '[]' + xpath_list[i][-1].rpartition(']')[
                    2] == xpath_list[i + 1][-1].rpartition('[')[0] + '[]' + xpath_list[i + 1][-1].rpartition(']')[2]:
                for j in range(len(xpath_list[i]) - 1):
                    cur_xpath_list.append(xpath_list[i][j])
                cur_xpath_list.append(
                    xpath_list[i][-1].rpartition('[')[0] + '()' + xpath_list[i][-1].rpartition(']')[2])
            else:
                for j in range(len(xpath_list[i]) - 1):
                    cur_xpath_list.append(xpath_list[i][j])
                cur_xpath_list.append(xpath_list[i][-1])
                same_xpath_list.append(cur_xpath_list)
                cur_xpath_list = []
        # 最后一项
        else:
            for j in range(len(xpath_list[i]) - 1):
                cur_xpath_list.append(xpath_list[i][j])
            cur_xpath_list.append(
                xpath_list[i][-1].rpartition('[')[0] + '()' + xpath_list[i][-1].rpartition(']')[2])
            same_xpath_list.append(cur_xpath_list)
    for same_xpath in same_xpath_list:
        count = 0
        new_list = []
        for i in same_xpath:
            if isinstance(i, int):
                new_list.append(i)
            else:
                if count == 0:
                    new_list.insert(0, i)
                    count += 1
        simple_same_xpath_list.append(new_list)

    return simple_same_xpath_list


def get_node_blocks_xpath(xpath_list):
    '''
    获得节点块的路径
    '''
    for xpath in xpath_list:
        index = xpath[0].find("(")
        # 路径包含'('
        if index != -1:
            xpath[0] = xpath[0][:index]
            xpath[0] = xpath[0].rpartition('/')[0]
    return xpath_list
# def get_adjacent_same_xpath(xpath_list):
#     '''
#     得到相邻路径相同的子列表
#     '''
#     same_xpath_list = []
#     cur_xpath_list = []
#     simple_same_xpath_list=[]
#
#     for i in range(len(xpath_list)):
#         if i + 1 < len(xpath_list):
#             if diff_str(xpath_list[i][1],xpath_list[i + 1][1]):
#                 cur_xpath_list.append(xpath_list[i][0])
#                 cur_xpath_list.append(xpath_list[i][1])
#             else:
#                 cur_xpath_list.append(xpath_list[i][0])
#                 cur_xpath_list.append(xpath_list[i][1])
#                 same_xpath_list.append(cur_xpath_list)
#                 cur_xpath_list = []
#         #最后一项
#         else:
#             cur_xpath_list.append(xpath_list[i][0])
#             cur_xpath_list.append(xpath_list[i][1])
#             same_xpath_list.append(cur_xpath_list)
#     for same_xpath in same_xpath_list:
#         if len(same_xpath)>2:
#             xpath = same_xpath[1]
#             same_xpath=same_xpath[::2]
#             same_xpath.append(xpath)
#             simple_same_xpath_list.append(same_xpath)
#         else:
#             simple_same_xpath_list.append(same_xpath)
#     return simple_same_xpath_list


def get_tree_max_deepth(all_xpath_list):
    '''
    得到一个HTML页面形成的xpath列表中最大长度，即DOM树的最大深度
    '''
    tree_deepth_list = []
    for one_xpath in all_xpath_list:
        tree_deepth_list.append(len(one_xpath.split('/')[1:]))
    return max(tree_deepth_list)


# def get_clean_xpath(xpath_list):
#     '''
#     输入：页面的DOM树xpath列表
#     输出：页面的每一条xpath以'/'分隔之后形成的路径,去除[]和()
#     '''
#
#     new_xpath_list = []
#     clean_nodes_xpath_list = []
#     for one_xpath in xpath_list:
#         new_list = []
#         one_list = one_xpath[1].split('/')[1:]
#         new_list.append(one_xpath[0])
#         new_list.append(one_list)
#         new_xpath_list.append(new_list)
#     for i in range(len(new_xpath_list)):
#         one_clean_list = []
#         for one in new_xpath_list[i][1]:
#             clean_xpath_list = []
#             if one.endswith(']'):
#                 one = one.split('[')[0]
#                 if one.endswith(')'):
#                     one = one.split('(')[0]
#                     one_clean_list.append(one)
#                 else:
#                     one_clean_list.append(one)
#             else:
#                 one_clean_list.append(one)
#         clean_xpath_list.append(new_xpath_list[i][0])
#         clean_xpath_list.append('/'.join(one_clean_list))
#         clean_nodes_xpath_list.append(clean_xpath_list)
#     return clean_nodes_xpath_list


def get_clean_xpath(xpath_list):
    '''
    输入：页面的DOM树xpath列表
    输出：页面的每一条xpath以'/'分隔之后形成的路径,去除[]和()
    '''

    new_xpath_list = []
    clean_nodes_xpath_list = []
    for one_xpath in xpath_list:
        new_list = []
        one_list = one_xpath[0].split('/')[1:]
        # new_list.append(one_xpath[0])
        # new_list.append(one_list)
        new_xpath_list.append(one_list)
    for xpath in new_xpath_list:
        one_clean_list = []
        for one in xpath:
            clean_xpath_list = []
            if one.endswith(']'):
                one = one.split('[')[0]
                one_clean_list.append(one)
            elif one.endswith(')'):
                one = one.split('(')[0]
                one_clean_list.append(one)
            else:
                one_clean_list.append(one)
        # clean_xpath_list.append(new_xpath_list[i][0])
        clean_xpath_list.append('/'.join(one_clean_list))
        clean_nodes_xpath_list.append(clean_xpath_list)
    return clean_nodes_xpath_list


def get_size_byxpath(xpath_list):
    nodes_size_list = []
    for xpath in xpath_list:
        # print(xpath_list.index(xpath))
        cur_size_list = []
        element = driver.find_element_by_xpath(xpath[0])
        cur_size_list.append(xpath[0])
        cur_size_list.append(element.location["x"])
        cur_size_list.append(element.location["y"])
        cur_size_list.append(element.size["width"])
        cur_size_list.append(element.size["height"])
        nodes_size_list.append(cur_size_list)
    return nodes_size_list


def get_visible_nodes_byxpath(xpath_list):
    for xpath in xpath_list:
        #获取body节点中除注释节点和脚本节点以外的节点
        if 'body' in xpath and 'comment()' not in xpath and 'script' not in xpath:
            element = driver.find_element_by_xpath(xpath)
            width = element.size["width"]
            height = element.size["height"]
            if width == 0 or height == 0:
                xpath_list.remove(xpath)
    return xpath_list


if __name__ == '__main__':
    filename = r"E:\学习\webDetection\preparation\orig_htmls\allo_result-2021-0402-154200.html"
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
    print(nodes_xpath_list)

    leaf_nodes_xpath_list = get_leaf_nodes_xpath(nodes_xpath_list)
    print(leaf_nodes_xpath_list)
    # clean_leaf_nodes_xpath_list = get_clean_xpath(leaf_nodes_xpath_list)

    same_xpath_list = get_adjacent_same_xpath(leaf_nodes_xpath_list)
    level_same_xpath_list = get_level_same_xpath(same_xpath_list)
    print(level_same_xpath_list)
    level_same_clean_xpath_list = get_clean_xpath(level_same_xpath_list)
    print(level_same_clean_xpath_list)

    node_blocks_xpath_list = get_node_blocks_xpath(level_same_xpath_list)
    print(node_blocks_xpath_list)
    # node_blocks_clean_xpath_list = get_clean_xpath(node_blocks_xpath_list)
    # print(node_blocks_clean_xpath_list)
    # same_tag_list = get_adjacent_same_tag(leaf_nodes_xpath[2] for leaf_nodes_xpath in leaf_nodes_xpath_list)
    node_blocks_size_list = get_size_byxpath(node_blocks_xpath_list)

    # print(node_blocks_size_list)
    # print(same_xpath_list)
    # print(level_same_xpath_list)
    # print(leaf_nodes_size_list)
    # print(get_screen_size())
    # print(get_real_resolution())

    # with open(r'E:\学习\webDetection\proxyserver\leaf_nodes_size.txt', 'w') as f1:
    #     for one_line in leaf_nodes_size_list:
    #         f1.write(str(one_line)+'\n')
    # with open(r'E:\学习\webDetection\proxyserver\leaf_nodes_xpath.txt', 'w') as f2:
    #     for one_line in leaf_nodes_xpath_list:
    #         f2.write(str(one_line)+'\n')

    # with open(r'E:\学习\webDetection\proxyserver\same_tag.txt', 'w') as f2:
    #     for one_line in same_tag_list:
    #         f2.write(str(one_line)+'\n')
