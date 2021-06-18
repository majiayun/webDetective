


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
        if i == 0:
            blocks_size_not_included.append(size_list[i])
        else:

            for j in blocks_size_not_included:

                # j节点块包含当前节点块
                if size_list[i][1] >= j[1] and size_list[i][2] >= j[2] and size_list[i][1] + \
                        size_list[i][3] <= j[1] + j[3] and size_list[i][2] + size_list[i][4] <= j[2] + j[4]:

                    break
                # 当前节点块包含j节点块，删去j节点块
                elif size_list[i][1] <= j[1] and size_list[i][2] <= j[2] and size_list[i][1] + size_list[i][3] >= j[1] + j[3] and \
                        size_list[i][2] + size_list[i][4] >= j[2] + j[4]:

                    blocks_size_not_included.remove(j)
                    blocks_size_not_included.append(size_list[i])
                else:
                    if size_list[i] not in blocks_size_not_included:
                        blocks_size_not_included.append(size_list[i])
    return blocks_size_not_included



nodes_size_list = [
                       ['/html/body/div[2]/div[2]/div/table/tbody/tr[1]', 28, 1297, 659, 22],
                       ['/html/body/div[2]/div[2]/div/table/tbody/tr[1]/td[5]', 291, 1297, 190, 22],
                       ['/html/body/div[2]/div[2]/div/table/tbody/tr[1]', 28, 1297, 659, 22],

                       ['/html/body/div[2]/div[2]/div/table/tbody/tr[2]', 28, 1321, 659, 22],
                       ['/html/body/div[2]/div[2]/div/table/tbody/tr[2]/td[5]', 291, 1321, 190, 22],
                       ['/html/body/div[2]/div[2]/div/table/tbody/tr[2]', 28, 1321, 659, 22],

                       ['/html/body/div[2]/div[2]/div/table/tbody/tr[3]', 28, 1345, 659, 22],
                       ['/html/body/div[2]/div[2]/div/table/tbody/tr[3]/td[5]', 291, 1345, 190, 22],
                       ['/html/body/div[2]/div[2]/div/table/tbody/tr[3]', 28, 1345, 659, 22],

                       ['/html/body/div[2]/div[2]/div/table/tbody/tr[4]', 28, 1369, 659, 22],
                       ['/html/body/div[2]/div[2]/div/table/tbody/tr[4]/td[5]', 291, 1369, 190, 22],
                       ['/html/body/div[2]/div[2]/div/table/tbody/tr[4]', 28, 1369, 659, 22],

                       ['/html/body/div[2]/div[2]/div/table/tbody/tr[5]', 28, 1393, 659, 22],
                       ['/html/body/div[2]/div[2]/div/table/tbody/tr[5]/td[5]', 291, 1393, 190, 22],
                       ['/html/body/div[2]/div[2]/div/table/tbody/tr[5]', 28, 1393, 659, 22],
                       ['/html/body/div[2]/div[2]/div/div[3]/nav/ul', 28, 1433, 718, 58]]

size_list = get_blocks_not_included(nodes_size_list)
print(size_list)


si=[['/html/body/div[1]', 8, 8, 758, 116],
    ['/html/body/div[2]/div[2]/ol', 8, 787, 758, 78],
    ['/html/body/div[2]/div[2]/div/div[2]/form/div[1]', 28, 953, 718, 119],
    ['/html/body/div[2]/div[2]/div/div[2]/form/div[2]/div[2]/div', 28, 1113, 718, 39],
    ['/html/body/div[2]/div[2]/div/div[2]/form/div[2]/div[4]/div', 28, 1193, 718, 39],
    ['/html/body/div[2]/div[2]/div/table/thead/tr', 28, 1273, 659, 22],
    ['/html/body/div[2]/div[2]/div/table/tbody/tr[1]', 28, 1297, 659, 22],
    ['/html/body/div[2]/div[2]/div/table/tbody/tr[1]/td[5]', 291, 1297, 190, 22],
    ['/html/body/div[2]/div[2]/div/table/tbody/tr[2]', 28, 1321, 659, 22],
    ['/html/body/div[2]/div[2]/div/table/tbody/tr[2]/td[5]', 291, 1321, 190, 22],
    ['/html/body/div[2]/div[2]/div/table/tbody/tr[3]', 28, 1345, 659, 22],
    ['/html/body/div[2]/div[2]/div/table/tbody/tr[3]/td[5]', 291, 1345, 190, 22],
    ['/html/body/div[2]/div[2]/div/table/tbody/tr[4]', 28, 1369, 659, 22],
    ['/html/body/div[2]/div[2]/div/table/tbody/tr[4]/td[5]', 291, 1369, 190, 22],
    ['/html/body/div[2]/div[2]/div/table/tbody/tr[5]', 28, 1393, 659, 22],
    ['/html/body/div[2]/div[2]/div/table/tbody/tr[5]/td[5]', 291, 1393, 190, 22],
    ['/html/body/div[2]/div[2]/div/div[3]/nav/ul', 28, 1433, 718, 58]
    ]
