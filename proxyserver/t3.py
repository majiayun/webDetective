from lxml import etree

ll = [
    ['/html/body/div/div[3]/div/div/div[2]/ul[1]', 8, 1599, 758, 60],

    ['/html/body/div/div[3]/div/div/div[2]/ul[2]/li[1]', 48, 1675, 718, 140],
    ['/html/body/div/div[3]/div/div/div[2]/ul[2]/li[2]', 48, 1817, 718, 140],
    ['/html/body/div/div[3]/div/div/div[2]/ul[2]/li[3]', 48, 1958, 718, 140],
    ['/html/body/div/div[3]/div/div/div[2]/ul[2]/li[4]', 48, 2097, 718, 140],
    ['/html/body/div/div[3]/div/div/div[2]/ul[2]/li[5]', 48, 2239, 718, 140]]


# def merge_data_nodes_size(size_xpath_list):
#     merge_data_nodes_size_list = []
#     cur_list = []
#     count = 1
#     for i in range(len(size_xpath_list)):
#         cur_node = size_xpath_list[i]
#         if i + 1 < len(size_xpath_list):
#             if size_xpath_list[i][1] == size_xpath_list[i + 1][1] and \
#                     size_xpath_list[i][3] == size_xpath_list[i + 1][3] and \
#                     size_xpath_list[i + 1][4] - 5 <= size_xpath_list[i][4] <= size_xpath_list[i + 1][4] + 5:
#
#                 if len(cur_list) == 0:
#                     cur_list.append(size_xpath_list[i][1])
#                     cur_list.append(size_xpath_list[i][2])
#                     cur_list.append(size_xpath_list[i][3])
#                     cur_list.append(size_xpath_list[i][4])
#                     cur_list.append(size_xpath_list[i][0])
#                     count += 1
#                 else:
#                     cur_list[3] += size_xpath_list[i][4]
#                     cur_list.append(size_xpath_list[i][0])
#                     count += 1
#
#             else:
#                 if len(cur_list) != 0:
#                     cur_list[3] += size_xpath_list[i][4]
#                     cur_list.append(size_xpath_list[i][0])
#                     merge_data_nodes_size_list.append(cur_list)
#                     cur_list = []
#                 else:
#                     merge_data_nodes_size_list.append(size_xpath_list[i])
#     else:
#         if len(cur_list) != 0:
#             cur_list[3] += size_xpath_list[i][4]
#             cur_list.append(size_xpath_list[i][0])
#             merge_data_nodes_size_list.append(cur_list)
#         else:
#             merge_data_nodes_size_list.append(size_xpath_list[i])
#     return merge_data_nodes_size_list

def merge_node_blocks_size(size_xpath_list):
    merge_data_nodes_size_list = []
    cur_list = []
    count = 1
    for i in range(len(size_xpath_list)):
        cur_node = size_xpath_list[i]
        if i + 1 < len(size_xpath_list):
            if size_xpath_list[i][1] == size_xpath_list[i + 1][1] and \
                    size_xpath_list[i][3] == size_xpath_list[i + 1][3] and \
                    size_xpath_list[i][4] == size_xpath_list[i + 1][4]:

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
# print(merge_node_blocks_size(ll))



def get_nodes_xpath(filename):
    nodes_xpath_list = []
    # 指定了etree.HTMLParser来作为一个parser,同时，etree.HTMLParser可以接受编码作为参数，避免编解码问题带来的错误
    tree = etree.parse(filename, parser=etree.HTMLParser(encoding="utf-8"))
    not_visible_nodes_xpath_list=[]
    remove_nodes_xpath_list=[]
    for element in tree.iter():
        attr = element.get('style')
        if attr:
            attr=attr.replace(' ', '')
            # 'type="hidden"' visibility:hidden
            if "display:none" not in attr and 'hidden' not in attr:
                nodes_xpath_list.append(element.getroottree().getpath(element))
            else:
                not_visible_nodes_xpath_list.append(element.getroottree().getpath(element))
        else:
            nodes_xpath_list.append(element.getroottree().getpath(element))
    for nodes_xpath in nodes_xpath_list:
        for not_visible_nodes_xpath in not_visible_nodes_xpath_list:
            if not_visible_nodes_xpath in nodes_xpath:
                remove_nodes_xpath_list.append(nodes_xpath)
    for i in remove_nodes_xpath_list:
        nodes_xpath_list.remove(i)
    return nodes_xpath_list

print(get_nodes_xpath(r'E:\学习\webDetection\preparation\orig_htmls\ul.html'))

s='ww ww'
s=s.replace(' ','')
print(s)