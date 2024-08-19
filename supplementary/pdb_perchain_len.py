import os
from Bio.PDB import PDBParser
from glob import glob
from tqdm import tqdm
import warnings
import json
# 禁用所有警告的打印
warnings.filterwarnings('ignore')
 
# 假设 'folder_path' 是您想要检查的文件夹的路径
folder_path = '../result/repo_result'
 
# 使用列表推导式提取前四个字符
first_four_chars = [filename[7:11] for filename in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, filename))]
 
#print(first_four_chars)
# 定义一个函数来计算单体的长度
def calculate_chain_length(structure):
    chain_length = 0
    for residue in structure.get_residues():
        chain_length += 1
    return chain_length
def count_lines_in_file(file_path):
    with open(file_path, 'r') as file:
        return sum(1 for line in file)

# 获取当前目录下所有PDB文件
pdb_files = glob('../pdb/*.pdb')
len_chain = {}
len_chain_patch = {}
fail = [] 
# 遍历每个PDB文件
with tqdm(total=len(pdb_files), desc='Walking through directory', unit='file') as pbar:
     for pdb_file in pdb_files:
         if pdb_file[7:11] in first_four_chars:  
            parser = PDBParser()
            structure = parser.get_structure('X', pdb_file)
            for chain in structure.get_chains():
              try:  
                chain_length = calculate_chain_length(chain)
                #print(f"{pdb_file}: Chain {chain.get_id()}, Length: {chain_length}")
                len_chain[pdb_file[7:11] + '_' + chain.get_id()] = chain_length
                #print(len_chain) 
                file_path = '../result/surpatch_order/' + pdb_file[7:11] + '_' + chain.get_id() + '.txt'  # 替换为你的文件路径
                line_count = count_lines_in_file(file_path)
                #print(f'The file {file_path} has {line_count} lines.')
                with open('../result/surpatch_order/' + pdb_file[7:11] + '_' + chain.get_id() + '.txt', 'r') as file:
                     lines = file.readlines()

                # 计数以"patch"开头的行
                count = 0
                for line in lines:
                    if line.startswith('patch'):
                       count += 1
                #print(f"以'patch'开头的行数: {count}")
                patch_res = (line_count - count) / count
                #print(patch_res)
                len_chain_patch[pdb_file[7:11] + '_' + chain.get_id()] = patch_res
              except Exception as e:
                fail.append(pdb_file[7:11] + '_' + chain.get_id())      
         pbar.update(1)    
print(len_chain)
print(len_chain_patch)
# 将字典保存为json文件
with open('len_chain.json', 'w') as f:
    json.dump(len_chain, f)
with open('len_chain_patch.json', 'w') as f:
    json.dump(len_chain_patch, f)
# 保存列表到文件
with open("fail.json", "w") as f:
    json.dump(fail, f)
