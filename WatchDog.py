#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
t = 0
while True:
    try:
        t+=1
        print('Call ' + str(t))
        os.system('python bot.py')
    except:
        print('Back')
        continue
