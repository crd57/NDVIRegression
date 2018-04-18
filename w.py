# -*- coding:utf-8 _*-  
""" 
@author:crd
@file: w.py
@time: 2018/04/18 
"""
with open('D:/2018.4.10/test/w.txt', 'w') as file_o:
    for i in range(1953, 2014):
        str = ('con_prec%d.grd\n' % i)
        file_o.write(str)
