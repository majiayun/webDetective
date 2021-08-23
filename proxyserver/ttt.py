
from lxml import etree

content='''

<span>
    <div>
        <em>你好</em>,北京
        
    </div>
        <div>
        <em>你好</em>,赏
        
    </div>
</span>
'''

page = etree.HTML(content)
re = page.xpath("//span//text()")
print(re)
for i in re:
    if '\n' in i :
        print('kong')
    i = i.strip()
    print(i)