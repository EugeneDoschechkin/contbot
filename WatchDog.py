#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
t = 0
while True:
    try:
        t+=1
        print('Call ' + str(t))
        os.system('python3.6 bot.py')
    except:
        print('Back')
        continue
