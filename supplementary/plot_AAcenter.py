import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import pandas as pd
from itertools import chain

# 读取数据
data = pd.read_csv('AA.txt', header=None, sep='\s+')
data = list(chain.from_iterable(data.itertuples(index=False, name=None)))
# 计算中位数
#median = np.median(data)
# 绘制密度图
plt.figure(figsize=(10, 6), dpi=300)  # 更高的分辨率
density = plt.hist(data, bins=500, density=True, alpha=0.7, color='#8dd3c7', label='Histogram')

# 添加核密度估计曲线
kernel_density = gaussian_kde(data)
xgrid = np.linspace(min(data), max(data), 1000)
plt.plot(xgrid, kernel_density(xgrid), color='#fb8072', linewidth=2, label='Kernel density estimation')

# 设置标题和轴标签
plt.title('Amino Acid Density Map', fontsize=18, fontweight='bold')
plt.xlabel('Number of Amino Acids', fontsize=16, fontweight='bold')
plt.ylabel('Density', fontsize=16, fontweight='bold')
# 标记中位数
#plt.axvline(median, color='blue', linestyle='--', linewidth=2, label='中位数')
#plt.text(median, 0.05, f'Median: {median:.2f}', horizontalalignment='center', color='blue', fontsize=14, fontweight='bold')
# 设置轴的极限和刻度
plt.xlim([0, 10000])
plt.xticks(fontsize=14, fontweight='bold')
plt.yticks(fontsize=14, fontweight='bold')

# 添加图例
plt.legend(prop={'size': 14, 'weight': 'bold'})

# 设置网格线
plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)

# 保存为JPG文件
plt.savefig('AA_center.jpg', bbox_inches='tight', dpi=300)

# 显示图像
plt.show()

