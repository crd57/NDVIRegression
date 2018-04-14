# -*- coding:utf-8 _*-  
""" 
@author:crd
@file: ndvi_regression.py
@time: 2018/04/13 
"""
import gdal
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


def read_ndvi(fileName):
    dataset = gdal.Open(fileName)
    if dataset is None:
        print(fileName + "文件无法打开")
        return
    im_width = dataset.RasterXSize  # 栅格矩阵的列数
    im_height = dataset.RasterYSize  # 栅格矩阵的行数
    im_bands = dataset.RasterCount  # 波段数
    im_data = dataset.ReadAsArray(0, 0, im_width, im_height)  # 获取数据
    im_geotrans = dataset.GetGeoTransform()  # 获取仿射矩阵信息
    im_proj = dataset.GetProjection()  # 获取投影信息
    return im_data, im_bands, im_geotrans, im_proj


def data_check(data):
    """
    If the value is abnormal, correct
    :param data:no correct data
    :return:correct data
    """
    data[data < -1] = -1
    data[data > 1] = 1
    return data


def max_data(data1, data2):
    """
    将每月两景数据最大值合成
    :param data1: first view
    :param data2: second view
    :return: maxdata
    """
    data1 = data_check(data1)
    data2 = data_check(data2)
    data_shape = np.shape(data1)
    for row in range(data_shape[0]):
        for col in range(data_shape[1]):
            data1[row][col] = np.max([data1[row][col], data2[row][col]])
    return data1


def year_data(year, month):
    """
    读取数据，处理数据
    :param year:
    :param month:
    :return:
    """
    data1_day = (2 * month - 1) * 16 + 1
    data2_day = (2 * month) * 16 + 1
    filename1 = ('D:/tif/%d/MOD13Q1.A%d%d.250m_16_days_NDVI.tif' % (month, year, data1_day))
    filename2 = ('D:/tif/%d/MOD13Q1.A%d%d.250m_16_days_NDVI.tif' % (month, year, data2_day))
    im_data1, im_bands1, im_geotrans1, im_proj1 = read_ndvi(filename1)
    im_data2, im_bands2, im_geotrans2, im_proj2 = read_ndvi(filename2)
    yearData = max_data(im_data1, im_data2)
    return yearData


def re_shape(im_data):
    shape = np.shape(im_data)
    x = im_data.reshape([shape[0] * shape[1], 1])
    return x, shape


def re_im(Weights, shape):
    Weights.reshape([shape[0], shape[1]])
    return Weights


def regression(x, y):
    lr = LinearRegression(n_jobs=-1)
    # (fit_intercept=True是否加入截距, normalize=False, copy_X=True, n_jobs=1使用几个CPU)
    lr.fit(x, y)
    lr.score(x, y)
    predict = lr.predict(x)
    plt.scatter(x, y, color='green')
    plt.plot(x, predict, color='blue', linewidth=3)
    plt.xlabel('Average Number of Rooms per Dwelling(RM)')
    plt.ylabel('Houseing Price')
    plt.title('2D Demo of Linear Regression')
    plt.show()
    return lr
