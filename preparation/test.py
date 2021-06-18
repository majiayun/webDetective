# import bs4
# from bs4 import BeautifulSoup
#
# file = open(r"E:\学习\webDetection\preparation\orig_htmls\allo_result-2021-0402-154200.html", 'r', encoding='utf-8')
# html_string = file.read()
# file.close()
# soup = BeautifulSoup(html_string, 'html.parser')
# # a = soup.table.descendants
#
# child_infos_dic = {}
# i = 1
# for child in soup.table.descendants:#获得table的所有子节点
#     if isinstance(child, bs4.element.Tag): #排除非标签元素干扰
#         if child.string:
#             child_infos_dic[i] = child.name+'-'+child.string.strip()
#         else:
#             child_infos_dic[i] = child.name+'-'+'None'
#         i += 1
# print(child_infos_dic)
# # for id,child_info in child_infos.items():
# # for i in range(len(child_infos.values())):
# #     tag=child_infos.values()[i].split('-')[0]
# #     next_tag=child_infos.values()[i+1].split('-')[0]
# #     if tag==next_tag:
# #         tag+=next_tag
# #
# #     else:
# #         break
# child_infos_list=list(child_infos_dic.values())
# for i in range(len(child_infos_list)):
#     if child_infos_list[i].split('-')[0]==child_infos_list[i+1].split('-')[0]:
#         child_infos_list[i]+=child_infos_list[i+1]
#         del child_infos_list[i+1]
# print(child_infos_list)
#
#
from collections import Iterable  # 导入Iterable类，以便下面判断对象是否可迭代


# 总的计算函数，函数会返回一个列表，包含输入可迭代对象中所有不可迭代对象（按顺序）
def get_item(total: Iterable) -> list:
    # 创建用于计算的闭包
    def calculate(lst: Iterable):  # 传入一个可迭代对象
        for item in lst:
            # 如果其中元素不可迭代，说明到达嵌套列表底层。将这个元素加到储存最终结果的result列表中，用return结束此次递归
            if not isinstance(item, list):  # 这里判断元素是否可以迭代
                result.append(item)

            # 如果元素依旧可以迭代，调用递归对这个元素进行计算
            else:
                calculate(item)

    result = []  # 创建储存结果的列表
    calculate(total)  # 调用闭包计算
    return result  # 返回最终结果


a=[['/html/body/div[1]/div[1]'], ['/html/body/div[1]/div[2]/img'], ['/html/body/div[1]/div[2]/ul/li[1]', '/html/body/div[1]/div[2]/ul/li[2]'], ['/html/body/div[2]/div[1]/div[1]/img']]
for i in a:
    print(get_item(i))

