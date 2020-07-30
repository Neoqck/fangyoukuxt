import os
import sys
from core import src

# 将启动文件的绝对路径加入到环境变量
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


if __name__ == '__main__':
    src.run()













