#!/usr/bin/python3
# import hoomd
# import hoomd.md
# import gsd
# import gsd.hoomd
import time
import numpy as np
import random 
import math
import sys
#import pandas
import freud
import os  #处理文件和目录
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from itertools import combinations_with_replacement
from collections import defaultdict, deque, Counter


# ----------- start 读取配置文件, 生成 output folder -----------
import json
from pathlib import Path

with open("config.json") as f:
    config = json.load(f)
### 待传入参数：数目
N0 = config.get('N0',0)   # N0=100 #mol0:异氰酸酯预聚体 NCO值=12.8  E(BA28B)3E 
N1 = config.get('N1',0)  # N1=5 #mol1:PTMG1000
N2 = config.get('N2',0)  # N2=0 #mol2:PTMG2000
N3 = config.get('N3',0)  # N3=10 #mol3:330N
N4 = config.get('N4',0)  # N4=0 #mol4:BDO
N5 = config.get('N5',0)  # N5=0 #mol5:水
N6 = config.get('N6',0)  # N6=0 #mol6:PCCD
Temperature = config.get('Temperature',30)  #k

job_id = str(config['job_id'])
base_path = job_id
assert  Path(base_path).exists(), f"dir {base_path} doesn't exist"

print(f"N0: {N0}, N1: {N1}, N2: {N2}, N3: {N3}, N4: {N4}, N5: {N5}, output_dir: {base_path}") 
# ----------- end  -----------

N001=0 #MDI
N6=0 #mol6:PCCD



# 将数据保存到文本文件中
# 将数据转换为numpy数组，并垂直堆叠为两列
data = np.vstack((x, y)).T
filename = "cluster distribution.txt"
header = "Cluster Size\tNumber of Clusters"
np.savetxt(filename, data, fmt='%.6f', header=header, comments='', delimiter='\t')
exit()
