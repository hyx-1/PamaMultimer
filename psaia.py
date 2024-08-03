import argparse
import pandas as pd 
import os
import numpy as np
import time

parser = argparse.ArgumentParser()
parser.add_argument('--pdbname','-n',type=str, required=True, help='pdb file name')
parser.add_argument('--top_num','-t',type=int, default=3, help='number of top patches you want')
args = parser.parse_args()

pdbname = args.pdbname
top_num = args.top_num
#pdbname = '1acb'
#top_num = 2
chain_name = pd.read_csv('./chain/chain_' + pdbname + '.txt', header=None)
if os.path.exists('./rsa/' + pdbname + '_RES.txt'):
        os.remove('./rsa/' + pdbname + '_RES.txt')
# 打开原始文件
with open('./rsa/' + pdbname + '.rsa', "r") as file:
    # 逐行读取原始文件内容
    for line in file:
        if line.startswith("RES"):
            # 如果当前行以"RES"开头，则将该行添加到新文件中
            with open('./rsa/' + pdbname + '_RES.txt', "a") as new_file:
                new_file.write(line)
rsa_name = './rsa/' + pdbname + '_RES.txt'

# 列的起始和结束位置（根据实际情况调整）
rsa_positions = [(0,3),(3,8),(8,9),(9,14),(15,22),(22,28)]  # 例如，从第0列到第5列是字符型，从第10列到第15列和第20列到第25列是数值型

# 初始化空矩阵
rsa_matrix = None

# 打开文件
with open(rsa_name, 'r') as file:
    # 遍历文件的每一行
    for line in file:
        # 初始化当前行的数据列表
        rsa_data = []
        
        # 遍历列的起始和结束位置
        for start, end in rsa_positions:
            # 提取每个列的数据，并添加到当前行的数据列表
            rsa_value = line[start:end].strip()
            rsa_data.append(rsa_value)
        # 提取字符型列和数值型列
        char_columns = rsa_data[0:4]
        numeric_columns = [float(data) for data in rsa_data[4:6]]  # 从第1列开始是数值型，转换为浮点数
        
        # 将字符型列和数值型列合并
        row_data = char_columns + numeric_columns

        # 将每行数据添加到数据矩阵
        if rsa_matrix is None:
            rsa_matrix = np.array([row_data])
        else:
            rsa_matrix = np.append(rsa_matrix, [row_data], axis=0)

# 将data_matrix转换为DataFrame
# columns = [0, 1, 2, 3, 4, 5, 6, 7, 8]
# df = pd.DataFrame(data_matrix, columns=columns)
rsa_total = pd.DataFrame(rsa_matrix)
rsa_total[4] = rsa_total[4].astype(float)
rsa_total[5] = rsa_total[5].astype(float)
# 寻找界面残基
# 寻找界面残基
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
    pairs = kdtree_A.query_ball_tree(kdtree_B, r=5.0)  # 使用适当的距离阈值

    # 将接近的残基对添加到界面列表中
    for res1, res2_list in enumerate(pairs):
        for res2 in res2_list:
            interface_A.add(A.iloc[res1, 5])
            interface_B.add(B.iloc[res2, 5])

    return list(interface_A), list(interface_B)
# 使用多线程版本的函数
pdb = pd.read_csv('./modify/' + pdbname + '.pdb',header=None,sep='\t')
pdb_by_chain = {}
interface_res = {}
for i in range(len(chain_name[0])):
    pdb_by_chain[chain_name[0][i]] = pdb[pdb[4]==chain_name[0][i]]
    interface_res[chain_name[0][i]] = []
find_start = time.time()
for j in range(len(chain_name[0])):
    for k in range(len(chain_name[0])):
        if k>j:
           # interface1, interface2 = find_interface_parallel(pdb_by_chain[chain_name[0][j]], pdb_by_chain[chain_name[0][k]])
            interface1, interface2 = find_interface(pdb_by_chain[chain_name[0][j]], pdb_by_chain[chain_name[0][k]])
            interface_res[chain_name[0][j]][1:1]=interface1
            interface_res[chain_name[0][k]][1:1]=interface2
find_end = time.time()
print(find_end - find_start)
print(interface_res)
for i in range(len(chain_name[0])):
    interface_res[chain_name[0][i]] = list(set(interface_res[chain_name[0][i]]))
print('Find interface is done.')

# 寻找表面模块并计算每个模块的PSAIA
surface_patch = {}
patch_order = {}
for chain_num in range(len(chain_name[0])):
    chain = chain_name[0][chain_num]
    rsa = rsa_total[rsa_total[2] == chain]
    contact = pd.read_csv('./contact/' + pdbname + '_' + chain + '-by-res.vor', header=None, sep='\s+')
    #print(contact[1].astype(str)=='156')
    patch_cen = contact[5].unique() 
    patch = {}
    sur_patch = {}
    patch_A = {}
    patch_C = {}
    patch_PSAIA = {}
    for i in range(len(patch_cen)):
        patch[patch_cen[i]] = contact[contact[5].isin([patch_cen[i]])]  
        patch_mem = patch[patch_cen[i]][1].values
        patch_mem = patch_mem.astype(str)
        if len(set(patch_mem) & set(rsa[rsa[5]>=15][3])): 
            sur_patch[patch_cen[i]] = patch[patch_cen[i]]  
            patch_A[patch_cen[i]] = 0
            for j in range(len(patch_mem)):
                #print(rsa[rsa[3] == patch_mem[j]][4].values)
                #print(patch_mem[j])
                #print(rsa[3]==patch_mem[j])
                patch_A[patch_cen[i]] += rsa[rsa[3] == patch_mem[j]][4].values  
            #print(patch_A[patch_cen[i]])
            patch_C[patch_cen[i]] = 0
            for k in range(len(list(patch_mem))):
                for l in range(len(list(patch_mem))):
                    if (k != l) & (len(contact[(contact[1].astype(str) == patch_mem[k]) & (contact[5].astype(str) == patch_mem[l])])):
                        #print(contact[(contact[1].astype(str) == patch_mem[k]) & (contact[5].astype(str) == patch_mem[l])][8].values)
                        #print(patch_mem[k],patch_mem[l])
                        patch_C[patch_cen[i]] += contact[(contact[1].astype(str) == patch_mem[k]) & (contact[5].astype(str) == patch_mem[l])][8].values[0]
            patch_C[patch_cen[i]] = patch_C[patch_cen[i]]/2
            patch_PSAIA[patch_cen[i]] = patch_A[patch_cen[i]] * patch_C[patch_cen[i]]**8 
    patch_order[chain] = sorted(patch_PSAIA.items(),key=lambda x:x[1],reverse=True) 
    surface_patch[chain] = sur_patch
    top_patch={}
    surpatch_order={}
    #print(patch_order[chain])
    for num in range(top_num):
        top_patch['patch' + str(num+1)] = contact[contact[5] == patch_order[chain][num][0]].iloc[:, 1:4]
    
    for num in range(len(patch_order[chain])):
        surpatch_order['patch' + str(num+1)] = contact[contact[5] == patch_order[chain][num][0]].iloc[:, 1:4]

    if os.path.exists('./result/surpatch_order/' + pdbname + '_' + chain +'.txt'):
        os.remove('./result/surpatch_order/' + pdbname + '_' + chain +'.txt')
    file = open('./result/surpatch_order/' + pdbname + '_' + chain +'.txt', 'w') 
    for key, value in surpatch_order.items():
        file.write('\n' + key)
        file.write(str(value))
    file.close()

    if os.path.exists('./result/top_patch/' + pdbname + '_' + chain +'.txt'):
        os.remove('./result/top_patch/' + pdbname + '_' + chain +'.txt')
    file = open('./result/top_patch/' + pdbname + '_' + chain +'.txt', 'w') 
    for key, value in top_patch.items():
        file.write('\n' + key)
        file.write(str(value))
    file.close()
    print('Chain '+str(chain)+' is done.(Find surface)')

#寻找界面模块
interface_patch = {}
inter_patch_order = {}
for chain_num in range(len(chain_name[0])):
    chain = chain_name[0][chain_num]
    contact = pd.read_csv('./contact/' + pdbname + '_' + chain + '-by-res.vor', header=None, sep='\s+')
    interface_patch[chain] = {}
    for key,value in surface_patch[chain].items():
        if len(set(value[1]) & set(interface_res[chain])):
            interface_patch[chain][key] = value

    index_rank = []
 
    # 提取patch的次序信息
    for sublist in patch_order[chain]:
        index_rank.append(sublist[0])
    # 提取界面patch的次序信息
    interface_order_rank = {}
    for index in range(len(interface_patch[chain])):
        interface_order_rank[list(interface_patch[chain].keys())[index]] = index_rank.index(list(interface_patch[chain].keys())[index])
    #给界面残基排序
    inter_patch_order[chain] = sorted(interface_patch[chain].items(), key=lambda x:interface_order_rank[x[0]])
    interpatch_order = {}
    for num in range(len(inter_patch_order[chain])):
        interpatch_order['patch' + str(num+1)] = contact[contact[5] == inter_patch_order[chain][num][0]].iloc[:, 1:4]

    if os.path.exists('./result/interpatch_order/' + pdbname + '_' + chain +'.txt'):
        os.remove('./result/interpatch_order/' + pdbname + '_' + chain +'.txt')
    file = open('./result/interpatch_order/' + pdbname + '_' + chain +'.txt', 'w') 
    for key, value in interpatch_order.items():
        file.write('\n' + key)
        file.write(str(value))
    file.close()
    print('Chain '+str(chain)+' is done.(Find interface)')
# 得到表面模块数，界面模块数，psaia值最高界面模块在表面模块中的排名
TRIP = {}
IPN = {}
SPN = {}
interface_rank = {}
interface_order = {}
for chain_num in range(len(chain_name[0])):
    chain = chain_name[0][chain_num]

    IPN[chain] = len(interface_patch[chain])
 
    SPN[chain] = len(surface_patch[chain])

    interface_rank[chain] = {}
    interface_order[chain] = {}
    TRIP[chain] = {}
    for key,value in interface_patch[chain].items():
        for i in range(len(patch_order[chain])):
            if patch_order[chain][i][0] == key:
                interface_rank[chain][key] = i+1
    interface_rank[chain]
    interface_order[chain] = sorted(interface_rank[chain].items(),key=lambda x:x[1],reverse=False)
    TRIP[chain] = interface_order[chain][0][1]

# 保存结果
if os.path.exists('./result/repo_result/result_' + pdbname + '.txt'):
    os.remove('./result/repo_result/result_' + pdbname + '.txt')
file = open('./result/repo_result/result_' + pdbname + '.txt', 'w')
file.write('\t' + 'TRIP' + '\t' + 'IPN' + '\t' + 'SPN' + '\n') 
for chain_num in range(len(chain_name[0])):
    chain = chain_name[0][chain_num] 
    file.write(chain + '\t')
    file.write(str(TRIP[chain]) + '\t' + str(IPN[chain]) + '\t' + str(SPN[chain]) + '\n')
file.close()
