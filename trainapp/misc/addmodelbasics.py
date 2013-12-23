# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 16:17:18 2013

@author: amyskerry
"""
# copy and past into python terminal after running python manage.py shell (from traintracker dir)
from trainapp.models import Metrics, WorkoutEntries, Usernames, Workouts, WorkoutUIs, PossMetrics

timerange=[str(x) for x in range(0,8*60,30)]
reprange=[str(x) for x in range(0,50)]
cyclerange=[str(x) for x in range(0,20)]
routerange=[]
for x in range(6,14):
    for l in ['a','b','c','d']:
        routerange.append('5.'+str(x)+l)
boulderrange=['v'+str(x) for x in range(0,14)]

#boulder
wo=Workouts(WONAME='boulder', INDOUT='outdoor',WOTIME='total time', WOREPS= 'reps at max', WOCYCLES=[], WOMAXAVG= 'max grade', CLEANS='# clean at max', METRIC='boulder--send', OTHER1=[], OTHER2=[], OTHER3=[], OTHER4=[], COMMENTS= 'comments')
wo.save()
wui=WorkoutUIs(WONAME='boulder', WOTIME=timerange, WOREPS= reprange, WOCYCLES= cyclerange, WOMAXAVG= boulderrange, CLEANS='textfield', OTHER1=[], OTHER2=[], OTHER3=[], OTHER4=[], COMMENTS= ['textbox'])
wui.save()

#TR
wo=Workouts(WONAME='TR', INDOUT='outdoor',WOTIME='total time', WOREPS= 'reps at max', WOCYCLES= [], WOMAXAVG= 'max grade', CLEANS='# clean at max', METRIC='TR--clean', OTHER1=[], OTHER2=[], OTHER3=[], OTHER4=[], COMMENTS= 'comments')
wo.save()
wui=WorkoutUIs(WONAME='TR', WOTIME=timerange, WOREPS= reprange, WOCYCLES= cyclerange, WOMAXAVG= routerange, CLEANS='textfield', OTHER1=[], OTHER2=[], OTHER3=[], OTHER4=[], COMMENTS= ['textbox'])
wui.save()
#boulder pyramid
wo=Workouts(WONAME='boulder_pyramid', INDOUT='outdoor',WOTIME='total time', WOREPS= 'reps per grade', WOCYCLES= 'cycles', WOMAXAVG= 'max grade', CLEANS='# clean at max', METRIC=[], OTHER1=[], OTHER2=[], OTHER3=[], OTHER4=[], COMMENTS= 'comments')
wo.save()
wui=WorkoutUIs(WONAME='boulder_pyramid', WOTIME=timerange, WOREPS= reprange, WOCYCLES= cyclerange, WOMAXAVG= boulderrange, CLEANS='textfield', OTHER1=[], OTHER2=[], OTHER3=[], OTHER4=[], COMMENTS= ['textbox'])
wui.save()
#sport
wo=Workouts(WONAME='sport', INDOUT='outdoor',WOTIME='total time', WOREPS= 'reps at max', WOCYCLES=[], WOMAXAVG= 'max grade', CLEANS='# clean at max', METRIC='sport--send', OTHER1=[], OTHER2=[], OTHER3=[], OTHER4=[], COMMENTS= 'comments')
wo.save()
wui=WorkoutUIs(WONAME='sport', WOTIME=timerange, WOREPS= reprange, WOCYCLES= cyclerange, WOMAXAVG= routerange, CLEANS='textfield', OTHER1=[], OTHER2=[], OTHER3=[], OTHER4=[], COMMENTS= ['textbox'])
wui.save()

m=PossMetrics(METRIC="SPORT--send", GRADERANGE=routerange)
m.save()
m=PossMetrics(METRIC="SPORT--finish", GRADERANGE=routerange)
m.save()
m=PossMetrics(METRIC="TRAD--send", GRADERANGE=routerange)
m.save()
m=PossMetrics(METRIC="TRAD--finish", GRADERANGE=routerange)
m.save()
m=PossMetrics(METRIC="BOULDER--send", GRADERANGE=boulderrange)
m.save()
m=PossMetrics(METRIC="TR--clean", GRADERANGE=routerange)
m.save()


