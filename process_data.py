import pandas as pd
import numpy as np

def find_lon_lat_ele(df):
    c1 = df.iloc[1:, 0].tolist()
    c2 = df.iloc[1:, 1].tolist()
    c3 = df.iloc[1:, 2].tolist()
    c4 = df.iloc[1:, 3].tolist()


    elevation,latitude,longitude = None, None, None

    if if_ele(c4):
        elevation = c4
        ele_col = 4

    if if_ele(c3):
        elevation = c3
        ele_col = 3

    if if_lon(c1):
        longitude = c1
        lon_col = 1


    if if_lon(c2):
        longitude = c2
        lon_col = 2

    if if_lon(c3):
        longitude = c3
        lon_col = 3

    if if_lat(c1):
        latitude = c1
        lat_col = 1

    if if_lat(c2):
        latitude = c2
        lat_col = 2

    if if_lat(c3):
        latitude = c3
        lat_col = 3

    return longitude, latitude, elevation, lon_col, lat_col, ele_col



def count_decimal_places(value):
    if isinstance(value, float) or isinstance(value, int):  # 确保是数字类型
        str_value = str(value)
        if "." in str_value:
            return len(str_value.split(".")[1])  # 获取小数部分的长度
        else:
            return 0  # 没有小数部分
    return 0  # 非数字返回 None

def if_lon(lst):
    if np.mean(lst) > 70 and count_decimal_places(lst[3])>=5:
        return True
    return False


def if_lat(lst):
    if 70 > np.mean(lst) > 10 and count_decimal_places(lst[3])>=5:
        return True
    return False

def if_ele(lst):
    if 4>=count_decimal_places(lst[3])>=1:
        return True
    return False




if __name__ == "__main__":
    df = pd.read_csv(r'D:\pyprojects\interpolation\2023-05-15 16-00-48.csv', encoding='ISO-8859-1')

    longitude, latitude, elevation, lon_col, lat_col, ele_col = find_lon_lat_ele(df)
    print(longitude)
    print(latitude)
    print(elevation)