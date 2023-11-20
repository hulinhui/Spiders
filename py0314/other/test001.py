# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         test001
# Description:  
# Author:       hlh
# Date:      2023/11/8 10:26
# -------------------------------------------------------------------------------
import requests

# Making a get request
response = requests.get('https://api.github.com/')
response = None
# print response
print(response)

# print if status code is less than 200
print(1 if response else 0)
