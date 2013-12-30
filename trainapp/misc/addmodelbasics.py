# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 16:17:18 2013

@author: amyskerry
"""
# copy and past into python terminal after running python manage.py shell (from traintracker dir)
from trainapp.models import *

timerange=[str(x) for x in range(0,4*60,30)]
reprange=[str(x) for x in range(0,30)]
cyclerange=[str(x) for x in range(0,20)]
routerange=[]
for x in range(7,14):
    for l in ['a','b','c','d']:
        routerange.append('5.'+str(x)+l)
boulderrange=['v'+str(x) for x in range(0,12)]

#boulder
wo=Workouts(WONAME='boulder_session', STYLE='boulder', OUTDOOR='outdoor',WOTIME='total time', WOREPS= 'reps at max', WOCYCLES=[], WOMAXAVG= 'max grade', CLEANS='# clean at max', METRIC='boulder', OTHER1=[], OTHER2=[], OTHER3=[], OTHER4=[], COMMENTS= 'comments')
wo.save()
wui=WorkoutUIs(WONAME='boulder_session', WOTIME=timerange, WOREPS= reprange, WOCYCLES= cyclerange, WOMAXAVG= boulderrange, CLEANS='textfield', OTHER1=[], OTHER2=[], OTHER3=[], OTHER4=[], COMMENTS= ['textbox'])
wui.save()

#boulder pyramid
wo=Workouts(WONAME='boulder_pyramid', STYLE='boulder', OUTDOOR='outdoor',WOTIME='total time', WOREPS= 'reps per grade', WOCYCLES= 'cycles', WOMAXAVG= 'max grade', CLEANS='# clean at max', METRIC=[], OTHER1=[], OTHER2=[], OTHER3=[], OTHER4=[], COMMENTS= 'comments')
wo.save()
wui=WorkoutUIs(WONAME='boulder_pyramid', WOTIME=timerange, WOREPS= reprange, WOCYCLES= cyclerange, WOMAXAVG= boulderrange, CLEANS='textfield', OTHER1=[], OTHER2=[], OTHER3=[], OTHER4=[], COMMENTS= ['textbox'])
wui.save()
#sport
wo=Workouts(WONAME='route_session', STYLE='route', OUTDOOR='outdoor',WOTIME='total time', WOREPS= 'reps at max', WOCYCLES=[], WOMAXAVG= 'max grade', CLEANS='# clean at max', METRIC='route', OTHER1=[], OTHER2=[], OTHER3=[], OTHER4=[], COMMENTS= 'comments')
wo.save()
wui=WorkoutUIs(WONAME='route_session', WOTIME=timerange, WOREPS= reprange, WOCYCLES= cyclerange, WOMAXAVG= routerange, CLEANS='textfield', OTHER1=[], OTHER2=[], OTHER3=[], OTHER4=[], COMMENTS= ['textbox'])
wui.save()

m=PossMetrics(METRIC="route", GRADERANGE=routerange, STYLE='route')
m.save()
m=PossMetrics(METRIC="boulder", GRADERANGE=boulderrange, STYLE='boulder')
m.save()



