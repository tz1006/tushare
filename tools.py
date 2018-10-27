#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: tools.py
# version: 0.0.1
# description: tools.py



from datetime import datetime, timedelta


def datechange(date, change):
    d = datetime.strptime(date,'%Y-%m-%d').date()
    new_d = d + timedelta(days=change)
    new_date = new_d.strftime('%Y-%m-%d')
    return new_date





