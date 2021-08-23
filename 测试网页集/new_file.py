from pathlib import Path

def new_file():
    for i in range(500):
        Path(str(i+1)+'.html').touch()


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    new_file()