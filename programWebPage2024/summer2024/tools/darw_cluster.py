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




base_path = './'
# 创建一个文件名数组
file_names = []
for i in range(1000000,201000001, 1000000):  # 从 0 到 20100000
    filename = f"particles.{i:010d}.xml"  # 格式化文件名，使数字部分有 10 位，前面补零
    filepath = os.path.join(base_path, filename)  # 构建完整路径
    if os.path.isfile(filepath):  # 检查文件是否存在
        file_names.append(filename)  # 如果文件存在，则添加到文件名数组
# print("所有文件名：", file_names)

frame = file_names[-1]
# print("选择的文件名：", frame )

tree = ET.parse(frame)
root = tree.getroot()

# positions = frame.particles.position
# types = frame.particles.typeid
# box = frame.configuration.box
# type_id=np.unique(types)

positions = []
position_elem = root.find('.//position')
if position_elem is not None:
    lines = position_elem.text.strip().split('\n')
    for line in lines:
        coords = line.strip().split()
        x = float(coords[0])
        y = float(coords[1])
        z = float(coords[2])
        positions.append([x, y, z])
positions = np.array(positions)

particles= []
particle_elem = root.find('.//type')
if particle_elem is not None:
    # 遍历 <type> 元素的所有文本节点，分割字符串并去除前后的空白字符
    for elem in particle_elem.text.split():
        clean_elem = elem.strip()
        particles.append(clean_elem)
particles = np.array(particles)

box_element = root.find('.//box')
lx = float(box_element.get('lx'))
ly = float(box_element.get('ly'))
lz = float(box_element.get('lz'))
box = np.array([lx, ly, lz, 0.0, 0.0, 0.0])

type=np.unique(particles)

bonds=[]
bond_elem = root.find('.//bond')
for bond in bond_elem.text.splitlines():
    if bond.strip():  # 确保不是空行
        parts = bond.split()
        if len(parts) == 3:
            bonds.append([int(parts[1]), int(parts[2])])
bonds = np.array(bonds, dtype=np.int32)
# print(bonds)
# exit()

# 构建邻接表
adj_list = defaultdict(list)
for bond in bonds:
    adj_list[bond[0]].append(bond[1])
    adj_list[bond[1]].append(bond[0])

# 寻找clusters
def find_clusters(adj_list):
    visited = set()
    clusters = []

    def bfs(start_node):
        cluster = []
        queue = deque([start_node])
        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                cluster.append(node)
                for neighbor in adj_list[node]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        return cluster

    for node in adj_list:
        if node not in visited:
            cluster = bfs(node)
            if cluster:
                clusters.append(cluster)

    return clusters

# 获取所有clusters
clusters = find_clusters(adj_list)

print(clusters[0])
exit()

# 统计clusters大小和数量
cluster_sizes = [len(cluster) for cluster in clusters]
size_count = Counter(cluster_sizes)

# print("cluster_sizes",cluster_sizes)
# print("size_count",size_count)
# exit()
# 分离横坐标（大小）和纵坐标（数目）
x = list(size_count.keys())
y = list(size_count.values())

x = np.array(x)
y = np.array(y)

# 设置条形宽度和间距
bar_width = 0.05  # 调整条形宽度
spacing = 0.8  # 条形之间的间距比例

# 将x轴值转换为对数刻度的位置
log_x = np.log10(x)

# 计算条形的实际位置
bar_positions = log_x - bar_width / 2

# 绘制条形图
plt.figure(figsize=(10, 6))  # 设置图表大小
plt.bar(bar_positions, y, color='skyblue', width=bar_width)

# 设置x轴为对数刻度
plt.yscale('log')

# 设置x轴的取值范围
x_min, x_max = 0.1, 3000
plt.xlim(np.log10(x_min) - bar_width, np.log10(x_max) + bar_width)

# 设置x轴的刻度和标签
log_ticks = np.arange(np.log10(x_min), np.log10(x_max) + 1)
plt.xticks(log_ticks, [f'$10^{int(t)}$' for t in log_ticks])

# 设置纵坐标范围
plt.ylim(0.5, 200)

# 添加网格线，设置透明度
plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
# 添加标题和标签
plt.title('Cluster Size vs. Number of Clusters')
plt.xlabel('Cluster Size')
plt.ylabel('Number of Clusters')

plt.savefig('rcluster.png', dpi=300)

# 将数据保存到文本文件中
# 将数据转换为numpy数组，并垂直堆叠为两列
data = np.vstack((x, y)).T
filename = "cluster distribution.txt"
header = "Cluster Size\tNumber of Clusters"
np.savetxt(filename, data, fmt='%.6f', header=header, comments='', delimiter='\t')
exit()





# # Initialize lists to store RDF results for each unique pair of particle types
# rdfs = { (i, j): [] for i, j in combinations_with_replacement(type, 2) }
# #字典里的这里列表可以储存多帧的RDF值，因此后面rdfs[(i, j)][0]是读取第一帧
# # exit()
# # Compute RDF for different particle types
# for i, j in combinations_with_replacement(type, 2):
#     positions_i = positions[particles == i]
#     positions_j = positions[particles == j]
#     # print(i, j)

#     # Compute RDF for type i and type j
#     rdf = freud.density.RDF(bins=200, r_max=5.0)
#     rdf.compute(system=(box, positions_i), query_points=positions_j, reset=False)
#     rdfs[(i, j)].append(rdf.rdf.copy())
#     # print(rdfs[(i, j)])
#     # exit()
#     # i==j, when r is small, g(r) will very big (particle will overlap itself)
#     if i==j:
#         rdfs[(i, j)][0][0]=0
    


# r = rdf.bin_centers

# # 计算需要的子图行数和列数
# num_plots = len(rdfs)
# num_cols = 4
# num_rows = (num_plots + num_cols - 1) // num_cols  # 向上取整计算行数

# fig, axes = plt.subplots(num_rows, num_cols, figsize=(20, num_rows * 4),dpi=300)

# # 确保 axes 是二维数组
# if num_rows == 1:
#     axes = np.expand_dims(axes, axis=0)
# if num_cols == 1:
#     axes = np.expand_dims(axes, axis=1)

# # 遍历所有的 (i, j) 对并生成对应的 RDF 图表
# for ax, ((i, j), rdf_list) in zip(axes.flat, rdfs.items()):
#     mean_rdf = np.mean(rdf_list, axis=0)  # 计算每个对的RDF数据的平均值
#     label = f'RDF ({i}, {j})'  # 设置图例标签
#     ax.plot(r, mean_rdf, label=label)  # 绘制图表
#     ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)  # 添加网格线
#     # 设置图表标题和轴标签
#     ax.set_title(f'Radial Distribution Function for Pair ({i}, {j})')
#     ax.set_xlabel('Distance (r)')
#     ax.set_ylabel('g(r)')
#     ax.legend()  # 显示图例

# # 调整布局，使子图不重叠
# plt.tight_layout()

# # 保存图表
# plt.savefig('rdf_each_pairs_5_200bins.png', dpi=300)


# pair_names = [f"{pair[0]}-{pair[1]}" for pair in combinations_with_replacement(type, 2)]
# # print(pair_names)
# # exit()
# # 构建包含列名的字符串
# header = "center\t" + "\t".join(pair_names)

# filename3="rdf_each_pairs_5_200bins.txt"
# output_data = np.vstack([r] + [rdfs[pair] for pair in combinations_with_replacement(type, 2)])
# np.savetxt(filename3, output_data.T, fmt='%.6f',header=header, comments='')

# exit()
