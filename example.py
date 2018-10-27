#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: example.py
# version: 0.0.1
# description: tushare example


import tushare as ts


ts.get_stock_basics()

ts.get_hist_data('600848')

'''
date：日期
open：开盘价
high：最高价
close：收盘价
low：最低价
volume：成交量
price_change：价格变动
p_change：涨跌幅
ma5：5日均价
ma10：10日均价
ma20:20日均价
v_ma5:5日均量
v_ma10:10日均量
v_ma20:20日均量
turnover:换手率[注：指数无此项]
'''

# 设定历史数据的起始时间
ts.get_hist_data('600848',start='2015-01-05',end='2015-01-09')


ts.get_hist_data('600848', ktype='W') #获取周k线数据
ts.get_hist_data('600848', ktype='M') #获取月k线数据
ts.get_hist_data('600848', ktype='5') #获取5分钟k线数据
ts.get_hist_data('600848', ktype='15') #获取15分钟k线数据
ts.get_hist_data('600848', ktype='30') #获取30分钟k线数据
ts.get_hist_data('600848', ktype='60') #获取60分钟k线数据
ts.get_hist_data('sh'）#获取上证指数k线数据，其它参数与个股一致，下同
ts.get_hist_data('sz'）#获取深圳成指k线数据
ts.get_hist_data('hs300'）#获取沪深300指数k线数据
ts.get_hist_data('sz50'）#获取上证50指数k线数据
ts.get_hist_data('zxb'）#获取中小板指数k线数据
ts.get_hist_data('cyb'）#获取创业板指数k线数据
