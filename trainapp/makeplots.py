# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 00:24:38 2013

@author: amyskerry
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

labeldict={'avggr':'avg grade', 'avreps':'avg reps', 'counts':'counts'}

dc.name='boulder'
dc.plotvar='avggr'
dc.bins=['2013-12-20', '2013-12-26']
dc.plotvector=[0.0, 1.8888888888888888]

filterstring= 'filtered by :
for fn, filtername in enumerate(dc.filternames):
    if fn<(len(dc.filternames-2)):
    filterstring=filterstring+filtername+','

