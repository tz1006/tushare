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
futu_data = data.loc[:'2018-09-10'][['close', 'ma5', 'ma10']]
hist_data = data.loc['2018-09-10':][['close', 'ma5', 'ma10']]
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
    start_date = datechange(select_date, -20)
    end_date = datechange(select_date, 8)
    data = ts.get_hist_data('600123',start=start_date,end=end_date)
    hist_data = data.loc[select_date:][['close', 'ma5', 'ma10']]
    last_close = hist_data.iloc[0]['close']
    ma4 = hist_data['close'][0:4].mean()
    ma9 = hist_data['close'][0:9].mean()
    d0ma5 = (ma4 * 4 + last_close * 1.04) / 5
    d0ma10 = (ma9 * 9 + last_close * 1.04) / 10
    d1ma5 = hist_data.iloc[0]['ma5']
    d1ma10 = hist_data.iloc[0]['ma10']
    d2ma5 = hist_data.iloc[1]['ma5']
    d3ma5 = hist_data.iloc[2]['ma5']
    if (d1ma5 < d1ma10) and (d3ma5 < d2ma5 < d1ma5) and (d0ma5 > d0ma10):
        d0 = data.loc[:select_date].index[-2]
        futu_data = data.loc[:d0]
        close = futu_data['close'].mean()
        close_ratio = close / last_close - 1
        high = futu_data['high'].max()
        high_ratio = high / last_close - 1
        low = futu_data['low'].min()
        low_ratio = low / last_close - 1
        result = [(close, close_ratio), (high, high_ratio), (low, low_ratio)]
    else:
        result = None


dd = {}

for i in tqdm(ftid):
    print(i)
    r =  model1(i, '2018-09-05')
    dd[i] = r


def analyze_model1(code):
    print(code)
    r =  model1(code, '2018-09-05')
    dd[i] = r



from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

dd = {}

def analyze_model1(code):
    #print(code)
    r =  model1(code, '2018-09-05')
    dd[code] = r
    #print(dd)


def t_analyze_model1():
    futures = []
    with ThreadPoolExecutor(max_workers=200) as executor:
        for i in ftid:
            futures.append(executor.submit(analyze_model1, i))
        kwargs = {'total': len(futures)}
        for f in tqdm(as_completed(futures), **kwargs):
            pass




