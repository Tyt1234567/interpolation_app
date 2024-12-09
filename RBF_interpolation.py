import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RBFInterpolator
from matplotlib.ticker import ScalarFormatter
import pandas as pd
from scipy.spatial.distance import cdist
from scipy.linalg import lstsq


def exponential_kernel(r, epsilon):
    """Exponential kernel function"""
    return np.exp(-r / epsilon)


def RBF_interpolation(latitudes, longitudes, elevations, epsilon_value=100):
    # 定义插值点
    x_num, y_num = 100, 100
    x2 = np.linspace(min(latitudes), max(latitudes), x_num)
    y2 = np.linspace(min(longitudes), max(longitudes), y_num)
    X, Y = np.meshgrid(x2, y2)
    interp_points = np.column_stack((X.ravel(), Y.ravel()))

    # 定义训练点（latitudes, longitudes）
    data_points = np.column_stack((latitudes, longitudes))

    # 计算距离矩阵
    dist_matrix = cdist(data_points, data_points, 'euclidean')
    kernel_matrix = exponential_kernel(dist_matrix, epsilon_value)

    # 计算插值的权重
    A = kernel_matrix
    b = elevations
    weights, _, _, _ = lstsq(A, b)  # 解线性方程

    # 插值到新点
    dist_interp = cdist(data_points, interp_points, 'euclidean')
    kernel_interp = exponential_kernel(dist_interp, epsilon_value)
    heights = kernel_interp.T.dot(weights)

    heights_grid = heights.reshape(x_num, y_num)

    # 可视化插值结果
    fig = plt.figure(figsize=(10, 8))

    # 3D 表面图
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, heights_grid, cmap='viridis', alpha=0.8)

    # 原始数据点
    ax.scatter(latitudes, longitudes, elevations, c=elevations, cmap='viridis', edgecolor='k', s=1)

    # 设置标签
    ax.set_xlabel('Latitudes')
    ax.set_ylabel('Longitudes')
    ax.set_zlabel('Elevations')

    # 禁用科学计数法
    ax.xaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    ax.zaxis.set_major_formatter(ScalarFormatter(useOffset=False))

    # 设置标题
    ax.set_title(f'interpolation result')

    # 添加颜色条
    fig.colorbar(surf, shrink=0.5, aspect=10)

    # 显示图形
    plt.show()

def read_data(file):

    df = pd.read_csv(file,encoding='ISO-8859-1')
    data_lst = df.values.tolist()
    longitudes = []
    latitudes = []
    elevations = []
    sonar = []
    for data in data_lst:
        latitudes.append(data[1])
        longitudes.append(data[2])
        elevations.append(data[3])
        sonar.append(data[4])
    return latitudes, longitudes, elevations

if __name__ == "__main__":
    latitudes, longitudes, elevations = read_data(r'D:\pyprojects\interpolation\2023-05-15 16-00-48.csv')
    RBF_interpolation(latitudes, longitudes, elevations)




