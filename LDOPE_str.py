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
with open('D:/NDVI/batch.cmd', 'w') as file_object:
    for year in range(2000, 2018):
        for day in enumerate(days):
            for nn in range(25, 27):
                if day[1] < 10:
                    strs = (
                        "unpack_sds_bits MOD13Q1.A%d00%d.h%dv05.006.hdf -sds=\"250m 16 days VI Quality\" -bit=0-1 "
                        "-of=MOD13Q1_A%d00%d.h%dv05.006.hdf\ncp_proj_param -ref=MOD13Q1.A%d00%d.h%dv05.006.hdf "
                        "MOD13Q1_A%d00%d.h%dv05.006.hdf -of=MOD13Q1_A%d00%d.h%dv05.006_unpack.hdf\ndel "
                        "MOD13Q1_A%d00%d.h%dv05.006.hdf\n" % (year, day[1], nn, year, day[1], nn, year, day[1], nn, year,
                                                            day[1], nn, year, day[1], nn, year, day[1], nn))
                if 10 <= day[1] < 100:
                    strs = (
                        "unpack_sds_bits MOD13Q1.A%d0%d.h%dv05.006.hdf -sds=\"250m 16 days VI Quality\" -bit=0-1 "
                        "-of=MOD13Q1_A%d0%d.h%dv05.006.hdf\ncp_proj_param -ref=MOD13Q1.A%d0%d.h%dv05.006.hdf "
                        "MOD13Q1_A%d0%d.h%dv05.006.hdf -of=MOD13Q1_A%d0%d.h%dv05.006_unpack.hdf\ndel "
                        "MOD13Q1_A%d0%d.h%dv05.006.hdf\n" % (year, day[1], nn, year, day[1], nn, year, day[1], nn, year,
                                                            day[1], nn, year, day[1], nn, year, day[1], nn))
                if day[1] >= 100:
                    strs = (
                        "unpack_sds_bits MOD13Q1.A%d%d.h%dv05.006.hdf -sds=\"250m 16 days VI Quality\" -bit=0-1 "
                        "-of=MOD13Q1_A%d%d.h%dv05.006.hdf\ncp_proj_param -ref=MOD13Q1.A%d%d.h%dv05.006.hdf "
                        "MOD13Q1_A%d%d.h%dv05.006.hdf -of=MOD13Q1_A%d%d.h%dv05.006_unpack.hdf\ndel "
                        "MOD13Q1_A%d%d.h%dv05.006.hdf\n" % (year, day[1], nn, year, day[1], nn, year, day[1], nn, year,
                                                            day[1], nn, year, day[1], nn, year, day[1], nn))
                file_object.write(strs)
