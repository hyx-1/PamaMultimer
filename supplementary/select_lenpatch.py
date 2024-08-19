import os
import json
import pandas as pd
# 打开JSON文件并读取数据
with open('fail.json', 'r', encoding='utf-8') as file:
    fail = json.load(file)

# 打开JSON文件并读取数据
with open('len_chain_patch.json', 'r', encoding='utf-8') as file:
    len_chain_patch = json.load(file)
# 打开JSON文件并读取数据
with open('len_chain.json', 'r', encoding='utf-8') as file:
    len_chain = json.load(file)
print(len(len_chain_patch))
if os.path.exists('len.txt'):
    # 删除文件
    os.remove('len.txt')
with open('len.txt', 'w', encoding='utf-8') as file:
     for key, value in len_chain_patch.items():
         file.write(str(value) + '\t' + str(len_chain[key]) + '\n')
#data = pd.read_csv('len.txt',header = None,sep='\s+')
#print(data)
data = pd.read_csv('../output.txt',sep='\s+')
print(data)
row_to_select = []
for key, value in len_chain_patch.items():
    if len_chain[key]/value > 10:
       row_to_select.append(key) 
# 选取名字在names_to_select列表中的行
selected_rows = data.loc[row_to_select]
with open('row_to_select.json', 'w', encoding='utf-8') as file:
    json.dump(row_to_select, file, ensure_ascii=False, indent=4)
if os.path.exists('output_select.txt'):
    # 删除文件
    os.remove('output_select.txt')

selected_rows.to_csv('output_select.txt', sep='\t', index=True, header=True) 
print(selected_rows)       
