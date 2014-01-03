# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 11:26:52 2013

@author: amyskerry
"""
import datetime
from trainapp.models import Metrics, WorkoutEntries, Usernames, Workouts, WorkoutUIs, PossMetrics

class dataview():
    def __init__(self):
        self.bins = []
        self.name =[]
        self.data=[]
        self.filters=[]
        self.binneddata =[]
        self.filternames=[]
        self.filtervalue=[]
        self.counts =[]

def bindata(data,startdatetuple):
    const=1
    [mindate,maxdate]=getdateends(data, startdatetuple) 
    datebins=getbins(mindate,maxdate,const)
    counts=[[] for thisbin in datebins]
    for entry in data:
        datelist=entry.DATE.split('-')
        dateobj=datetime.date(int(datelist[0]), int(datelist[1]), int(datelist[2]))
        binned=False
        for binnum, thisbin in enumerate(datebins):
            if not binned:
                if (dateobj-thisbin).days<=0 :
                    binned=True
                    counts[binnum].append(entry)
    return datebins,counts
def getbins(mindate,maxdate,binconst):
    datebins=[]
    daterange=(maxdate-mindate).days
    for d in range(0,daterange,7*binconst):
        datebins.append(mindate+datetime.timedelta(days=d))
    datebins.append(maxdate+datetime.timedelta(days=1))
    return datebins
        
def getdateends(data, startdatetuple):
    for entryn,entry in enumerate(data):
        datelist=entry.DATE.split('-')    
        dateobj=datetime.date(int(datelist[0]), int(datelist[1]), int(datelist[2]))
        if entryn==0:
            mindate=dateobj
            maxdate=dateobj
        else:
            mintd=(mindate-dateobj).days
            maxtd=(maxdate-dateobj).days
            if maxtd<0:
                maxdate=dateobj
            if mintd>0:
                mindate=dateobj
    #wops. hackily overriding this because this approach leads to different bins for different variables
    mindate=datetime.date(startdatetuple[0], startdatetuple[1], startdatetuple[2])
    maxdate=datetime.date.today()
    return mindate,maxdate
def sortdata(datachoices):
    allchoices=[]
    for choice in datachoices:
        thischoice=dataview()
        thischoice.name=choice.encode('ascii','ignore')
        thischoice.data=Metrics.objects.all().filter(METRIC=choice)
        if not thischoice.data: #len(data)<1
            thischoice.data=WorkoutEntries.objects.all().filter(WONAME=choice)
        if thischoice.data:
            [bins,thischoice.binneddata]=bindata(thischoice.data)
            thischoice.counts=[len(databin) for databin in thischoice.binneddata]
            thischoice.bins=map(lambda binobj:binobj.strftime("%Y-%m-%d"), bins)
            allchoices.append(thischoice)
    return allchoices
def filterdata(filternames,filtervals,thischoice, data, username):
    # do remaining filtering and add the data to the object
    data=data.filter(USERID=username) #always filter by username
    if 'WOREPS' in filternames:
        data=data.filter(WOREPS__in=thischoice.WOREPS)
    if 'WOCYCLES' in filternames:
        data=data.filter(WOCYCLES__in=thischoice.WOCYCLES)
    if 'WOMAXAVG' in filternames:
        data=data.filter(WOMAXAVG__in=thischoice.WOMAXAVG)
    if 'GRADE' in filternames:
        data=data.filter(GRADE__in=thischoice.GRADE)
    if 'OUTDOOR' in filternames:
        data=data.filter(OUTDOOR=thischoice.OUTDOOR)
    if 'COMMENTS' in filternames:
        data=data.filter(COMMENTS__contains=thischoice.COMMENTS)
    if 'STATUS' in filternames:
        data=data.filter(STATUS=thischoice.STATUS)
    if 'LEAD' in filternames:
        data=data.filter(LEAD=thischoice.LEAD)
    if 'TYPE' in filternames:
        data=data.filter(TYPE=thischoice.TYPE)
    return data