import xml.etree.ElementTree as ET
import numpy as np
import os  #处理文件和目录
import matplotlib.pyplot as plt
from pathlib import Path

# N0=100 #mol0:异氰酸酯预聚体 NCO值=12.8  E(BA28B)3E 
# N1=0 #mol1:PTMG1000
# N2=0 #mol2:PTMG2000
# N3=0 #mol3:330N
# N4=1000 #mol4:BDO
# N5=0 #mol5:水

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
Temperature = config.get('Temperature',30)  #k

job_id = str(config['job_id'])
base_path = job_id
assert  Path(base_path).exists(), f"dir {base_path} doesn't exist"

print(f"N0: {N0}, N1: {N1}, N2: {N2}, N3: {N3}, N4: {N4}, N5: {N5}, output_dir: {base_path}") 
# ----------- end  -----------

image_path = f'{base_path}/all_variables.png'

init_NCO=N0*2
init_PTMG1000=N1*2
init_PTMG2000=N2*2
num_A=N0*28*3
all_particles=N0*92+N1*14+N2*28+N3*82+N4*2+N5*2

urethane_particles=['F1','L1','K011','K021','K031','C1']

file_indices = []  # 用于存储文件索引
num_NCO=[]
num_PTMG1000=[]
num_PTMG2000=[]
num_BDO=[]

num_urethane_totals = []  # 用于存储每个文件的计数结果
# base_path = './'
for i in range(100000,120001, 10000):  # 从 0 到 20100000
    filename = f"particles.{i:010d}.xml"  # 格式化文件名，使数字部分有 10 位，前面补零
    filepath = os.path.join(base_path, filename)  # 构建完整路径
    # print(filename)

    if os.path.isfile(filepath):  # 检查文件是否存在
        # 对每个文件进行计数
        tree = ET.parse(filepath)
        root = tree.getroot()

        numF1=0
        numL1=0
        numK011=0
        numK021=0
        numK031=0
        numC1=0
        numE=0
        numC=0
        numL=0
        numF=0

        type_elem = root.find('.//type')
        if type_elem is not None:
            lines = type_elem.text.strip().split('\n')
            for line in lines:
                type_value = line.strip()
                # print(type_value)
                if type_value in urethane_particles:
                    if type_value == 'F1':
                        numF1 += 1
                    elif type_value == 'L1':
                        numL1 += 1
                    elif type_value == 'K011':
                        numK011 += 1
                    elif type_value == 'K021':
                        numK021 += 1
                    elif type_value == 'K031':
                        numK031 += 1
                    elif type_value == 'C1':
                        numC1 += 1
                if type_value == 'E':# NCO的值
                    numE += 1
                if type_value == 'C':# BDO
                    numC += 1
                if type_value == 'L':# PTMG2000
                    numL += 1
                if type_value == 'F':# PTMG1000
                    numF += 1
        num_urethane=numF1+ numL1+ numK011+ numK021+ numK031+ numC1
        # print(numE) 
        # print(numA) 
        # exit()   
        num_urethane_totals.append(num_urethane)
        num_NCO.append(numE)
        num_PTMG1000.append(numF)
        num_PTMG2000.append(numL)
        num_BDO.append(numC)
        file_indices.append(i / 10**4)  # 将文件索引除以 10^4，并添加到列表中
        
num_urethane_totals = np.array(num_urethane_totals) #生成氨基甲酸酯
num_NCO=np.array(num_NCO) #NCO数目
num_PTMG1000=np.array(num_PTMG1000) #PTMG1000的羟基数目
num_PTMG2000=np.array(num_PTMG2000) #PTMG2000的羟基数目
num_BDO=np.array(num_BDO) #PTMG2000的羟基数目
# print(num_NCO)  
# exit()
soft_segment_content=num_A/(all_particles)
text = f'Soft segment content: {soft_segment_content:.2f}'  # 格式化文本
# Check if all arrays are zero
# Plot all variables on the same graph
plt.figure(figsize=(10, 6), dpi=300)

# Plot num_urethane_totals if not all zero
if not np.all(num_urethane_totals == 0):
    plt.plot(file_indices, num_urethane_totals, marker='o', linestyle='-', label='Urethane Particle Count')

# Plot num_NCO if not all zero
if not np.all(num_NCO == 0):
    plt.plot(file_indices, num_NCO, marker='s', linestyle='-', label='NCO Count')

# Plot num_PTMG1000 if not all zero
if not np.all(num_PTMG1000 == 0):
    plt.plot(file_indices, num_PTMG1000, marker='^', linestyle='-', label='PTMG1000-OH Count')

# Plot num_PTMG2000 if not all zero
if not np.all(num_PTMG2000 == 0):
    plt.plot(file_indices, num_PTMG2000, marker='v', linestyle='-', label='PTMG2000-OH Count')

# Plot num_BDO if not all zero
if not np.all(num_BDO == 0):
    plt.plot(file_indices, num_BDO, marker='*', linestyle='-', label='BDO-OH Count')

plt.xlabel('timesteps (x $10^6$)')
plt.ylabel('Count')
plt.title('Variation of Variables with timesteps')
# plt.text(0.5, -0.15, text, transform=plt.gca().transAxes, ha='center')
plt.grid(True)
plt.legend()  
plt.savefig(image_path)  




# num_urethane_list.append(numC1)
# print(num_urethane_list)
# # 将列表转换为 NumPy 数组（可选）
# types_array = np.array(types)
# # print(types_array)
# filename = 'types.txt'
# #保存数据格式为字符串
# np.savetxt(filename, types_array, fmt='%s')

# filename = 'num_urethane.txt'
# #保存数据格式为字符串
# np.savetxt(filename,num_urethane)
        

# 打印每种粒子类型的个数统计结果
# for particle_type, count in particle_count.items():
#     print(f"Particle type {particle_type}: {count}")





# # 查找 position 元素并解析坐标数据
# positions = []
# position_elem = root.find('.//position')
# if position_elem is not None:
#     lines = position_elem.text.strip().split('\n')
#     for line in lines:
#         coords = line.strip().split()
#         x = float(coords[0])
#         y = float(coords[1])
#         z = float(coords[2])
#         positions.append([x, y, z])

# # 将列表转换为 NumPy 数组
# positions = np.array(positions)

# filename="position.txt"
# with open(filename,'a+') as f1:
#     np.savetxt(f1,positions)
# current_dir = os.getcwd()
# print("当前工作目录：", current_dir)
# exit()
