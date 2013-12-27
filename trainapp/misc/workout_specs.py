# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 20:36:27 2013

@author: amyskerry
"""

import json

rootdir='/Users/amyskerry/Documents/projects/trainapp/'

othermax=30
timerange=[str(x) for x in range(0,4*60,30)]
reprange=[str(x) for x in range(0,30)]
cyclerange=[str(x) for x in range(0,20)]
routerange=[]
for x in range(7,14):
    for l in ['a','b','c','d']:
        routerange.append('5.'+str(x)+l)
boulderrange=['v'+str(x) for x in range(0,12)]

defaultUIs={'WONAME':[], 'INDOUT':['radio',['indoor', 'outdoor']], 'WOTIME':['scroll',timerange], 'WOREPS': ['scroll', reprange], 'WOCYCLES': ['scroll', cyclerange], 'WOMAXAVGRANGE': ['textfield'], 'CLEANS':['textfield'], 'METRIC':[], 'OTHER1':[], 'OTHER2':[], 'OTHER3':[], 'OTHER4':[], 'COMMENTS': ['textbox']}
WOsqlspecs={'WONAME':'varchar(30)','INDOUT':'varchar(20)', 'WOTIME':'float(4,2)', 'WOREPS': 'int', 'WOCYCLES': 'int', 'WOMAXAVGRANGE': 'varchar(5)', 'CLEANS':'int', 'METRIC':'varchar(30)', 'OTHER1':'varchar('+str(othermax)+')', 'OTHER2':'varchar('+str(othermax)+')', 'OTHER3':'varchar('+str(othermax)+')', 'OTHER4':'varchar('+str(othermax)+')','COMMENTS': 'text'}

# one time specifications
WOs=[]
WOuispecs=[]
WOs.append({'WONAME':'boulder', 'INDOUT':'outdoor?', 'WOTIME':'time', 'WOREPS': 'reps at max', 'WOCYCLES': [], 'WOMAXAVGRANGE': 'max grade', 'CLEANS':'clean at max', 'METRIC':'boulder (send)', 'OTHER1':[], 'OTHER2':[], 'OTHER3':[], 'OTHER4':[], 'COMMENTS': 'comments'})
thisui=defaultUIs
thisui['WOMAXAVGRANGE']=[['scroll'],boulderrange]
WOuispecs.append(thisui)
WOs.append({'WONAME':'TR', 'INDOUT':'outdoor?', 'WOTIME':'time', 'WOREPS': 'reps at max', 'WOCYCLES': [], 'WOMAXAVGRANGE': 'max grade', 'CLEANS':'clean at max', 'METRIC':'TR (clean)', 'OTHER1':[], 'OTHER2':[], 'OTHER3':[], 'OTHER4':[],'COMMENTS': 'comments'})
thisui=defaultUIs
thisui['WOMAXAVGRANGE']=[['scroll'],routerange]
WOuispecs.append(thisui)
WOs.append({'WONAME':'boulder pyramid','INDOUT':[], 'WOTIME':'time', 'WOREPS': 'reps', 'WOCYCLES': 'cycles', 'WOMAXAVGRANGE': 'max grade', 'CLEANS':'clean at max', 'METRIC':[], 'OTHER1':[], 'OTHER2':[], 'OTHER3':[], 'OTHER4':[],'COMMENTS': 'comments'})
thisui=defaultUIs
thisui['WOMAXAVGRANGE']=[['minmax'],boulderrange]
WOuispecs.append(thisui)


with open(rootdir+'WOs_dict.json', 'w') as f:
    json.dump(WOs, f)
with open(rootdir+'WOuispecs_dict.json', 'w') as f:
    json.dump(WOuispecs, f)
