# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 16:34:50 2020

@author: Yurii
"""
import shutil
import os
from dirtools import create_directory
x = None
print(x)
if x == None:
    x = 'data_not_sorted_workfile_will_be_deleted'
create_directory(x, ['0'])
if os.path.exists('data_not_sorted_workfile_will_be_deleted'):
    shutil.rmtree('data_not_sorted_workfile_will_be_deleted')