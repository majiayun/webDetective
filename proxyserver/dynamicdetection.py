from lxml import etree
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import tkinter
from win32.lib import win32con
import win32gui
import win32print
from win32api import GetSystemMetrics
from collections import Iterable  # 导入Iterable类，以便判断对象是否可迭代
import os

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


# 总的计算函数，函数会返回一个列表，包含输入可迭代对象中所有不可迭代对象（按顺序）
def get_item(total: Iterable):
    # 创建用于计算的闭包
    def calculate(lst: Iterable):  # 传入一个可迭代对象
        for item in lst:
            # 如果其中元素不可迭代，说明到达嵌套列表底层。将这个元素加到储存最终结果的result列表中，用return结束此次递归
            if not isinstance(item, list):  # 这里判断元素是否是列表
                result.append(item)

            # 如果元素依旧可以迭代，调用递归对这个元素进行计算
            else:
                calculate(item)

    result = []  # 创建储存结果的列表
    calculate(total)  # 调用闭包计算
    return result  # 返回最终结果


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
    # 指定了etree.HTMLParser来作为一个parser,同时，etree.HTMLParser可以接受编码作为参数，避免编解码问题带来的错误
    tree = etree.parse(filename, parser=etree.HTMLParser(encoding="utf-8"))
    not_visible_nodes_xpath_list=[]
    remove_nodes_xpath_list=[]
    for element in tree.iter():
        attr = element.get('style')
        if attr:
            attr = attr.replace(' ', '')
            # 'type="hidden"' visibility:hidden
            if "display:none" not in attr and 'visibility:hidden' not in attr:
                nodes_xpath_list.append(element.getroottree().getpath(element))
            else:
                not_visible_nodes_xpath_list.append(element.getroottree().getpath(element))
        else:
            nodes_xpath_list.append(element.getroottree().getpath(element))
    for nodes_xpath in nodes_xpath_list:
        for not_visible_nodes_xpath in not_visible_nodes_xpath_list:
            if not_visible_nodes_xpath in nodes_xpath:
                remove_nodes_xpath_list.append(nodes_xpath)
    remove_nodes_xpath_list=list(set(remove_nodes_xpath_list))
    for i in remove_nodes_xpath_list:
        # print(i)
        nodes_xpath_list.remove(i)
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
        if 'body' in leaf_node_xpath and 'comment()' not in leaf_node_xpath and 'script' not in leaf_node_xpath and \
                'svg' not in leaf_node_xpath:

            element = driver.find_element_by_xpath(leaf_node_xpath)
            # 获得叶子节点的宽和高，都不能为0，任何一个为0在页面上都不可见
            width = element.size["width"]
            height = element.size["height"]
            if width != 0 and height != 0:
                leaf_nodes_xpath_list.append(leaf_node_xpath)

            # cur_xpath_list = []
            # index = leaf_allnodes_xpath_list.index(leaf_node_xpath)
            # cur_xpath_list.append(index)
            # cur_xpath_list.append(leaf_node_xpath)
            # leaf_nodes_xpath_list.append(cur_xpath_list)

    return leaf_nodes_xpath_list


def get_pruned_leaf_nodes_xpath(xpath_list):
    '''
    第一次剪枝
    '''
    pruned_xpath_list = []

    for xpath in xpath_list:
        # temp_list = []
        # 这里需要注意有没有/a开头的其他标签
        if xpath.find('/a') != -1:
            # temp_list.append(xpath[0])
            index = xpath.find('/a')
            # temp_list.append(xpath[:index])
            pruned_xpath_list.append(xpath[:index])
        # elif xpath[1].find('/i') != -1:
        #     temp_list.append(xpath[0])
        #     index = xpath[1].find('/i')
        #     temp_list.append(xpath[1][:index])
        #     pruned_xpath_list.append(temp_list)
        elif xpath.find('/img') != -1:

            index = xpath.find('/img')

            pruned_xpath_list.append(xpath[:index])
        elif xpath.find('/input') != -1:

            index = xpath.find('/input')

            pruned_xpath_list.append(xpath[:index])
        elif xpath.find('/button') != -1:

            index = xpath.find('/button')

            pruned_xpath_list.append(xpath[:index])
        else:
            pruned_xpath_list.append(xpath)

    deduplicated_pruned_xpath_list = list(set(pruned_xpath_list))
    deduplicated_pruned_xpath_list.sort(key=pruned_xpath_list.index)

    return deduplicated_pruned_xpath_list


def get_adjacent_similar_xpath(xpath_list):
    '''
    获得叶子节点路径中相邻路径相同的子列表，可以改进，获得尾部标签内的编号顺序
    '''
    similar_xpath_list = []
    # similar_complete_xpath_list = []
    cur_xpath_list = []
    # cur_complete_xpath_list = []
    simple_similar_xpath_list = []
    temp_similar_xpath_list = []

    for i in range(len(xpath_list)):
        if i + 1 < len(xpath_list):
            if xpath_list[i].rpartition('[')[0] + '[]' + xpath_list[i].rpartition(']')[
                    2] == xpath_list[i + 1].rpartition('[')[0] + '[]' + xpath_list[i + 1].rpartition(']')[2]:

                cur_xpath_list.append(xpath_list[i].rpartition(
                    '[')[0] + "()" + xpath_list[i].rpartition(']')[2])

            else:

                cur_xpath_list.append(xpath_list[i])

                similar_xpath_list.append(cur_xpath_list)

                cur_xpath_list = []

        # 最后一项
        else:
            if xpath_list[i].rpartition('[')[0] + '[]' + xpath_list[i].rpartition(']')[
                    2] == xpath_list[i - 1].rpartition('[')[0] + '[]' + xpath_list[i - 1].rpartition(']')[2]:

                cur_xpath_list.append(xpath_list[i].rpartition(
                    '[')[0] + "()" + xpath_list[i].rpartition(']')[2])

                similar_xpath_list.append(cur_xpath_list)

            else:
                cur_xpath_list.append(xpath_list[i])

                similar_xpath_list.append(cur_xpath_list)

    # print(similar_xpath_list)
    # 删去每个子列表中相似的xpath，只保留一个
    for similar_xpath in similar_xpath_list:
        if len(similar_xpath) > 1:
            temp_list = []
            xpath = similar_xpath[0]
            # 删去偶数项
            # similar_xpath = similar_xpath[::2]
            temp_list.append(xpath)
            temp_similar_xpath_list.append(temp_list)
        else:
            temp_similar_xpath_list.append(similar_xpath)
    for xpath in temp_similar_xpath_list:
        simple_similar_xpath_list.append(xpath[0])

    return simple_similar_xpath_list


def get_level_similar_xpath(xpath_list):
    '''
    获得叶子节点路径中相邻路径相同的子列表，可以改进，获得尾部标签内的编号顺序
    '''
    similar_xpath_list = []
    # similar_complete_xpath_list = []
    cur_xpath_list = []
    # cur_complete_xpath_list = []
    simple_similar_xpath_list = []
    temp_similar_xpath_list = []

    for i in range(len(xpath_list)):
        if i + 1 < len(xpath_list):
            if xpath_list[i].rpartition('[')[0] + '[]' + xpath_list[i].rpartition(']')[
                    2] == xpath_list[i + 1].rpartition('[')[0] + '[]' + xpath_list[i + 1].rpartition(']')[2]:
                # if xpath_list[i][1] == xpath_list[i + 1][1]:
                # cur_xpath_list.append(xpath_list[i][0])
                cur_xpath_list.append(xpath_list[i].rpartition(
                    '[')[0] + "()" + xpath_list[i].rpartition(']')[2])
                # item = get_item(complete_xpath_list[i])
                # cur_complete_xpath_list.append(item)
            else:
                # cur_xpath_list.append(xpath_list[i][0])
                cur_xpath_list.append(xpath_list[i])
                # item = get_item(complete_xpath_list[i])
                # cur_complete_xpath_list.append(item)
                similar_xpath_list.append(cur_xpath_list)
                # similar_complete_xpath_list.append(cur_complete_xpath_list)
                cur_xpath_list = []
                # cur_complete_xpath_list = []

        # 最后一项
        else:
            if xpath_list[i].rpartition('[')[0] + '[]' + xpath_list[i].rpartition(']')[
                    2] == xpath_list[i - 1].rpartition('[')[0] + '[]' + xpath_list[i - 1].rpartition(']')[2]:
                cur_xpath_list.append(xpath_list[i].rpartition(
                    '[')[0] + "()" + xpath_list[i].rpartition(']')[2])
                # cur_complete_xpath_list.append(
                #     get_item(complete_xpath_list[i]))
                similar_xpath_list.append(cur_xpath_list)
                # similar_complete_xpath_list.append(cur_complete_xpath_list)
            else:
                cur_xpath_list.append(xpath_list[i])
                # cur_complete_xpath_list.append(
                #     get_item(complete_xpath_list[i]))
                similar_xpath_list.append(cur_xpath_list)
                # similar_complete_xpath_list.append(cur_complete_xpath_list)

    # print(similar_xpath_list)
    # 删去每个子列表中重复的xpath
    for similar_xpath in similar_xpath_list:
        if len(similar_xpath) > 1:
            temp_list = []
            xpath = similar_xpath[0]
            # 删去偶数项
            # similar_xpath = similar_xpath[::2]
            temp_list.append(xpath)
            temp_similar_xpath_list.append(temp_list)
        else:
            temp_similar_xpath_list.append(similar_xpath)
    for xpath in temp_similar_xpath_list:
        simple_similar_xpath_list.append(xpath[0])
    return simple_similar_xpath_list


def get_node_blocks_xpath(xpath_list):
    '''
    获得节点块的路径
    '''
    nodes_xpath_list = []
    for xpath in xpath_list:
        index = xpath.find("(")
        # 路径包含'('
        if index != -1:
            temp_xpath = xpath[:index]
            front_xpath = temp_xpath.rpartition('/')[0]
            nodes_xpath_list.append(front_xpath)
        # 单个叶子节点不可能是表格区域，可舍
        # else:
        #     nodes_xpath_list.append(xpath)
    return nodes_xpath_list


def get_tree_max_deepth(all_xpath_list):
    '''
    得到一个HTML页面形成的xpath列表中最大长度，即DOM树的最大深度
    '''
    tree_deepth_list = []
    for one_xpath in all_xpath_list:
        tree_deepth_list.append(len(one_xpath.split('/')[1:]))
    return max(tree_deepth_list)


def get_clean_xpath(xpath_list):
    '''
    输入：页面的DOM树xpath列表
    输出：页面的每一条xpath以'/'分隔之后形成的路径,去除[]和()
    '''

    new_xpath_list = []
    clean_nodes_xpath_list = []
    for one_xpath in xpath_list:
        new_list = []
        # one_list = one_xpath.split('/')[1:]
        # new_list.append(one_xpath[0])
        # new_list.append(one_list)
        new_xpath_list.append(one_xpath.split('/')[1:])
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
        # clean_xpath_list.append('/'.join(one_clean_list))
        clean_nodes_xpath_list.append('/'.join(one_clean_list))
    return clean_nodes_xpath_list


def get_size_byxpath(xpath_list):
    nodes_size_list = []
    for xpath in xpath_list:
        # print(xpath_list.index(xpath))
        cur_size_list = []
        element = driver.find_element_by_xpath(xpath)
        cur_size_list.append(xpath)
        cur_size_list.append(element.location["x"])
        cur_size_list.append(element.location["y"])
        cur_size_list.append(element.size["width"])
        cur_size_list.append(element.size["height"])
        nodes_size_list.append(cur_size_list)
    return nodes_size_list


def get_visible_leaf_nodes_byxpath(xpath_list):
    '''
    得到可视的节点路径
    '''
    for xpath in xpath_list:
        element = driver.find_element_by_xpath(xpath)
        width = element.size["width"]
        height = element.size["height"]
        # 可改进 ，不在可视窗口范围内
        if width < 2 or height < 2:  # 不设置成0的原因是，存在比较微小的显示
            xpath_list.remove(xpath)
    return xpath_list


def get_fixed_node_blocks(size_list):
    blocks_size_not_included = []
    for i in range(len(size_list)):
        cur_block = size_list[i]
        if i == 0:
            blocks_size_not_included.append(size_list[i])
        else:
            add_list = []
            remove_list = []
            for j in range(len(blocks_size_not_included)):
                # j节点块包含当前节点块
                if size_list[i][1] >= blocks_size_not_included[j][1] and size_list[i][2] >= blocks_size_not_included[j][2] \
                        and size_list[i][1] + \
                        size_list[i][3] <= blocks_size_not_included[j][1] + blocks_size_not_included[j][3] \
                        and size_list[i][2] + size_list[i][4] <= blocks_size_not_included[j][2] + blocks_size_not_included[j][4]:
                    add_list.clear()
                    break
                # 当前节点块包含j节点块，删去j节点块
                elif size_list[i][1] <= blocks_size_not_included[j][1] and size_list[i][2] <= blocks_size_not_included[j][2] and size_list[i][1] + size_list[i][3] >= blocks_size_not_included[j][1] + blocks_size_not_included[j][3] and \
                        size_list[i][2] + size_list[i][4] >= blocks_size_not_included[j][2] + blocks_size_not_included[j][4]:
                    remove_list.append(blocks_size_not_included[j])
                    if len(add_list) == 0:
                        add_list.append(size_list[i])
                else:
                    if len(add_list) == 0:
                        add_list.append(size_list[i])
            blocks_size_not_included += add_list
            for i in remove_list:
                blocks_size_not_included.remove(i)
    return blocks_size_not_included


def get_merge_node_blocks_size(size_xpath_list):
    '''
    合并宽和高相等，横坐标相同，路径相似的节点块
    '''
    merge_data_nodes_size_list = []
    cur_list = []
    count = 1
    for i in range(len(size_xpath_list)):
        cur_node = size_xpath_list[i]
        if i + 1 < len(size_xpath_list):
            if size_xpath_list[i][1] == size_xpath_list[i + 1][1] and \
                    size_xpath_list[i][3] == size_xpath_list[i + 1][3] and \
                    size_xpath_list[i][4] == size_xpath_list[i + 1][4] and \
                    size_xpath_list[i][0].rpartition('[')[0] + '[]' + size_xpath_list[i][0].rpartition(']')[
                    2] == size_xpath_list[i + 1][0].rpartition('[')[0] + '[]' + size_xpath_list[i + 1][0].rpartition(']')[2] and \
                    size_xpath_list[i][2]+size_xpath_list[i][4] == size_xpath_list[i+1][2]:
                if len(cur_list) == 0:
                    cur_list.append(size_xpath_list[i][0])
                    cur_list.append(size_xpath_list[i][1])
                    cur_list.append(size_xpath_list[i][2])
                    cur_list.append(size_xpath_list[i][3])
                    cur_list.append(size_xpath_list[i][4])
                    count += 1
                else:
                    cur_list[-1] += size_xpath_list[i][4]
                    cur_list.insert(0,size_xpath_list[i][0])
                    count += 1
            else:
                if len(cur_list) != 0:
                    cur_list[-1] += size_xpath_list[i][4]
                    cur_list.insert(0,size_xpath_list[i][0])
                    merge_data_nodes_size_list.append(cur_list)
                    cur_list = []
                else:
                    merge_data_nodes_size_list.append(size_xpath_list[i])
    else:
        if len(cur_list) != 0:
            cur_list[-1] += size_xpath_list[i][4]
            cur_list.insert(0,size_xpath_list[i][0])
            merge_data_nodes_size_list.append(cur_list)
        else:
            merge_data_nodes_size_list.append(size_xpath_list[i])
    return merge_data_nodes_size_list


if __name__ == '__main__':
    # filename = r"E:\学习\webDetection\preparation\orig_htmls\yanjiusheng.html"
    # 设置浏览器
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')  # 无头参数
    options.add_argument('--disable-gpu')
    # 启动浏览器
    driver = Chrome(executable_path=DRIVER_PATH, options=options)
    html_path = os.getcwd() + '\\test_files'

    for file in os.listdir(html_path):
        file_path = os.path.join(html_path, file)
        if os.path.getsize(file_path) != 0:
            print(file_path)

        # get参数还是要换成url，直接文件名获取的元素大小与浏览网页显示的大小不一致

            try:
                driver.get(file_path)
                #得到所有节点，同时初步剔除不可见的节点
                nodes_xpath_list = get_nodes_xpath(file_path)
                # print(nodes_xpath_list)

                # 比较费时
                leaf_nodes_xpath_list = get_leaf_nodes_xpath(nodes_xpath_list)
                # print(leaf_nodes_xpath_list)

                # 第二次剔除不可视的节点
                # get_visible_leaf_nodes_byxpath(leaf_nodes_xpath_list)

                pruned_leaf_nodes_xpath_list = get_pruned_leaf_nodes_xpath(
                    leaf_nodes_xpath_list)
                # print(pruned_leaf_nodes_xpath_list)

                similar_xpath_list = get_adjacent_similar_xpath(
                    pruned_leaf_nodes_xpath_list)
                # print(similar_xpath_list)

                level_similar_xpath_list = get_level_similar_xpath(similar_xpath_list)
                # print(level_similar_xpath_list)

                # 获得节点块路径
                node_blocks_xpath_list = get_node_blocks_xpath(level_similar_xpath_list)
                # print(node_blocks_xpath_list)

                # 获得节点块大小，为位置加权做准备
                node_blocks_size_list = get_size_byxpath(node_blocks_xpath_list)
                # print(node_blocks_size_list)

                fixed_node_blocks_size_list = get_fixed_node_blocks(
                    node_blocks_size_list)
                # print(node_blocks_not_included_size_list)

                merge_node_blocks_size_list = get_merge_node_blocks_size(fixed_node_blocks_size_list)
                # print(merge_node_blocks_size_list)

                with open(r'E:\学习\webDetection\proxyserver\test_result.txt', 'a') as f1:
                    f1.write(str(file_path) + '\n')
                    for one_line in merge_node_blocks_size_list:
                        f1.write(str(one_line)+'\n')
            except:

                with open(r'E:\学习\webDetection\proxyserver\test_result.txt', 'a') as f1:
                    f1.write(str(file_path) +'解析错误'+ '\n')



    # with open(r'E:\学习\webDetection\proxyserver\yanjiusheng_node_xpath_list.txt', 'w') as f2:
    #     for one_line in nodes_xpath_list:
    #         f2.write(str(one_line) + '\n')

    # with open(r'E:\学习\webDetection\proxyserver\similar_tag.txt', 'w') as f2:
    #     for one_line in similar_tag_list:
    #         f2.write(str(one_line)+'\n')
