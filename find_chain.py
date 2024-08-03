import os
import shutil
from Bio import PDB
import pandas as pd 
import argparse
import subprocess
parser = argparse.ArgumentParser(description='Select PDB Number')
parser.add_argument("--number", type=int, default="2")
args = parser.parse_args()

def count_chains(filepath):
    parser = PDB.PDBParser()
    structure = parser.get_structure("", filepath)
    
    chain_counts = 0
    for model in structure:
        for chain in model:
            chain_counts += 1 
    return chain_counts
directory='./pdb/'
folder_path = './result/repo_result/'
subprocess.run(['mkdir','pdb_' + str(args.number)])
for root1, dirs1, files1 in os.walk(folder_path):
    for file in files1:
        pdb_file = './pdb/'+file[7:11]+'.pdb'
        result = pd.read_csv('./result/repo_result/'+file,header=None,sep='\t')
        result = result.drop(index=0)
        chain_num = len(result)
        if chain_num == args.number:
             try:
            # 复制文件到当前文件夹
                shutil.copy2(pdb_file, "pdb_" + str(args.number) + "/")
                print("success",pdb_file)
             except Exception as e:
                print('fail')
        
