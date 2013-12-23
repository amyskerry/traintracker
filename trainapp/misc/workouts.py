# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 18:28:02 2013

@author: amyskerry
"""
import json
import datetime
from django.utils import timezone
from trainapp.models import WorkoutEntries, Metrics

p = Metrics(METRIC="boulder (send)", GRADE="v6", DATE=timezone.now())

#constants
rootdir='/Users/amyskerry/Documents/projects/traintracker/trainapp/'

global userID, date, WOcolumns, metrics

#load in modules so that you have array of module dictionaries
with open(rootdir+'WOs_dict.json') as f:
    WOs = json.load(f)
with open(rootdir+'WOuispecs_dict.json') as f:
    WOuipecs = json.load(f)

#random function that defines misc details
def details():
    WOcolumns=WOs[0].keys()
    WOnames=[workout['WONAME'] for workout in WOs]
    metrics={'boulder (send)','sport (send)','TR (clean)','trad (send)','sport (finish)', 'trad (finish)'}
    datevar=datetime.datetime.now()
    date=datevar.strftime("%Y-%m-%d %H:%M")
    return WOcolumns, WOnames, metrics, date

#main functions
def login():
    #onstartup, sign in
    #userID= raw_input('Enter username: ')
    userID='askerry'
    # present html to get userID from user
    return userID
    
def choosetask():
    print "update metric or workout?" 
    choice= raw_input()
    #present html to get choice of task fromuser
    return choice
    
def worequest(WOs):
    print WOnames
    #desiredWO= raw_input('Enter desired workout: ')
    desiredWO='boulder'
    WOindex=find([workout['WONAME']==desiredWO for workout in WOs])
    currentWO=WOs[WOindex]
    currentUI=WOuispecs[WOindex]
    print WOindex
    return currentWO, currentUI

def write2sql(dictionary):
    for item in dictionary.items():
        sqlcol=item[0]
        sqlval=item[1]
        sql=""
    
def enterentry(currentWO, currentUI):    
    entrydict={'USERID':userID, 'DATE':date}
    for sqlcol in WOcolumns:
        if sqlcol!='METRIC':
            inputreq=currentWO[sqlcol]
            if inputreq!=[]:
                print inputreq+'?'
                entrydict[sqlcol]=raw_input()
    #abov should be seperate call to UI that returns entrydict
    #this function then extracts metric info and writes entry to sql            
    if currentWO['METRIC']!=[]:
        entrydict['METRIC']=currentWO['METRIC']
        extractmetric(entrydict)
        #write entry to sql

def extractmetric(entry):
    metric2update=entry['METRIC']
    grade=entry['WOMAXAVGRANGE']
    numatgrade=int(entry['CLEANS'])
    metricentry={'USERID':userID, 'DATE':date}
    for n in range(numatgrade):
        metricentry['GRADE']=grade
        metricentry['SENDTYPE']=metric2update
        print metricentry
        #write it to sql
        #write metricentry to sql
        
def reportmetric():
    [metric2update,grade,flash]=metricUI()
    metricentry={'USERID':userID, 'DATE':date, 'GRADE':grade, 'SENDTYPE':metric2update, 'FLASH':flash}
    print metricentry
    #write metricentry to sql
    
def metricUI():
    print metrics
    #make selector for the metrics
    metricselector='<select name="metric2update" id=dropdownsel>'
    for metric in metrics:
        metricselector=metricselector+'<option value="'+metric+'">'+metric+'</option>'
    metricselector=metricselector+'</select>'
    # metricselector can be inserted into relevant html location as a strings
    
    metric2update=raw_input('which metric?')
    grade=raw_input('grade?')
    flash=raw_input('flash?')
    return metric2update, grade, flash


#just debugging
[g,g,metrics,g]=details()
metricselector='<select name="metric2update">'
for metric in metrics:
    thisstr='<option value="'+metric+'">'+metric+'</option>'
    metricselector=metricselector+thisstr
metricselector=metricselector+'</select>'
    
    
