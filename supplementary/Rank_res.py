import os
from collections import defaultdict
from Bio.PDB import PDBParser
import json
# 定义文件夹路径
folder_path = './pdb'

# 创建一个默认字典来存储每种氨基酸的计数
amino_acid_counts = defaultdict(int)
res_list = ['ALA', 'CYS', 'ASP', 'GLU', 'PHE', 'GLY', 'HIS', 'ILE', 'LYS', 'LEU', 'MET', 'ASN', 'PRO', 'GLN', 'ARG', 'SER', 'THR', 'VAL', 'TRP', 'TYR']

# 创建PDB解析器
parser = PDBParser()

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # 检查文件是否是PDB文件
    if filename.endswith('.pdb'):
        # 构建PDB文件的全路径
        pdb_file_path = os.path.join(folder_path, filename)
        # 解析PDB文件
        structure = parser.get_structure('struct', pdb_file_path)
        # 遍历模型、链和残基
        for model in structure:
            for chain in model:
                for residue in chain:
                    # 获取残基名称
                    residue_name = residue.get_resname()
                    # 只计算标准氨基酸残基
                    if residue_name in res_list:
                        amino_acid_counts[residue_name] += 1

# 打印每种氨基酸的计数
for amino_acid, count in amino_acid_counts.items():
    print(f"{amino_acid}: {count}")


import pandas as pd
import numpy as np
from scipy.spatial import cKDTree

def find_interface(A, B):
    coords_A = A.iloc[:, 6:9].values
    coords_B = B.iloc[:, 6:9].values

    kdtree_A = cKDTree(coords_A)
    kdtree_B = cKDTree(coords_B)

    interface_A = set()
    interface_B = set()

    # 查询接近的残基对
    pairs = kdtree_A.query_ball_tree(kdtree_B, r=8.0)  # 使用适当的距离阈值

    # 将接近的残基对添加到界面列表中
    for res1, res2_list in enumerate(pairs):
        for res2 in res2_list:
            interface_A.add(A.iloc[res1, 5])
            interface_B.add(B.iloc[res2, 5])

    return list(interface_A), list(interface_B)

# 定义文件夹路径
folder_path = './modify'
res_inter = {}
# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # 检查文件是否是PDB文件
    if filename.endswith('.pdb'):
        # 构建PDB文件的全路径
        pdb_file_path = os.path.join(folder_path, filename)
        # 打印PDB文件路径
        print(pdb_file_path)
        chain_name = pd.read_csv('./chain/chain_' + filename[0:4] + '.txt', header=None)
        # 这里可以添加代码来处理PDB文件，例如读取文件内容或解析结构
	# 使用多线程版本的函数
        pdb = pd.read_csv(pdb_file_path,header=None,sep='\t')
        #print(pdb)
        pdb_by_chain = {}
        interface_res = {}
        residue_internum = {}
        for i in range(len(chain_name[0])):
            pdb_by_chain[chain_name[0][i]] = pdb[pdb[4]==chain_name[0][i]]
            interface_res[chain_name[0][i]] = []
        for j in range(len(chain_name[0])):
            for k in range(len(chain_name[0])):
                if k>j:
                   # interface1, interface2 = find_interface_parallel(pdb_by_chain[chain_name[0][j]], pdb_by_chain[chain_name[0][k]])
                    interface1, interface2 = find_interface(pdb_by_chain[chain_name[0][j]], pdb_by_chain[chain_name[0][k]])
                    interface_res[chain_name[0][j]][1:1]=interface1
                    interface_res[chain_name[0][k]][1:1]=interface2
        #print(find_end - find_start)
        #print(interface_res)
        for i in range(len(chain_name[0])):
            temp = pdb_by_chain[chain_name[0][i]]
            for j in range(len(interface_res[chain_name[0][i]])):
                #print(temp[temp.iloc[:,5][0]==str(interface_res[chain_name[0][i]][j])].iloc[:,3][0])
                tempres = temp[temp[5] == interface_res[chain_name[0][i]][j]][3].values[0]
                if tempres in residue_internum:
                   residue_internum[tempres] += 1
                else:
                   residue_internum[tempres] = 1
        print(residue_internum)
        for res,count in residue_internum.items():
            if res in res_inter:
               res_inter[res] += count
            else:
               res_inter[res] = count
print(res_inter)
res_inter_filter = {}
rank_res = {}
for res,count in amino_acid_counts.items():
    count1 = res_inter[res]
    rank_res[res] = count1/count
    res_inter_filter[res] = count1
rank_res = dict(sorted(rank_res.items(), key=lambda x:x[1], reverse=True))
res_inter_filter = dict(sorted(res_inter_filter.items(), key=lambda x:x[1], reverse=True))
print(rank_res)
print(res_inter_filter)
with open('rank_res.json', 'w') as f:
    json.dump(rank_res, f)
with open('res_inter_filter.json', 'w') as g:
    json.dump(res_inter_filter, g)
