import bs4
from bs4 import BeautifulSoup

file = open(r"E:\学习\webDetection\preparation\orig_htmls\allo_result-2021-0402-154200.html", 'r', encoding='utf-8')
html_string = file.read()
file.close()
soup = BeautifulSoup(html_string, 'html.parser')
# a = soup.table.descendants

child_infos_dic = {}
i = 1
for child in soup.table.descendants:#获得table的所有子节点
    if isinstance(child, bs4.element.Tag): #排除非标签元素干扰
        if child.string:
            child_infos_dic[i] = child.name+'-'+child.string.strip()
        else:
            child_infos_dic[i] = child.name+'-'+'None'
        i += 1
print(child_infos_dic)
# for id,child_info in child_infos.items():
# for i in range(len(child_infos.values())):
#     tag=child_infos.values()[i].split('-')[0]
#     next_tag=child_infos.values()[i+1].split('-')[0]
#     if tag==next_tag:
#         tag+=next_tag
#
#     else:
#         break
child_infos_list=list(child_infos_dic.values())
for i in range(len(child_infos_list)):
    if child_infos_list[i].split('-')[0]==child_infos_list[i+1].split('-')[0]:
        child_infos_list[i]+=child_infos_list[i+1]
        del child_infos_list[i+1]
print(child_infos_list)



