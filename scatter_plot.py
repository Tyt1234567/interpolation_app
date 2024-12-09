import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

def plot_raw_data(longitudes, latitudes, elevations):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    sc = ax.scatter(longitudes, latitudes, elevations, c=elevations, cmap='viridis', s=50, alpha=0.7, edgecolors='w')

    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Elevation')

    # 禁用科学计数法
    ax.xaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    ax.zaxis.set_major_formatter(ScalarFormatter(useOffset=False))

    # 添加颜色条
    cbar = plt.colorbar(sc)
    cbar.set_label('Elevation')

    # 设置图标题
    ax.set_title('river_elevation_model')
    plt.title('raw_data_scatter')
    plt.show()
