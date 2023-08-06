# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 10:18:29 2023

@author: lass_j
"""

websites = [r'https://www.ill.eu/sites/ccsl/ffacts/ffactnode5.html', # 3d
            r'https://www.ill.eu/sites/ccsl/ffacts/ffactnode9.html', # 3d J2
            r'https://www.ill.eu/sites/ccsl/ffacts/ffactnode6.html', # 4d
            r'https://www.ill.eu/sites/ccsl/ffacts/ffactnode10.html', # 4d J2
            r'https://www.ill.eu/sites/ccsl/ffacts/ffactnode7.html', # rare earths
            r'https://www.ill.eu/sites/ccsl/ffacts/ffactnode11.html', # rare earths J2
            r'https://www.ill.eu/sites/ccsl/ffacts/ffactnode8.html', # actinide 
            r'https://www.ill.eu/sites/ccsl/ffacts/ffactnode12.html', # actinide  J2
            ]



import pandas as pd
import numpy as np

formFactor = {'columns':['A','a','B','b','C','c','D','A2','a2','B2','b2','C2','c2','D2']}


for web in websites:
    dfs = pd.read_html(web)
    dat = np.asarray(dfs[0][1:])
    for line in dat:
        ion = line[0]
        
        if not ion in formFactor: # not in the dictionary
            
            formFactor[ion] = [float(x) for x in line[1:]]
        else:
            
            formFactor[ion] = formFactor[ion]+[float(x) for x in line[1:]]
            



for key,value in formFactor.items():
    formFactor[key] = np.asarray(value)