import argparse
import pandas as pd
parser = argparse.ArgumentParser()
parser.add_argument('--pdbname','-n',type=str, required=True, help='pdb file name')
args = parser.parse_args()

pdbname = args.pdbname
#pdbname = '1acb'
pdb = pd.read_csv('./modify/' + pdbname + '.pdb', sep='\s+', header=None)
chain = pdb[4].unique()
file = open('./chain/chain_' + pdbname + '.txt','w')
for i in range(len(chain)):
    file.write(str(chain[i]) + '\n')
file.close()
