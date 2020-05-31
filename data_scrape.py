# -*- coding: utf-8 -*-
"""
Created on Thu May 28 21:08:45 2020

@author: Jason
"""

import glassdoor_scraper as gs
import pandas as pd

path = 'C:\\Users\\User\\Documents\\School\\code\\chromedriver.exe'

df = gs.get_jobs('data scientist',1000,False,path,5)

df.to_csv('glassdoor_jobs.csv', index=False)
