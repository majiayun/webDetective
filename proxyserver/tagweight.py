# 表格标签
table_tags = {"table": 0.1,
              "thead": 0.1,
              "tbody": 0.2,
              "tfoot": 0.1,
              "tr": 0.1,
              "th": 0.1,
              "td": 0.2,
              "col": 0,
              }

# 列表标签
list_tags = {"ul": 0.1,
             "ol": 0.1,
             "li": 0.2,
             "dl": 0,
             "dt": 0,
             "dd": 0

             }

# 表单和输入标签
input_tags = {"form": 0,
              "imput": 0,
              "button": 0,
              "select": 0,
              "option": 0,
              "label": 0,

              }

# 图像标签
img_tags = {"img": 0,
            "canvas": 0,
            "figure": 0,
            "i": 0,  # 有可能是图像标签
            }

# 音频和视频标签
audio_tags = {"audio": 0,
              "source": 0,
              "track": 0,
              "video": 0,

              }

# 链接标签
link_tags = {"a": 0.1,
             "link": 0,
             "nav": 0

             }

# 样式和语义标签
style_tags = {"div": 0,
              "span": 0,
              "section": 0,
              "header": 0,
              "footer": 0,
              "main": 0,
              "article": 0,
              "details": 0,
              "style": 0,

              }

# 基础标签
base_tags = {"html": 0,
             "head": 0,
             "title": 0,
             "meta": 0,
             "body": 0,
             "h1": 0,
             "h2": 0,
             "h3": 0,
             "h4": 0,
             "h5": 0,
             "h6": 0,
             "p": 0,
             "pre": 0,
             "br": 0,
             "hr": 0,
             "b": 0,
             "i": 0,
             "time": 0,
             "big": 0,
             "small": 0,
             "strong": 0,
             "font": 0,
             }

# 编程标签
code_tags = {"script": 0,
             "object": 0,
             "param": 0,
             }

all_tags = dict(list(table_tags.items()) +
                list(list_tags.items()) +
                list(input_tags.items()) +
                list(img_tags.items()) +
                list(audio_tags.items()) +
                list(link_tags.items()) +
                list(style_tags.items()) +
                list(base_tags.items()) +
                list(code_tags.items()))
# print(dict(list(table_tags.items()) + list(list_tags.items())))
# print(all_tags)
xpath_list = [['html/body/div/div/div/div/form/div/div/div/div/input'],
              ['html/body/div/div/div/div/form/div/input'],
              ['html/body/div/div/div/table/thead/tr/th'],
              ['html/body/div/div/div/table/tbody/tr/td'],
              ['html/body/div/div/div/div/nav/ul/li/a']]


def cal_tag_value(xpath_list):
    for xpath in xpath_list:
        tag_value = 0
        tags_list = xpath[0].split("/")
        for tag in tags_list:
            if tag in all_tags.keys():
                # i=all_tags[tag]
                tag_value += all_tags[tag]
        xpath.append(tag_value)
    return xpath_list


print(cal_tag_value(xpath_list))
