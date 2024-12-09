import tkinter as tk
from tkintermapview import TkinterMapView

class ShowlocUI:
    def __init__(self,root,points):
        self.root = root
        self.points = points
        self.root.title("Shapefile Cutter")
        self.path_line = None

        # 创建 TkinterMapView 组件
        self.map_view = TkinterMapView(self.root, width=800, height=600, corner_radius=0)
        self.map_view.pack(fill="both", expand=True)

        # 设置地图中心点和缩放级别
        self.map_view.set_position(self.points[0][1], self.points[0][0])  # 你可以根据需要调整中心点
        self.map_view.set_zoom(10)  # 你可以根据需要调整缩放级别

        # 设置卫星影像服务的 tile 服务器 URL
        self.map_view.set_tile_server(
            "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}")

        # 显示提供的坐标点
        self.display_points(self.points)



    def display_points(self, points):
        for idx, (lon, lat) in enumerate(points):
            self.map_view.set_marker(lat, lon)



if __name__ == "__main__":
    root = tk.Tk()
    app = ShowlocUI(root,[(120.0750046,33.4890505),(120.0750044, 33.4890505), (120.0750041, 33.4890505), (120.0750038, 33.4890505)])
    root.mainloop()
