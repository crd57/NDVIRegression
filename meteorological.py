# -*- coding:utf-8 _*-  
""" 
@author:crd
@file: meteorological.py.py 
@time: 2018/04/21 
"""
import pandas as pd
import numpy as np


def openfile(filename):
    files = open(filename)
    data = pd.read_csv(files)
    return data


def teannual(data):
    data_ave = []
    for year in range(1980, 2018):
        data_year = sum(data['月平均气温'][data['年份'] == year])
        data_ave.append(data_year / 12)
    data_ava = np.array(data_ave)
    data_ave = data_ava.reshape(len(data_ave), 1)
    return data_ave


"""
def preannual(data):
    data_ave = []
    for year in range(1980, 2018):
        data_year = sum(data['月降水量'][data['年份'] == year])
        if year / 4 == 0:
            data_temp = data_year / 366
        else:
            data_temp = data_year / 365
        data_ave.append(data_temp)
    data_arr = np.array(data_ave)
    data_out = data_ave.reshape(len(data_arr), 1)
    return data_out
"""


def evannual(data):
    data_ave = []
    for year in range(1980, 2018):
        data_year = sum(data['月降水量'][data['年份'] == year])
        if year / 4 == 0:
            data_temp = data_year / 366
        else:
            data_temp = data_year / 365
        data_ave.append(data_temp)
    data_arr = np.array(data_ave)
    data_out = data_arr.reshape(len(data_arr), 1)
    return data_out


def saveout(filenames, fw):
    data = openfile(filenames)
    datat = teannual(data)
    datae = evannual(data)
    datas = np.hstack([datat, datae])
    data_from = pd.DataFrame(datas, index=np.arange(1980, 2018))
    data_from.rename(index=str, columns={0: '平均温度'}, inplace=True)
    data_from.rename(index=str, columns={1: '平均降水'}, inplace=True)
    data_from.to_csv(fw)


fw = open('D:/NDVI/out/out.csv', 'w')
for i in ['共和', '刚察', '天峻', '海晏']:
    path = i+'.csv'
    fw.write(i)
    saveout(path, fw)
fw.close()
