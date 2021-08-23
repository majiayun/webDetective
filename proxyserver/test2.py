


# def get_merge_nodes_size(xpath_list):
#     for xpath in xpath_list:
#         elements = driver.find_elements_by_xpath(xpath)
#         cal_list = []
#
#         for element in elements:
#             cur_list = [
#                 element.location["x"],
#                 element.location["y"],
#                 element.size["width"],
#                 element.size["height"]]
#             cal_list.append(cur_list)
#             if len(cal_list) >= 2:
#                 cur_index = cal_list.index(cur_list)
#                 # 横坐标和宽相等，且前一个的纵坐标加上高度等于当前的纵坐标
#                 if cal_list[cur_index][0] == cal_list[cur_index - 1][0] and \
#                         cal_list[cur_index][2] == cal_list[cur_index - 1][2] and \
#                         cal_list[cur_index - 1][1] + cal_list[cur_index - 1][3] == cal_list[cur_index][1]:
#                     pass
#                 # 纵坐标和高相等，且前一个的横坐标加上宽度等于当前的横坐标
#                 if cal_list[cur_index][1] == cal_list[cur_index - 1][1] and \
#                         cal_list[cur_index][3] == cal_list[cur_index - 1][3] and \
#                         cal_list[cur_index - 1][0] + cal_list[cur_index - 1][2] == cal_list[cur_index][0]:
#                     pass
#                 else:
#                     cal_list.remove(cur_list)


def get_blocks_not_included(size_list):
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
                if size_list[i][1] >= blocks_size_not_included[j][1] and size_list[i][2] >= blocks_size_not_included[j][
                    2] \
                        and size_list[i][1] + \
                        size_list[i][3] <= blocks_size_not_included[j][1] + blocks_size_not_included[j][3] \
                        and size_list[i][2] + size_list[i][4] <= blocks_size_not_included[j][2] + \
                        blocks_size_not_included[j][4]:
                    add_list.clear()
                    break
                # 当前节点块包含j节点块，删去j节点块
                elif size_list[i][1] <= blocks_size_not_included[j][1] and size_list[i][2] <= \
                        blocks_size_not_included[j][2] and size_list[i][1] + size_list[i][3] >= \
                        blocks_size_not_included[j][1] + blocks_size_not_included[j][3] and \
                        size_list[i][2] + size_list[i][4] >= blocks_size_not_included[j][2] + \
                        blocks_size_not_included[j][4]:
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



nodes_size_list = [
 ['/html/body/div/div[3]/div/div/div[4]/ul[1]', 8, 1121, 758, 80],
 ['/html/body/div/div[3]/div/div/div[4]/ul[2]/li[1]/div', 48, 1217, 718, 96],
 ['/html/body/div/div[3]/div/div/div[4]/ul[2]/li[2]/div', 48, 1313, 718, 116],
 ['/html/body/div/div[3]/div/div/div[4]/ul[2]', 8, 1217, 758, 1292],
 ['/html/body/div/div[3]/div/div/div[4]/ul[2]/li[4]/div', 48, 1545, 718, 154],
 ['/html/body/div/div[3]/div/div/div[4]/ul[2]/li[5]/div', 48, 1699, 718, 136],
 ['/html/body/div/div[3]/div/div/div[4]/ul[2]', 8, 1217, 758, 1292],
 ['/html/body/div/div[3]/div/div/div[4]/ul[2]/li[7]/div', 48, 1951, 718, 154],
 ['/html/body/div/div[3]/div/div/div[4]/ul[2]', 8, 1217, 758, 1292],
 ['/html/body/div/div[3]/div/div/div[4]/ul[2]', 8, 1217, 758, 1292],
 ['/html/body/div/div[3]/div/div/div[4]/ul[2]/li[10]/div', 48, 2355, 718, 154],
 ['/html/body/div/div[5]/div/div[1]/div[1]/ul', 8, 2698, 758, 80],
 ['/html/body/div/div[5]/div/div[1]/div[2]/ul', 8, 2840, 758, 116],
 ['/html/body/div/div[5]/div/div[1]/div[4]/ul', 8, 3098, 758, 238],
 ['/html/body/div/div[5]/div/div[1]/div[5]/ul', 8, 3398, 758, 40],
 ['/html/body/div/div[5]/div/div[2]', 8, 3454, 758, 110]]


size_list = get_blocks_not_included(nodes_size_list)
print(size_list)

