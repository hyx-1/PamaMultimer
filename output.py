import os
import pandas as pd
if os.path.exists('output.txt'):
    os.remove('output.txt')
# 指定要遍历的文件夹路径
folder_path = "./result/repo_result/"
 
with open('./output.txt', "a") as new_file:
    new_file.write('\t' + 'TRIP' + '\t' + 'IPN' + '\t' + 'SPN' + '\n')
    for root, dirs, files in os.walk(folder_path):
        for file in files:
        # 获取文件名（包括后缀）
            filename = os.path.splitext(file)[0]
            #print(filename)
            pdb = file[7:11]
            # 打开原始文件
            with open('./result/repo_result/' + filename + '.txt', "r") as result_file:
                result_file.readline()
                # 逐行读取原始文件内容
                for line in result_file:
                    new_file.write(pdb+ '_'+line)

file_count = 0
top_exist = 0
top_all = 0
chain_list = {}
for root1, dirs1, files1 in os.walk(folder_path):
    for file in files1:
        file_count += 1
        result = pd.read_csv('./result/repo_result/'+file,header=None,sep='\t')
        result = result.drop(index=0)
        #print(result)
        chain_num = len(result[1])
        #print(chain_num)
        if chain_num in chain_list:
            chain_list[chain_num] += 1
        else:
            chain_list[chain_num]=1
        if all(result[1].astype(int)<4):
            top_all += 1
        if any(result[1].astype(int)<4):
            top_exist += 1
result_total = pd.read_csv('output.txt',index_col=0,sep='\t')
TRIP = result_total.loc[:,"TRIP"]
IPN = result_total.loc[:,"IPN"]
SPN = result_total.loc[:,"SPN"]
#print(TRIP)
#print(IPN)
#print(SPN)
#print(result_total)
#获取统计信息
interface_max = IPN.max()
interface_min = IPN.min()
surface_max = SPN.max()
surface_min = SPN.min()

#Protein monomer information
count_less_equal_to_5 = TRIP[TRIP <= 5].size
total_length = len(TRIP)
percentage_5 = count_less_equal_to_5 / total_length

count_less_equal_to_1 = TRIP[TRIP <= 1].size
percentage_1 = count_less_equal_to_1 / total_length

count_less_equal_to_4 = TRIP[TRIP <= 4].size
percentage_4 = count_less_equal_to_4 / total_length

count_less_equal_to_3 = TRIP[TRIP <= 3].size
percentage_3 = count_less_equal_to_3 / total_length

count_less_equal_to_2 = TRIP[TRIP <= 2].size
percentage_2 = count_less_equal_to_2 / total_length

#print("小于等于5的数量为：", count_less_equal_to_5)
#print("百分比为：", percentage_5)


print('The number of proteins is '+str(file_count))
print('In at least one chain, the interface patches are in the top3: {:.2%}'.format(top_exist/file_count))
print('In all chains, the interface patches are in the top3: {:.2%}'.format(top_all/file_count))
#print(chain_list)
chain_list_order = sorted(chain_list.items(),key = lambda item:item[0])
#print(chain_list_order)
for element in chain_list_order:
    print('The number of '+str(element[0])+'-chain proteins is '+str(element[1]))
print('The interface patch number is '+ str(interface_min) + '-' + str(interface_max))
print('The surface patch number is '+ str(surface_min) + '-' + str(surface_max))
print('The number of monomers: '+str(total_length))
print('For all monomers, the interface patches are in the top5: '+str(count_less_equal_to_5)+'({:.2%}'.format(percentage_5)+')')
print('For all monomers, the interface patches are in the top4: '+str(count_less_equal_to_4)+'({:.2%}'.format(percentage_4)+')')
print('For all monomers, the interface patches are in the top3: '+str(count_less_equal_to_3)+'({:.2%}'.format(percentage_3)+')')
print('For all monomers, the interface patches are in the top2: '+str(count_less_equal_to_2)+'({:.2%}'.format(percentage_2)+')')
print('For all monomers, the interface patches are in the top1: '+str(count_less_equal_to_1)+'({:.2%}'.format(percentage_1)+')')
