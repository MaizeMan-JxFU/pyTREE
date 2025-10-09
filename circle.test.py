import numpy as np
import matplotlib.pyplot as plt

# 定义极径和角度
r = np.arange(1, 6, 1)
theta = [i * np.pi / 2 for i in range(5)]

# 创建极坐标子图
ax = plt.subplot(111, projection='polar')
ax.scatter(theta, r, linewidth=3, color='red')
ax.grid(True) # 显示网格
plt.savefig('test.png')