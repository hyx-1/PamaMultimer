import pandas as pd
import json
import os 
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')
# 设置目标文件夹路径
folder_path = './result/top_patch' 
# 遍历文件夹
with tqdm(total=len(os.listdir(folder_path)), desc='Walking through directory', unit='file') as pbar:
  for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
      try:  
        # 完整的文件路径
        file_path = os.path.join(folder_path, filename)
        
        data = pd.read_csv(file_path,header=None,sep='\s+')
        #print(data.iloc[:,1])
        data = data[data.iloc[:,6].str.len() == 3]
 
        #print(data)
        # 根据第五列进行分组
        grouped_data = data.groupby(data.columns[5])
        #print(grouped_data)
        group_dist = {}
        group_surnum = {}
        for name, group in grouped_data:
            #print(f'Group for Column5 value {name}:')
            #print(group)
            group_dist[name] = group
            s=group[2]
            # 使用str.count()方法统计包含'#'的元素数量
            number_of_sharp = s.str.count('#').sum()
            group_surnum[name] = number_of_sharp
        #print(group_surnum)
        group_dist = dict(sorted(group_dist.items(), key=lambda x: group_surnum[x[0]], reverse = True))
        #print(group_dist)
        with open('rank_res.json', 'r') as f:
            rank_res = json.load(f)
        #print(rank_res)

        rank_num = {} 
        count = 0
        for res,score in rank_res.items():
            count = count + 1
            rank_num[res] = count
        #print(rank_num)
        for key,value in group_dist.items():
            value['rank'] = None
            for index, row in value.iterrows():
                value['rank'][index] = rank_num[row[2][0:3]]
            group_dist[key] = value.sort_values(by='rank')
            #print(value)
        #print(group_dist)
        top_num = 5
        select_res = []
        for key,value in group_dist.items():
            for index,row in value.iterrows():
                select_res.append(row[1])
        #print(select_res)
        def count_special_elements(lst, special_element):
            # 使用列表推导式找出前十个元素中特定元素的数量
            count = sum([1 for elem in lst[:top_num] if special_element in elem])
            return count
        acc = count_special_elements(select_res,'*')/top_num
        #print(acc)
        if os.path.exists('./result/acc_result/' + filename):
           os.remove('./result/acc_result/' + filename)
        file = open('./result/acc_result/' + filename, 'w')
        file.write(filename[0:6] + '\t')
        file.write(str(acc*100))
        file.close()
      except Exception as e:
        # 处理其他所有异常
        print(f"Error:{e}")
        #pass
    pbar.update(1)
