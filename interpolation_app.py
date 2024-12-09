import tkinter as tk
from show_location import ShowlocUI
import pandas as pd
from tkinter import filedialog, messagebox
from process_data import find_lon_lat_ele
from scatter_plot import plot_raw_data
from RBF_interpolation import RBF_interpolation

class APP:
    def __init__(self,root):
        self.root = root
        self.root.geometry("600x300+100+100")  # 800x600 是宽度和高度，+100+100 是窗口左上角的起始位置
        self.root.title("河流地形插值")
        self.root.configure(bg="white")

        # 按钮选择文件
        self.select_button = tk.Button(self.root, text="选择文件", command=self.select_file)
        self.select_button.place(x=20,y=10)

        #显示河道位置
        self.show_loc_button = tk.Button(self.root, text="显示位置（需要翻墙）", command=self.show_loc)
        self.show_loc_button.place(x=20, y=120)

        #显示原始散点图
        self.show_scatter_data_button = tk.Button(self.root, text="显示散点图", command=self.plot_scatter)
        self.show_scatter_data_button.place(x=20, y=160)

        #显示插值结果
        self.show_scatter_data_button = tk.Button(self.root, text="显示插值结果", command=self.show_interpolation_result)
        self.show_scatter_data_button.place(x=20, y=200)

    #让用户选择文件，符合要求得到dataframe
    def select_file(self):
        # 打开文件选择对话框
        file_path = filedialog.askopenfilename(
            title="选择文件",
            filetypes=[("CSV 文件", "*.csv"), ("Excel 文件", "*.xls;*.xlsx")]
        )
        if not file_path:
            return  # 用户取消操作
        if file_path:
            self.df = self.check_file_type(file_path)
            self.find_column()


    #检查用户输入文件类型，符合则返回dataframe, 不符合则弹出警告
    def check_file_type(self,file_path):

        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path, encoding='ISO-8859-1')
            elif file_path.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file_path, encoding='ISO-8859-1')
            else:
                messagebox.showerror("错误", "请选择csv/xls/xlsx文件")

        except Exception as e:
            messagebox.showerror("错误", f"读取文件时出错: {e}")
        else:
            return df

    #尝试找到用户输入文件的经纬度列号，然后弹出让用户确定
    #如果找到先得到 self.longitude, self.latitude, self.elevation, self.lon_col, self.lat_col, self.ele_col
    #如果得不到就让用户输入列号
    def find_column(self):
        self.data_text = tk.Text(self.root, height=3, width=60)
        try:
            self.longitude, self.latitude, self.elevation, self.lon_col, self.lat_col, self.ele_col = find_lon_lat_ele(self.df)
            result_text = f'''经度：{self.longitude[0], self.longitude[1], self.longitude[2]}...\n纬度：{self.latitude[0], self.latitude[1], self.latitude[2]}...\n高程：{self.elevation[0], self.elevation[1], self.elevation[2]}...'''
            self.data_text.insert("1.0", result_text)
            self.data_text.place(x=100, y=10)
            self.data_text.configure(state='disabled')
            self.check_column(self.lon_col, self.lat_col, self.ele_col)



        except Exception as e:
            result_text = '请手动选择维度、经度、高程所在列'
            self.data_text.insert("1.0", result_text)
            self.data_text.place(x=100, y=10)
            self.data_text.configure(state='disabled')
            self.check_column(1,2,3)
            return None

    def check_column(self,ini_lon_col, ini_lat_col, ini_ele_col):
        self.lon_col_label = tk.Label(self.root,text="经度列号")
        self.lon_col_label.place(x=100,y=70)
        self.lon_col_entry = tk.Entry(self.root, width=5)
        self.lon_col_entry.place(x=160,y=71)
        self.lon_col_entry.insert(0, ini_lon_col)

        self.lat_col_label = tk.Label(self.root, text="纬度列号")
        self.lat_col_label.place(x=200, y=70)
        self.lat_col_entry = tk.Entry(self.root, width=5)
        self.lat_col_entry.place(x=260, y=71)
        self.lat_col_entry.insert(0, ini_lat_col)

        self.ele_col_label = tk.Label(self.root, text="高程列号")
        self.ele_col_label.place(x=300, y=70)
        self.ele_col_entry = tk.Entry(self.root, width=5)
        self.ele_col_entry.place(x=360, y=71)
        self.ele_col_entry.insert(0, ini_ele_col)

        self.change_col_confirm = tk.Button(self.root, text='确认修改',command=self.read_col_input)
        self.change_col_confirm.place(x=400, y=70)

    def read_col_input(self):
        #这里的列号从1开始数
        self.lon_col = int(self.lon_col_entry.get())
        self.lat_col = int(self.lat_col_entry.get())
        self.ele_col = int(self.ele_col_entry.get())

        self.longitude = self.df.iloc[1:, self.lon_col-1].tolist()
        self.latitude = self.df.iloc[1:, self.lat_col-1].tolist()
        self.elevation = self.df.iloc[1:, self.ele_col-1].tolist()

        #更改文本框内容
        self.data_text.configure(state='normal')
        self.data_text.delete("1.0", "end")
        result_text = f'''经度：{self.longitude[0], self.longitude[1], self.longitude[2]}...\n纬度：{self.latitude[0], self.latitude[1], self.latitude[2]}...\n高程：{self.elevation[0], self.elevation[1], self.elevation[2]}...'''
        self.data_text.insert("1.0", result_text)
        self.data_text.configure(state='disabled')

    #绘制原始数据三维散点图
    def plot_scatter(self):
        plot_raw_data(self.longitude, self.latitude, self.elevation)

    def show_interpolation_result(self):
        RBF_interpolation(self.latitude,self.longitude,self.elevation)

    def show_loc(self):
        new_window = tk.Toplevel(root)
        new_window.title("河道位置显示")
        ShowlocUI(new_window,list(zip(self.longitude, self.latitude)))



if __name__ == '__main__':
    root = tk.Tk()
    APP(root)
    root.mainloop()