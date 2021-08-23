from lxml import etree


def get_imgs_xpath(filename):
    '''获得当前页面的img标签列表'''
    tree = etree.parse(filename, parser=etree.HTMLParser(encoding="utf-8"))
    # 选取所有的a标签
    res = tree.xpath('//img')
    img_xpath_list = []
    for r in res:
        img_path = r.getroottree().getpath(r)
        img_xpath_list.append(img_path)
    return img_xpath_list




get_imgs_xpath(r'C:\Users\jiayun.ma\Desktop\webDetection\webDetection\preparation\orig_htmls\allo_result-2021-0402-154200.html')