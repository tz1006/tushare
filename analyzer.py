#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: analyzer.py
# version: 0.0.1
# description: analyze ma


import tushare as ts
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import futuquant as ft



def datechange(date, change):
    d = datetime.strptime(date,'%Y-%m-%d').date()
    new_d = d + timedelta(days=change)
    new_date = new_d.strftime('%Y-%m-%d')
    return new_date


import futuquant as ft

q = ft.OpenQuoteContext(host='sz.omg.tf', port=11111)
# 沪深A股
hs = q.get_plate_stock('SH.3000005')[1]
q.close()
hs['code'] = hs['code'].map(lambda x: x[3:])
# 富途牛牛Code
ftid = hs.set_index('code').drop(columns=['stock_owner','stock_name', 'lot_size', 'stock_child_type', 'stock_type', 'list_time']).T.to_dict('records')[0]







# MA5 MA10 某日交叉后走势

code = '600123'
select_date = '2018-05-09'
start_date = datechange(select_date, -20)
end_date = datechange(select_date, 8)

data = ts.get_hist_data(code,start=start_date,end=end_date)
d0 = data.loc[:select_date].index[-2]
hist_data = data.loc[d0:][['close', 'ma5', 'ma10']]

last_close = hist_data.iloc[1]['close']
ma4 = hist_data[1:5]['close'].mean()
ma9 = hist_data[1:10]['close'].mean()
d0ma5p = (ma4 * 4 + last_close * 1.04) / 5
d0ma10p = (ma9 * 9 + last_close * 1.04) / 10
d1ma5 = hist_data.iloc[1]['ma5']
d1ma10 = hist_data.iloc[1]['ma10']
d2ma5 = hist_data.iloc[2]['ma5']
d3ma5 = hist_data.iloc[3]['ma5']
d0ma5 = hist_data.iloc[0]['ma5']
d0ma10 = hist_data.iloc[0]['ma10']


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
    

# model1('600123', '2018-05-09')
def model1(code, select_date):
    start_date = datechange(select_date, -20)
    end_date = datechange(select_date, 8)
    data = ts.get_hist_data(code, start=start_date,end=end_date)
    hist_data = data.loc[select_date:][['close', 'ma5', 'ma10']]
    #print(hist_data)
    last_close = hist_data.iloc[0]['close']
    ma4 = hist_data['close'][0:4].mean()
    ma9 = hist_data['close'][0:9].mean()
    d0ma5 = (ma4 * 4 + last_close * 1.04) / 5
    d0ma10 = (ma9 * 9 + last_close * 1.04) / 10
    d1ma5 = hist_data.iloc[0]['ma5']
    d1ma10 = hist_data.iloc[0]['ma10']
    d2ma5 = hist_data.iloc[1]['ma5']
    d3ma5 = hist_data.iloc[2]['ma5']
    # print('LAST_CLOSE: %s \nMA4: %s \nMA9: %s \nd0MA5: %s \nd0MA10: %s \nd1MA5: %s \nd1MA10: %s \nd2MA5: %s \nd3MA5: %s' % (last_close, ma4, ma9, d0ma5, d0ma10, d1ma5, d1ma10, d2ma5, d3ma5))
    if (d1ma5 < d1ma10) and (d3ma5 < d2ma5 < d1ma5) and (d0ma5 > d0ma10):
        #print(True)
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
    return result


dd = {}

for i in tqdm(ftid):
    print(i)
    r =  model1(i, '2018-09-05')
    dd[i] = r


def analyze_model1(code):
    #print(code)
    r =  model1(code, '2018-05-09')
    dd[code] = r



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


def printdd():
    li = {}
    for i in dd:
        r = dd[i]
        if r != None:
            li[i] = r
    close_win = 0
    for x in li:
        rr = li[x]
        close_ratio = rr[0][1]
        if close_ratio > 0.01:
            close_win += 1
        print(x)
        print(rr)
    print(len(li))
    print('close_win:')
    print(close_win)




class model1():
    def __init__(self, date, rising_ratio=1.04):
        self.date = date
        self.rising_ratio = rising_ratio
        self.dd = {}
    def model1(self, code, select_date, rising_ratio):
        start_date = datechange(select_date, -20)
        end_date = datechange(select_date, 8)
        data = ts.get_hist_data(code, start=start_date,end=end_date)
        hist_data = data.loc[select_date:][['close', 'ma5', 'ma10']]
        #print(hist_data)
        last_close = hist_data.iloc[0]['close']
        ma4 = hist_data['close'][0:4].mean()
        ma9 = hist_data['close'][0:9].mean()
        d0ma5 = (ma4 * 4 + last_close * rising_ratio) / 5
        d0ma10 = (ma9 * 9 + last_close * rising_ratio) / 10
        d1ma5 = hist_data.iloc[0]['ma5']
        d1ma10 = hist_data.iloc[0]['ma10']
        d2ma5 = hist_data.iloc[1]['ma5']
        d3ma5 = hist_data.iloc[2]['ma5']
        # print('LAST_CLOSE: %s \nMA4: %s \nMA9: %s \nd0MA5: %s \nd0MA10: %s \nd1MA5: %s \nd1MA10: %s \nd2MA5: %s \nd3MA5: %s' % (last_close, ma4, ma9, d0ma5, d0ma10, d1ma5, d1ma10, d2ma5, d3ma5))
        if (d1ma5 < d1ma10) and (d3ma5 < d2ma5 < d1ma5) and (d0ma5 > d0ma10):
            #print(True)
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
        return result
    def analyze_model1(self, code, date, rising_ratio):
        #print(code)
        r = self.model1(code, date, rising_ratio)
        self.dd[code] = r
    def analyze(self):
        futures = []
        with ThreadPoolExecutor(max_workers=200) as executor:
            for i in ftid:
                futures.append(executor.submit(self.analyze_model1, i, self.date, self.rising_ratio))
            kwargs = {'total': len(futures)}
            for f in tqdm(as_completed(futures), **kwargs):
                pass
    def printresult(self):
        li = {}
        for i in self.dd:
            r = dd[i]
            if r != None:
                li[i] = r
        close_win = 0
        for x in li:
            rr = li[x]
            close_ratio = rr[0][1]
            if close_ratio > 0.01:
                close_win += 1
            print(x)
            print(rr)
        print(len(li))
        print('close_win:')
        print(close_win)
    
    
# a = model('2018-05-09')
class model2():
    def __init__(self, date, rising_ratio=1.04):
        self.date = date
        self.rising_ratio = rising_ratio
        self.dd = {}
    def model2(self, code, select_date, rising_ratio):
        start_date = datechange(select_date, -20)
        end_date = datechange(select_date, 8)
        data = ts.get_hist_data(code, start=start_date,end=end_date)
        d0 = data.loc[:select_date].index[-2]
        hist_data = data.loc[d0:][['close', 'ma5', 'ma10', 'high']]
        last_close = hist_data.iloc[1]['close']
        d0high = hist_data.iloc[0]['high']
        ma4 = hist_data[1:5]['close'].mean()
        ma9 = hist_data[1:10]['close'].mean()
        d0ma5p = (ma4 * 4 + last_close * 1.04) / 5
        d0ma10p = (ma9 * 9 + last_close * 1.04) / 10
        d0ma5h = (ma4 * 4 + d0high) / 5
        d0ma10h = (ma9 * 9 + d0high) / 10
        d1ma5 = hist_data.iloc[1]['ma5']
        d1ma10 = hist_data.iloc[1]['ma10']
        d2ma5 = hist_data.iloc[2]['ma5']
        d3ma5 = hist_data.iloc[3]['ma5']
        # print('LAST_CLOSE: %s \nMA4: %s \nMA9: %s \nd0MA5: %s \nd0MA10: %s \nd1MA5: %s \nd1MA10: %s \nd2MA5: %s \nd3MA5: %s' % (last_close, ma4, ma9, d0ma5, d0ma10, d1ma5, d1ma10, d2ma5, d3ma5))
        if (d1ma5 < d1ma10) and (d3ma5 < d2ma5 < d1ma5) and (d0ma5p > d0ma10p) and (d0ma5h > d0ma10h):
            #print(True)
            futu_data = data.loc[:d0]
            even_pirce = ma9 * 9 - ma4 * 8
            even_ratio = even_pirce / last_close - 1
            close = futu_data['close'].mean()
            close_ratio = close / last_close - 1
            high = futu_data['high'].max()
            high_ratio = high / last_close - 1
            low = futu_data['low'].min()
            low_ratio = low / last_close - 1
            r = [(even_pirce, even_ratio), (close, close_ratio), (high, high_ratio), (low, low_ratio)]
        else:
            r = None
        return r
    def analyze_model2(self, code, date, rising_ratio):
        #print(code)
        r = self.model2(code, date, rising_ratio)
        self.dd[code] = r
    def analyze(self):
        futures = []
        with ThreadPoolExecutor(max_workers=200) as executor:
            for i in ftid:
                futures.append(executor.submit(self.analyze_model2, i, self.date, self.rising_ratio))
            kwargs = {'total': len(futures)}
            for f in tqdm(as_completed(futures), **kwargs):
                pass
    def result(self):
        li = {}
        for i in self.dd:
            r = self.dd[i]
            if r != None:
                li[i] = r
        close_win = 0
        for x in li:
            rr = li[x]
            close_ratio = rr[1][1]
            if close_ratio > 0.01:
                close_win += 1
            print(x)
            print(rr)
        print(len(li))
        print('close_win:')
        print(close_win)
    



# a = model3('2018-05-09')
class model3():
    def __init__(self, date, rising_ratio=1.04):
        self.date = date
        self.rising_ratio = rising_ratio
        self.dd = {}
    def model3(self, code, select_date, rising_ratio):
        start_date = datechange(select_date, -20)
        end_date = datechange(select_date, 8)
        data = ts.get_hist_data(code, start=start_date,end=end_date)
        d0 = data.loc[:select_date].index[-2]
        hist_data = data.loc[d0:][['close', 'ma5', 'ma10', 'high']]
        last_close = hist_data.iloc[1]['close']
        d0high = hist_data.iloc[0]['high']
        ma4 = hist_data[1:5]['close'].mean()
        ma9 = hist_data[1:10]['close'].mean()
        d0ma5p = (ma4 * 4 + last_close * 1.04) / 5
        d0ma10p = (ma9 * 9 + last_close * 1.04) / 10
        d0ma5h = (ma4 * 4 + d0high) / 5
        d0ma10h = (ma9 * 9 + d0high) / 10
        d1ma5 = hist_data.iloc[1]['ma5']
        d1ma10 = hist_data.iloc[1]['ma10']
        d2ma5 = hist_data.iloc[2]['ma5']
        d3ma5 = hist_data.iloc[3]['ma5']
        #print('LAST_CLOSE: %s \nd0HIGH: %s \nMA4: %s \nMA9: %s \nd0MA5p: %s \nd0MA10p: %s \nd0MA5h: %s \nd0MA10h: %s \nd1MA5: %s \nd1MA10: %s \nd2MA5: %s \nd3MA5: %s' % (last_close, d0high, ma4, ma9, d0ma5p, d0ma10p, d0ma5h, d0ma10h, d1ma5, d1ma10, d2ma5, d3ma5))
        if (d1ma5 < d1ma10) and (d2ma5 < d3ma5 < d1ma5) and (d0ma5p > d0ma10p) and (d0ma5h > d0ma10h):
            #print(True)
            futu_data = data.loc[:d0]
            even_pirce = ma9 * 9 - ma4 * 8
            even_ratio = even_pirce / last_close - 1
            close = futu_data['close'].mean()
            close_ratio = close / last_close - 1
            high = futu_data['high'].max()
            high_ratio = high / last_close - 1
            low = futu_data['low'].min()
            low_ratio = low / last_close - 1
            r = [(even_pirce, even_ratio), (close, close_ratio), (high, high_ratio), (low, low_ratio)]
        else:
            r = None
        return r
    def analyze_model3(self, code, date, rising_ratio):
        #print(code)
        r = self.model3(code, date, rising_ratio)
        self.dd[code] = r
    def analyze(self):
        futures = []
        with ThreadPoolExecutor(max_workers=200) as executor:
            for i in ftid:
                futures.append(executor.submit(self.analyze_model3, i, self.date, self.rising_ratio))
            kwargs = {'total': len(futures)}
            for f in tqdm(as_completed(futures), **kwargs):
                pass
    def result(self):
        li = {}
        for i in self.dd:
            r = self.dd[i]
            if r != None:
                li[i] = r
        close_win = 0
        for x in li:
            rr = li[x]
            close_ratio = rr[1][1]
            if close_ratio > 0.01:
                close_win += 1
            print(x)
            print(rr)
        print(len(li))
        print('close_win:')
        print(close_win)
    


    
# 未完成
# a = model4('2018-05-09')
# a.analyze()
class model4():
    def __init__(self, date, rising_ratio=1.04):
        self.date = date
        self.rising_ratio = rising_ratio
        self.df = pd.DataFrame(columns=['code', 'd0CLOSE', 'd1MA5', 'd1MA10', 'd2MA5', 'd2MA10', 'd3MA5', 'd3MA10', 'EvenPrice', 'EvenRatio', 'ClosePrice', 'CloseRatio', 'High', 'HighRatio', 'Low', 'LowRatio'])
    def model4(self, code, select_date, rising_ratio):
        start_date = datechange(select_date, -20)
        end_date = datechange(select_date, 8)
        data = ts.get_hist_data(code, start=start_date,end=end_date)
        d0 = data.loc[:select_date].index[-2]
        hist_data = data.loc[d0:][['close', 'ma5', 'ma10', 'high']]
        last_close = hist_data.iloc[1]['close']
        d0high = hist_data.iloc[0]['high']
        ma4 = hist_data[1:5]['close'].mean()
        ma9 = hist_data[1:10]['close'].mean()
        d0ma5p = (ma4 * 4 + last_close * 1.04) / 5
        d0ma10p = (ma9 * 9 + last_close * 1.04) / 10
        d0ma5h = (ma4 * 4 + d0high) / 5
        d0ma10h = (ma9 * 9 + d0high) / 10
        d1ma5 = hist_data.iloc[1]['ma5']
        d1ma10 = hist_data.iloc[1]['ma10']
        d2ma5 = hist_data.iloc[2]['ma5']
        d2ma10 = hist_data.iloc[2]['ma10']
        d3ma5 = hist_data.iloc[3]['ma5']
        d3ma10 = hist_data.iloc[3]['ma10']
        #print('LAST_CLOSE: %s \nd0HIGH: %s \nMA4: %s \nMA9: %s \nd0MA5p: %s \nd0MA10p: %s \nd0MA5h: %s \nd0MA10h: %s \nd1MA5: %s \nd1MA10: %s \nd2MA5: %s \nd3MA5: %s' % (last_close, d0high, ma4, ma9, d0ma5p, d0ma10p, d0ma5h, d0ma10h, d1ma5, d1ma10, d2ma5, d3ma5))
        if (d1ma5 < d1ma10) and (d2ma5 < d3ma5 < d1ma5) and (d0ma5p > d0ma10p) and (d0ma5h > d0ma10h) and (d2ma10 > d2ma5) and (d1ma10 < d2ma10):
            #print(True)
            futu_data = data.loc[:d0]
            even_pirce = ma9 * 9 - ma4 * 8
            even_ratio = even_pirce / last_close - 1
            close = futu_data['close'].mean()
            close_ratio = close / last_close - 1
            high = futu_data['high'].max()
            high_ratio = high / last_close - 1
            low = futu_data['low'].min()
            low_ratio = low / last_close - 1
            self.df.loc[len(self.df)] = [code, last_close, d1ma5, d1ma10, d2ma5, d2ma10, d3ma5, d3ma10, even_pirce, even_ratio, close, close_ratio, high, high_ratio, low, low_ratio]
        else:
            pass
    def analyze_model4(self, code, date, rising_ratio):
        #print(code)
        r = self.model4(code, date, rising_ratio)
    def analyze(self):
        futures = []
        with ThreadPoolExecutor(max_workers=200) as executor:
            for i in ftid:
                futures.append(executor.submit(self.analyze_model4, i, self.date, self.rising_ratio))
            kwargs = {'total': len(futures)}
            for f in tqdm(as_completed(futures), **kwargs):
                pass
    def result(self):
        li = {}
        for i in self.dd:
            r = self.dd[i]
            if r != None:
                li[i] = r
        close_win = 0
        for x in li:
            rr = li[x]
            close_ratio = rr[1][1]
            if close_ratio > 0.01:
                close_win += 1
            print(x)
            print(rr)
        print(len(li))
        print('close_win:')
        print(close_win)
       

a = model4('2018-09-20')
a.analyze()
    
    
    
    
a = model3('2018-07-11')
a.model3('002902', '2018-07-11', 1.04)
