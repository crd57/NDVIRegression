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
    im_filename1 = ('D:/tif/%d/MOD13Q1.A%d%d.250m_16_days_NDVI.tif' % (month, year, data1_day))
    im_filename2 = ('D:/tif/%d/MOD13Q1.A%d%d.250m_16_days_NDVI.tif' % (month, year, data2_day))
    im_data1, im_bands1, im_geotrans1, im_proj1 = read_ndvi(im_filename1)
    im_data2, im_bands2, im_geotrans2, im_proj2 = read_ndvi(im_filename2)
    yearData = max_data(im_data1, im_data2)
    return yearData


def re_shape(im_data):
    shape = np.shape(im_data)
    x = im_data.reshape([shape[0] * shape[1], 1])
    return x, shape


def regression(x, y):
    """
    线性回归
    :param x:
    :param y:
    :return:
    """
    lr = LinearRegression(n_jobs=-1)
    # (fit_intercept=True是否加入截距, normalize=False, copy_X=True, n_jobs=1使用几个CPU)
    lr.fit(x, y)
    lr.score(x, y)
    plt.scatter(x, y, color='green')
    plt.plot(x, lr.predict(x), color='blue', linewidth=3)
    plt.xlabel('Average Number of Rooms per Dwelling(RM)')
    plt.ylabel('Houseing Price')
    plt.title('2D Demo of Linear Regression')
    plt.show()
    return lr


def re_im(Weights, shape):
    Weights.reshape([shape[0], shape[1]])
    return Weights


def writeTiff(im_data, im_width, im_height, im_bands, im_geotrans, im_proj, path):
    """
    写Tiff文件
    :param im_data:影像矩阵
    :param im_width: 影像的宽
    :param im_height: 影像的长
    :param im_bands: 影像的波段
    :param im_geotrans: 影像的仿射变换参数
    :param im_proj: 影像的投影
    :param path: 输出路径
    :return: 输出影像
    """
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32

    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    elif len(im_data.shape) == 2:
        im_data = np.array([im_data])
    else:
        im_bands, (im_height, im_width) = 1, im_data.shape
        # 创建文件
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(path, im_width, im_height, im_bands, datatype)
    if dataset is not None:
        dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
        dataset.SetProjection(im_proj)  # 写入投影
    for i in range(im_bands):
        dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
    del dataset


def int2bin(n, count=16):
    """
    十进制转二进制
    :param n: 十进制数
    :param count: 多少比特位
    :return: 二进制数
    """
    return "".join([str((n >> y) & 1) for y in range(count - 1, -1, -1)])


def quality(im_data, Bits):
    """
    质量依赖数据读取
    :param im_data:
    :param Bits:
    :return:
    """
    shape = np.shape(im_data)
    data_quality = np.empty(shape)
    for row in range(shape[0]):
        for col in range(shape[1]):
            temp = int2bin(im_data[row, col])
            data_quality[row, col] = int(temp[Bits])
    return data_quality


