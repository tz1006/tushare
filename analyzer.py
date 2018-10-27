#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: analyzer.py
# version: 0.0.1
# description: analyze ma


import tushare as ts


# MA5 MA10 某日交叉后走势

code = '600123'
select_date = '2018-09-10'
start_date = '2018-09-05'
end_date = '2018-09-15'

data = ts.get_hist_data('600123',start='2018-09-05',end='2018-09-15')
futu_data = df.loc[:'2018-09-10'][['close', 'ma5', 'ma10']]
hist_data = df.loc['2018-09-10':][['close', 'ma5', 'ma10']]
last_close = hist_data.iloc[0]['close']
ma4 = hist_data['close'][0:4].mean()
ma9 = hist_data['close'][0:9].mean()

d0ma5 = (ma4 * 4 + last_close * 1.04) / 5
d0ma10 = (ma9 * 9 + last_close * 1.04) / 10
d1ma5 = hist_data.iloc[0]['ma5']
d1ma10 = hist_data.iloc[0]['ma10']
d2ma5 = hist_data.iloc[1]['ma5']
d3ma5 = hist_data.iloc[2]['ma5']

if (d1ma5 < d1ma10) and (d3ma5 < d2ma5 < d1ma5):
    


def model1(code, select_date):
    start_date = 
    data = ts.get_hist_data('600123',start='2018-09-05',end='2018-09-15')

