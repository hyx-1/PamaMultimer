import subprocess
import os
import pandas as pd
import time
import numpy as np
# 指定要遍历的文件夹路径
folder_path = "./pdb"
# 列的起始和结束位置（根据实际情况调整）
column_positions = [(0,4),(6,11),(12,16),(17,20),(21,22),(22,26),(30,38),(38,46),(46,54)]  # 例如，从第0列到第5列是字符型，从第10列到第15列和第20列到第25列是数值型 
main_start=time.time()
for root, dirs, files in os.walk(folder_path):
    # print(files)
    for file in files:
        # 获取文件名（包括后缀）
        filename = os.path.splitext(file)[0]
        print(filename)
        try:
            pdb_filename = filename
            # 初始化空矩阵
            data_matrix = None
            # 只保留pdb中原子信息
            with open(f'./pdb/{pdb_filename}.pdb', 'r') as pdb_file:
                for line in pdb_file:
                    if line.startswith('ATOM'):
                        columns_data = []
                        # 遍历列的起始和结束位置
                        for start, end in column_positions:
                            # 提取每个列的数据，并添加到当前行的数据列表
                            column_value = line[start:end].strip()
                            columns_data.append(column_value)
                        # print(columns_data)
                            # 将每行数据添加到数据
                        if data_matrix is None:
                            data_matrix = np.array([columns_data])
                        else:
                            data_matrix = np.append(data_matrix, [columns_data], axis=0)
            df = pd.DataFrame(data_matrix)
            df.to_csv(f'./modify/{pdb_filename}.pdb', sep='\t', index=False,header=False)
            print(pdb_filename+' modify is done.')
            # 生成链名文件
            subprocess.run(['python', 'chain.py', '-n', f'{pdb_filename}'])
            print(pdb_filename+' chain is done.')
            # 得到模块和模块内残基接触面积
            with open(f'./chain/chain_{pdb_filename}.txt', 'r') as chain_file:
                chains = chain_file.readlines()
                for chain in chains:
                    chain = chain.strip()
                    subprocess.run(['./Qcontacts', '-i', f'./pdb/{pdb_filename}.pdb', '-prefOut', f'./contact/{pdb_filename}_{chain}', '-c1', chain, '-c2', chain])
                    os.chdir('contact')
                    os.remove(f'{pdb_filename}_{chain}-by-atom.vor')
                    os.chdir('..')
            print(pdb_filename+str('Qcontacts is done.'))
            # 得到溶剂可及表面积
            os.chdir('pdb')
            subprocess.run(['naccess', f'{pdb_filename}.pdb'])
            os.system(f"cp {pdb_filename}.rsa ../rsa")
            os.remove(f"{pdb_filename}.rsa")
            os.remove(f"{pdb_filename}.asa")
            os.remove(f"{pdb_filename}.log")
            os.chdir('..')

            # 运行程序复现结果
            subprocess.run(['python', 'psaia.py', '-n', f'{pdb_filename}'])
            print('Finish'+str(pdb_filename) )

        except:
            print('Error with'+str(pdb_filename))
main_end = time.time()
print(main_end - main_start)
