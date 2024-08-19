import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
data = pd.read_csv('len.txt',header=None,sep='\s+')
#print(data)
data1 = data[0].values.tolist()
data2 = data[1].values.tolist()
# 绘制两组数据的密度图
plt.figure(figsize=(8, 6), dpi=300)  # 更高的分辨率

# 数据1的密度图
density1 = plt.hist(data1, bins=30, density=True, alpha=0.7, color='#8dd3c7', label='Density map for patch length')

# 数据2的密度图
density2 = plt.hist(data2, bins=30, density=True, alpha=0.7, color='#fb8072', label='Density map for chain length')

# 添加核密度估计曲线
kde1 = gaussian_kde(data1)
xgrid1 = np.linspace(min(data1), max(data1), 1000)
plt.plot(xgrid1, kde1(xgrid1), color='#8dd3c7', linewidth=2, linestyle='--', label='Kernel density estimation for patch length')

kde2 = gaussian_kde(data2)
xgrid2 = np.linspace(min(data2), max(data2), 1000)
plt.plot(xgrid2, kde2(xgrid2), color='#fb8072', linewidth=2, linestyle='--', label='Kernel density estimation for chain length')

# 设置标题和轴标签
plt.title('Density map for patch length and chain length', fontsize=16, fontweight='bold')
plt.xlabel('Length', fontsize=14, fontweight='bold')
plt.ylabel('Density', fontsize=14, fontweight='bold')

# 设置轴的刻度和标签
plt.xlim([0, max(data2) + 0.1 * (max(data2) - min(data2))])
plt.xticks(fontsize=14, fontweight='bold')
plt.yticks(fontsize=14, fontweight='bold')

# 添加图例
plt.legend(prop={'size': 14, 'weight': 'bold'})

# 添加网格线
plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)

# 保存为JPG文件
plt.savefig('Patch_and_chain_length.jpg', bbox_inches='tight', dpi=300)

# 显示图像
plt.show()
