import glob
from tqdm import tqdm
def count_atoms(filepath):
    with open(filepath) as file:
        lines = file.readlines()
    
    atom_count = 0
    for line in lines:
        if line.startswith("ATOM"):
            atom_count += 1
    
    return atom_count


from Bio import SeqIO
import os
folder_path = "../pdb/"
total_items = 0
for _ in os.listdir(folder_path):
    total_items += 1  # 对于每个目录计数 
# 指定要遍历的文件夹路径
print(total_items)
AA = [] 
ATOM = []
with tqdm(total=total_items, desc='Walking through directory', unit='file') as pbar:
 for root, dirs, files in os.walk(folder_path):
    for file in files:
#        print(file)
        if file.endswith(".pdb"):
            # 打开并处理每个PDB文件
            pdb_file_path = os.path.join(root, file)
            with open(pdb_file_path) as file:
                records = list(SeqIO.parse(file, "pdb-seqres"))

            total_amino_acids = sum([len(record.seq) for record in records])
            AA.append(total_amino_acids)
            atoms = count_atoms(pdb_file_path)
            ATOM.append(atoms)
        pbar.update(1)
#print(AA)
#print(ATOM)


import os

# 判断文件是否存在
if os.path.exists('ATOM.txt'):
    # 若存在则删除文件
    os.remove('ATOM.txt')
 
# 判断文件是否存在
if os.path.exists('AA.txt'):
    # 若存在则删除文件
    os.remove('AA.txt')

with open('ATOM.txt', 'w') as file:
    # 遍历列表中的每个元素
    for item in ATOM:
        # 将当前元素作为字符串写入到文件中，并换行
        file.write(str(item) + '\n')

with open('AA.txt', 'w') as file:
    # 遍历列表中的每个元素
    for item in AA:
        # 将当前元素作为字符串写入到文件中，并换行
        file.write(str(item) + '\n')




import statistics

# 计算最大值
maxAA = max(AA)
maxATOM = max(ATOM)

minAA = min(AA)
minATOM = min(ATOM)

averageAA = sum(AA) / len(AA)
averageATOM = sum(ATOM) / len(ATOM)

varianceAA = statistics.variance(AA)
varianceATOM= statistics.variance(ATOM)
print("--------------AA------------------")
print("The max number of AA: ", maxAA)
print("The min number of AA: ", minAA)
print("The average number of AA: ","{:.2f}".format(averageAA))
print("The variance of AA: ", "{:.2f}".format(varianceAA))
print("--------------ATOM----------------")
print("The max number of ATOM: ", maxATOM)
print("The min number of ATOM: ", minATOM)
print("The average number of ATOM: ", "{:.2f}".format(averageATOM))
print("The variance of ATOM: ", "{:.2f}".format(varianceATOM))



