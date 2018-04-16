# -*- coding:utf-8 _*-  
""" 
@author:crd
@file: LDOPE_str.py 
@time: 2018/04/15 
"""
import numpy as np

xl = lambda x: 16 * x + 1
n = np.arange(22)
days = xl(n)
with open('D:/NDVI/batch.txt', 'w') as file_object:
    for year in range(2000, 2018):
        for day in enumerate(days):
            if day[1] < 10:
                strs = (
                        "unpack_sds_bits MOD13Q1.A%d00%d.hdf -sds= \"250m 16 days VI Quality\" -bit=0-3 "
                        "-of=MOD13Q1_A%d00%d.hdf \n" %
                        (year, day[1], year, day[1]))
            if 10 <= day[1] < 100:
                strs = (
                        "unpack_sds_bits MOD13Q1.A%d0%d.hdf -sds= \"250m 16 days VI Quality\" -bit=0-3 "
                        "-of=MOD13Q1_A%d0%d.hdf \n" %
                        (year, day[1], year, day[1]))
            if day[1] >= 100:
                strs = (
                        "unpack_sds_bits MOD13Q1.A%d%d.hdf -sds= \"250m 16 days VI Quality\" -bit=0-3 "
                        "-of=MOD13Q1_A%d%d.hdf \n" %
                        (year, day[1], year, day[1]))
            file_object.write(strs)
