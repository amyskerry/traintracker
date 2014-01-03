from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import datetime, time
import numpy as np
import seaborn as sns
import random
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

from trainapp.models import Metrics, WorkoutEntries, Usernames, Workouts, WorkoutUIs, PossMetrics
from trainapp.analyzefunctions import *

global timerange, reprange, cyclerange, routerange, boulderrange, datachoices, datevar, startdatetuple, footertext, headertext
timerange=[str(x) for x in range(0,4*60,30)]
reprange=[str(x) for x in range(0,50)]
cyclerange=[str(x) for x in range(0,20)]
routerange=[]
for x in range(7,14):
    for l in ['a','b','c','d']:
        routerange.append('5.'+str(x)+l)
boulderrange=['v'+str(x) for x in range(0,12)]
datachoices=[]
#datevar=time.strftime("%Y-%m-%d")
#can add to earlier times by manually adjustigthis e.g. 
datevar='2013-12-11'
startdatetuple=(2013,10,01)
footertext="traintracker.2013"
headertext="STRONG FOR THAILAND"

def index(request):
    global datachoices
    datachoices=[]
    title='TrainTracker'
    stored_users=Usernames.objects.all()
    try:
        usernames=[induser.USERID for induser in stored_users]
    except:
        usernames=[]
    context = {'pagetitle': title, 'usernames': usernames, 'headertext':headertext, 'footertext':footertext}
    return render(request, 'trainapp/index.html', context)
def loggedin(request):
    username=request.POST['username']
    goal='Get Strong!'
    try:
        goal=request.POST['goal']
    except:
        pass
    if username=="none":
        username=request.POST['newuser']    
    try: 
        u=Usernames.objects.get(USERID=username)
    except:
        u=Usernames(USERID=username)
        u.GOAL=goal
        u.save()
    return HttpResponseRedirect(reverse('trainapp.views.chooseworkout', args=(username,)))
def homepage(request, username):
    u=Usernames.objects.get(USERID=username)
    goal=u.GOAL           
    myphoto='trainapp/'+username+'.jpg'
    metricreports = Metrics.objects.order_by('USERID')[:5]
    context ={'metricreports': metricreports, 'userid':username, 'goal': goal, 'myphoto':myphoto,'headertext':headertext, 'footertext':footertext}
    #return HttpResponse(template.render(context))
    return render(request, 'trainapp/choose.html', context)
    
def chooseworkout(request, username):
    global datachoices
    datachoices=[]
    u=Usernames.objects.get(USERID=username)
    goal=u.GOAL           
    myphoto='trainapp/'+username+'.jpg'
    context={'userid': username, 'goal': goal, 'myphoto':myphoto,'headertext':headertext, 'footertext':footertext}
    # get wo possibilities
    workouts=Workouts.objects.all()
    context['wooptions']=[workout.WONAME for workout in workouts]
    return render(request, 'trainapp/chooseworkout.html', context)
def choosemetric(request, username):
    global datachoices
    datachoices=[]
    u=Usernames.objects.get(USERID=username)
    goal=u.GOAL           
    myphoto='trainapp/'+username+'.jpg'
    # get wo possibilities
    metrics=PossMetrics.objects.all()
    context={'userid': username, 'metricoptions':[metric.METRIC for metric in metrics], 'goal': goal, 'myphoto':myphoto,'headertext':headertext, 'footertext':footertext}
    return render(request, 'trainapp/choosemetric.html', context)
def dataentry(request, username):
    global datachoices
    datachoices=[]
    u=Usernames.objects.get(USERID=username)
    goal=u.GOAL           
    myphoto='trainapp/'+username+'.jpg'
    wk=request.POST['wochoice'] # find user choice
    # get parameters and ui specs for that workout
    workout = get_object_or_404(Workouts, WONAME=wk)
    workoutUI = get_object_or_404(WorkoutUIs, WONAME=wk)
    propobjs=workout._meta.fields
    propnames=[prop.name for prop in propobjs]
    workouttimes=workoutUI.WOTIME[1:-1].replace("'","").replace("[","").replace("]","").split(",") #to convert back to list
    workoutreps=workoutUI.WOREPS[1:-1].replace("'","").replace("[","").replace("]","").split(",") 
    workoutcycles=workoutUI.WOCYCLES[1:-1].replace("'","").replace("[","").replace("]","").split(",") 
    workoutgrades=workoutUI.WOMAXAVG[1:-1].replace("'","").replace("[","").replace("]","").split(",") 
    workoutcleans=workoutUI.CLEANS[1:-1].replace("'","").replace("[","").replace("]","").split(",")
    print workout.OTHER1
    context={'userid': username, 'workout':workout, 'workoutui':workoutUI, 'propnames': propnames, 'workouttimes':workouttimes,'workoutreps':workoutreps,'workoutcycles':workoutcycles,'workoutgrades':workoutgrades,'workoutcleans':workoutcleans, 'goal': goal, 'myphoto':myphoto,'headertext':headertext, 'footertext':footertext}
    # still want to provide wo possibilities
    workouts=Workouts.objects.all()
    context['wooptions']=[workout.WONAME for workout in workouts]
    return render(request, 'trainapp/dataentry.html', context)
    
def updated(request, username):
    u=Usernames.objects.get(USERID=username)
    goal=u.GOAL           
    myphoto='trainapp/'+username+'.jpg'
    wk=request.POST['WONAME'].encode('ascii','ignore')
    workout = get_object_or_404(Workouts, WONAME=wk)
    entry=WorkoutEntries(WONAME=wk)
    #set default
    entry.WOTIME=0
    entry.OUTDOOR=0
    entry.WOREPS=0
    entry.STATUS=1
    if workout.STYLE=='route':
        entry.TYPE=0
        entry.LEAD=0
    else:
        entry.TYPE=[]
        entry.LEAD=[]
    entry.WOCYCLES=0
    entry.WOMAXAVG=''
    entry.CLEANS=0
    entry.COMMENTS=''
    entry.OTHER1=''
    entry.OTHER2=''
    entry.OTHER3=''
    entry.OTHER4=''
    #update (figure out cleaner way to do this)
    try:
        entry.WOTIME=int(request.POST['WOTIME'].encode('ascii','ignore'))
    except:
        pass
    try:
        entry.TYPE=request.POST['TYPE'].encode('ascii','ignore')
        print entry.TYPE
    except:
        pass
    try:
        entry.STATUS=int(request.POST['STATUS'].encode('ascii','ignore'))
        print entry.STATUS
    except:
        pass
    try:
        entry.LEAD=int(request.POST['LEAD'].encode('ascii','ignore'))
        print entry.LEAD
    except:
        pass
    try:
        entry.OUTDOOR=bool(request.POST['OUTDOOR'].encode('ascii','ignore'))
    except:
        pass
    try:
        entry.WOREPS=int(request.POST['WOREPS'].encode('ascii','ignore'))
    except:
        pass
    try:
        entry.WOCYCLES=int(request.POST['WOCYCLES'].encode('ascii','ignore'))
    except:
        pass
    try:
        entry.WOMAXAVG=request.POST['WOMAXAVG'].encode('ascii','ignore')
    except:
        pass
    try:
        entry.CLEANS=int(request.POST['CLEANS'].encode('ascii','ignore'))
    except:
        pass
    try:
        entry.COMMENTS=request.POST['COMMENTS'].encode('ascii','ignore')
    except:
        pass
    try:
        entry.OTHER1=request.POST['OTHER1'].encode('ascii','ignore')
    except:
        pass
    try:
        entry.OTHER2=request.POST['OTHER2'].encode('ascii','ignore')
    except:
        pass
    try:
        entry.OTHER3=request.POST['OTHER3'].encode('ascii','ignore')
    except:
        pass
    try:
        entry.OTHER4=request.POST['OTHER4'].encode('ascii','ignore')
    except:
        pass
    entry.DATE=datevar
    workout = get_object_or_404(Workouts, WONAME=wk)
    propobjs=workout._meta.fields
    propnames=[prop.name for prop in propobjs]
    context={'propnames':propnames, 'entry':entry, 'workout': workout, 'userid':username, 'goal': goal, 'myphoto':myphoto, 'headertext':headertext, 'footertext':footertext}
    entry.save()
    print "hi"
    print workout
    metric=workout.METRIC
    print metric
    if metric:
        for x in range(entry.CLEANS):
            m=Metrics(METRIC=metric, GRADE=entry.WOMAXAVG, DATE=datevar, USERID=username, OUTDOOR=entry.OUTDOOR)
            print m
            m.save()
    #should add optional metric save here as well
    return render(request, 'trainapp/updated.html', context)
def metrics(request, username):
    datachoices=[]
    u=Usernames.objects.get(USERID=username)
    goal=u.GOAL           
    myphoto='trainapp/'+username+'.jpg'
    metric=request.POST['METRIC'].encode('ascii','ignore')
    metricinfo=PossMetrics.objects.get(METRIC=metric)
    graderange=metricinfo.GRADERANGE[1:-1].replace("'","").replace("[","").replace("]","").split(",")
    #metricvals=Metrics._meta.fields
    #metricnames=[mval.name for mval in metricvals]
    metrics=PossMetrics.objects.all()
    metricoptions=[thism.METRIC for thism in metrics]
    context={'userid': username, 'metric': metric, 'metricoptions': metricoptions, 'graderange':graderange, 'goal': goal, 'myphoto':myphoto, 'metricinfo':metricinfo, 'headertext':headertext, 'footertext':footertext}
    return render(request, 'trainapp/metrics.html', context)
def report(request,username):
    u=Usernames.objects.get(USERID=username)
    goal=u.GOAL           
    myphoto='trainapp/'+username+'.jpg'
    metric=request.POST['METRIC'].encode('ascii','ignore')
    themetric = get_object_or_404(PossMetrics, METRIC=metric)
    mentry=Metrics(METRIC=metric)
    mentry.DATE=datevar
    mentry.USERID=username
    mentry.GRADE=''
    mentry.STATUS=0
    if themetric.STYLE=='route':
        mentry.TYPE=0
        mentry.LEAD=0
    else:
        mentry.TYPE=[]
        mentry.LEAD=[]
    mentry.OUTDOOR=0
    mentry.COMMENTS=''
    try:
        mentry.GRADE=request.POST['GRADE'].encode('ascii','ignore')
    except:
        pass
    try:
        mentry.OUTDOOR=bool(request.POST['OUTDOOR'].encode('ascii','ignore'))
        print mentry.OUTDOOR
    except:
        pass
    try:
        mentry.COMMENTS=request.POST['COMMENTS'].encode('ascii','ignore')
    except:
        pass
    try:
        mentry.TYPE=request.POST['TYPE'].encode('ascii','ignore')
        print mentry.TYPE
    except:
        pass
    try:
        mentry.STATUS=int(request.POST['STATUS'].encode('ascii','ignore'))
        print mentry.STATUS
    except:
        pass
    try:
        mentry.LEAD=int(request.POST['LEAD'].encode('ascii','ignore'))
        print mentry.LEAD
    except:
        pass
    mentry.save()
    metricvals=Metrics._meta.fields
    metricnames=[mval.name for mval in metricvals]
    context={'userid': username, 'fieldnames':metricnames, 'mentry':mentry, 'goal': goal, 'myphoto':myphoto,'headertext':headertext, 'footertext':footertext}
    return render(request, 'trainapp/report.html', context)
def choosedata(request, username):
    u=Usernames.objects.get(USERID=username)
    goal=u.GOAL           
    myphoto='trainapp/'+username+'.jpg'
    pms=PossMetrics.objects.all()
    pmnames=[pm.METRIC for pm in pms]
    wos=Workouts.objects.all()
    wonames=[wo.WONAME for wo in wos]
    allnames=wonames+pmnames
    context={'userid': username, 'pmnames':pmnames, 'wonames':wonames, 'allnames': allnames, 'goal': goal, 'myphoto':myphoto,'headertext':headertext, 'footertext':footertext}
    return render(request, 'trainapp/choosedata.html', context)
def choosefilters(request, username):
    u=Usernames.objects.get(USERID=username)
    goal=u.GOAL           
    myphoto='trainapp/'+username+'.jpg'
    datachoice=request.POST.get('data').encode('ascii','ignore')
    try:    
        chosen=PossMetrics.objects.get(METRIC=datachoice)
    except:
        chosen=Workouts.objects.get(WONAME=datachoice)
    routetype=chosen.STYLE
    pms=PossMetrics.objects.all()
    pmnames=[pm.METRIC for pm in pms]
    wos=Workouts.objects.all()
    wonames=[wo.WONAME for wo in wos]
    allnames=wonames+pmnames
    context={'userid': username, 'pmnames':pmnames, 'wonames':wonames, 'allnames': allnames, 'goal': goal, 'myphoto':myphoto, 'routetype':routetype,'headertext':headertext, 'footertext':footertext}
    try:    
        dataclass=PossMetrics.objects.get(METRIC=datachoice)
        context['woORme']='me'
        context['graderange']=dataclass.GRADERANGE[1:-1].replace("'","").replace("[","").replace("]","").split(",")
    except:
        dataclass = get_object_or_404(Workouts, WONAME=datachoice)
        context['woORme']='wo'
        workoutUI = get_object_or_404(WorkoutUIs, WONAME=datachoice)
        context['workoutreps']=workoutUI.WOREPS[1:-1].replace("'","").replace("[","").replace("]","").split(",") 
        context['workoutcycles']=workoutUI.WOCYCLES[1:-1].replace("'","").replace("[","").replace("]","").split(",") 
        context['workoutgrades']=workoutUI.WOMAXAVG[1:-1].replace("'","").replace("[","").replace("]","").split(",") 
    context['dataclass']=dataclass
    return render(request, 'trainapp/choosefilters.html', context)
def viewdata(request, username):
    u=Usernames.objects.get(USERID=username)
    goal=u.GOAL           
    myphoto='trainapp/'+username+'.jpg'
    #get the datachoice
    datachoice=request.POST.get('dataWO').encode('ascii','ignore')
    objtype='Workouts'
    if not datachoice:
        datachoice=request.POST.get('dataMetric').encode('ascii','ignore')
        objtype='Metrics'
    #get the datatype and create dataview object
    datatype=request.POST.get('countsORavg').encode('ascii','ignore')
    thischoice=dataview()
    thischoice.name=datachoice
    thischoice.plotvar=datatype
    thischoice.objtype=objtype
    if objtype=='Workouts':
        data=WorkoutEntries.objects.filter(WONAME=datachoice)
    elif objtype=='Metrics':
        data=Metrics.objects.filter(METRIC=datachoice)
    possiblefilters=['WOREPS', 'WOCYCLES', 'WOMAXAVG', 'GRADE', 'COMMENTS', 'OUTDOOR', 'STATUS', 'LEAD', 'TYPE']
    filternames=[]
    filtervals=[]
    for thisfilter in possiblefilters:
        if thisfilter=='WOREPS' or thisfilter=='WOCYCLES' or thisfilter == 'WOMAXAVG' or thisfilter =='GRADE':
            x=request.POST.getlist(thisfilter)
        elif thisfilter=='COMMENTS':
            x=request.POST.get(thisfilter)
        elif thisfilter=='OUTDOOR':
            x=request.POST.get(thisfilter)
            if x=='1':
                x=1
            if x=='2':
                x=0
        elif thisfilter=='STATUS':
            try:
                x=int(request.POST.get(thisfilter))
            except:
                x=[]
        elif thisfilter=='LEAD':
            try:
                x=int(request.POST.get(thisfilter))
            except:
                x=[]
        elif thisfilter=='TYPE':
            try:
                x=request.POST.get(thisfilter)
            except:
                x=[]
        if x != [] and x != '' and x != None:
            try:
                x=map(lambda i:int(i), x)
            except:
                pass
            setattr(thischoice, thisfilter, x)
            print thisfilter
            print x
            filternames.append(thisfilter)
            filtervals.append(x) 
    thischoice.data=filterdata(filternames,filtervals,thischoice, data)
    print "this is the data:"+str(thischoice.data)
    # do other things
    if thischoice.data:
        [bins,thischoice.binneddata]=bindata(thischoice.data, startdatetuple)
        thischoice.counts=[len(databin) for databin in thischoice.binneddata]
        thischoice.bins=map(lambda binobj:binobj.strftime("%Y-%m-%d"), bins)        
        thischoice.filternames=filternames
        thischoice.filtervals=filtervals
    # once fully filtered, append to list
        datachoices.append(thischoice)
    context={'userid': username,'datachoices':datachoices, 'goal': goal, 'myphoto':myphoto,'headertext':headertext, 'footertext':footertext}
    return render(request, 'trainapp/viewdata.html', context)
def plotdata(request, username):
    plt.close('all')
    u=Usernames.objects.get(USERID=username)
    goal=u.GOAL           
    myphoto='trainapp/'+username+'.jpg'
    context ={'userid':username, 'goal': goal, 'myphoto':myphoto,'headertext':headertext, 'footertext':footertext}
    print "found"
    print datachoices
    for dc in datachoices:
        if dc.plotvar=="sessions":
            vector=dc.counts
        if dc.plotvar=="counts":
            vector=[]
            for thebin in dc.binneddata:
                sumit=0
                for entry in thebin:
                    try:
                        sumit=sumit+entry.CLEANS
                    except:
                        sumit=sumit+1
                vector.append(sumit)
        elif dc.plotvar=="avggr":
            vector=[]
            for thebin in dc.binneddata:
                avggr=[]
                for entry in thebin:
                    entrygrade=0
                    try:
                        e= entry.GRADE
                        entrygrade=len(e)>0
                    except:
                        e=entry.WOMAXAVG
                        entrygrade=len(e)>0
                    if entrygrade:
                        if dc.objtype=='Metrics':
                            entry.GRADE=entry.GRADE.replace(' ','') #erm figure out where that space is coming from...
                            pref=entry.GRADE[0].encode('ascii','ignore')
                            if pref=='5':
                                pref=pref+'.'
                            dc.gradepref=pref
                            grade=entry.GRADE[1:]#cut off the initial 5/V
                        elif dc.objtype=='Workouts':
                            entry.WOMAXAVG=entry.WOMAXAVG.replace(' ','')
                            pref=entry.WOMAXAVG[0].encode('ascii','ignore')
                            if pref=='5':
                                pref=pref+'.'
                            dc.gradepref=pref
                            grade=entry.WOMAXAVG[1:]
                        grade=[x for x in list(grade) if x.isdigit()]
                        if type(grade)==list and len(grade)>0:
                            grade=float(''.join(grade))
                            avggr.append(grade)
                        elif type(grade)==str:
                             grade=float(grade)
                        elif type(grade)==list and len(grade)==0:
                            pass
                avggrade=np.mean(np.array(avggr))
                vector.append(avggrade)
        elif dc.plotvar=="avgrep":
            vector=[]
            for thebin in dc.binneddata:
                avgrep=[]
                for entry in thebin:
                        if dc.objtype=='Metrics':
                            avgrep=0
                        elif dc.objtype=='Workouts':
                            reps=entry.WOREPS
                            try:
                                reps=float(reps)
                                avggr.append(reps)
                            except:
                                pass
                avgreps=np.mean(np.array(avgrep))
                vector.append(avgreps)
        nv=[]
        for v in vector:
            if not np.isnan(v):
                nv.append(v)
            else:
                nv.append(0.0)
        vector=nv
        dc.plotvector=vector
    vardict={'avggr':'avg grade', 'avgrep':'avg reps', 'counts':'# climbs', 'sessions':'# sessions'}
    filterdict={'WOTIME':'time', 'WOREPS':'reps','WOCYCLES':'cycles', 'WOMAXAVG':'grade', 'GRADE':'grade', 'OUTDOOR':'outdoor', 'COMMENTS':'comments'}        
    numplots=len(datachoices)
    sns.set(style='nogrid')
    #ourfigsize=[8,6]
    ourfigsize=[12,8]
    bgcolor='black'
    axiscolor='white'
    textcolor='white'
    plotcolor=(.2,.59,.92)
    font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12,}
    matplotlib.rc('font', **font)
    if numplots>0:
        fig,axarr=plt.subplots(numplots, sharex=True, figsize=ourfigsize, facecolor=bgcolor) #squeeze=False returns an array even if just one
        for dn,dc in enumerate(datachoices):
            if dc.plotvector !=[]:
                filterstring= dc.name.upper().replace('_', ' ') +' (filtered by: '
                for fn, filtername in enumerate(dc.filternames):
                    fv=dc.filtervals[fn]
                    print filtername
                    print fv
                    print type(fv)
                    if type(fv)==list:
                        minfv=fv[0].encode('ascii','ignore')
                        maxfv=fv[-1].encode('ascii','ignore')
                        fv=minfv+'-'+maxfv
                    elif type(fv)==int:
                        fv=str(fv)
                    else: 
                        fv=str(fv)
                        
                    if fn<(len(dc.filternames)-1):
                        filterstring=filterstring+filterdict[filtername]+'='+fv +', '
                    else:
                        filterstring=filterstring+filterdict[filtername]+'='+fv
                filterstring=filterstring+')'
                title=filterstring
                try:
                    ax=axarr[dn]
                except: 
                    ax=axarr
                #ax.plot(dc.plotvector, color=plotcolor, marker="8", ls='none')
                x=range(len(dc.plotvector))
                y=dc.plotvector[:]
                ax.bar(x,y, color=plotcolor, width=1)
                ylocbase=np.floor((max(dc.plotvector)-min(dc.plotvector))/4)
                if ylocbase==0:
                    ylocbase=1
                yloc = plticker.MultipleLocator(base=ylocbase)
                ax.yaxis.set_major_locator(yloc)
                ax.set_ylim(top=max(dc.plotvector)+.25)
                ax.set_xlim(left=0,right=len(dc.plotvector)+.25)
                ax.set_axis_bgcolor(axiscolor)
                ax.set_title(title, color=textcolor, fontsize=14)
                ax.set_ylabel(vardict[dc.plotvar],color=textcolor, fontsize=12)
                yticklabels=ax.get_yticks()
                yticklabels=map(lambda x:int(x), yticklabels)
                try:
                    yticklabels=[dc.gradepref+str(tick) for tick in yticklabels]
                except:
                    pass
                ax.set_yticklabels(yticklabels,color=textcolor, fontsize=12)
                xindex=ax.get_xticks()
                xticklabels=[dc.bins[xn] for xn,xv in enumerate(dc.bins) if xn in xindex]
                ax.set_xticklabels(xticklabels,rotation='40', color=textcolor, fontsize=14) #rotation='60'
        plt.gcf().subplots_adjust(bottom=0.16, left=.05, hspace = .6)
        randomint=str(random.randint(0,100))
        fig.savefig('/Users/amyskerry/Documents/projects/traintracker/trainapp/static/trainapp/plots/temp'+randomint+'.png', facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close('all')
        context['photoshow']='trainapp/plots/temp'+randomint+'.png'
    else:
        context['photoshow']='trainapp/solo.jpg'   
        
    return render(request, 'trainapp/plotdata.html', context)
def newworkout(request, username):
    u=Usernames.objects.get(USERID=username)
    goal=u.GOAL           
    myphoto='trainapp/'+username+'.jpg'
    context={'userid':username, 'goal': goal, 'myphoto':myphoto, 'headertext':headertext, 'footertext':footertext}
    return render(request, 'trainapp/newworkout.html', context)
def newworkoutupdate(request, username):
    u=Usernames.objects.get(USERID=username)
    goal=u.GOAL           
    myphoto='trainapp/'+username+'.jpg'
    inputstyle=0
    inputreps=0
    inputcycles=0
    inputgrade=0
    inputname=request.POST['inputname'].encode('ascii','ignore')
    inputname=inputname.replace(' ', '_')
    print inputname
    try:
        inputstyle=request.POST['inputstyle'].encode('ascii','ignore')
        print inputstyle
    except:
        pass
    try:
        inputreps=request.POST['inputreps'].encode('ascii','ignore')
        print inputreps
    except:
        pass
    try:
        inputcycles=request.POST['inputcycles'].encode('ascii','ignore')
        print inputcycles
    except:
        pass
    try:
        inputgrade=request.POST['inputgrade'].encode('ascii','ignore')
        print inputgrade
    except:
        pass
    inputother1=request.POST['inputother1'].encode('ascii','ignore')
    print inputother1
    inputother2=request.POST['inputother2'].encode('ascii','ignore')
    print inputother2
    print type(inputother2)
    inputother3=request.POST['inputother3'].encode('ascii','ignore')
    print inputother3
    inputother4=request.POST['inputother4'].encode('ascii','ignore')
    print inputother4
    wo=Workouts(WONAME=inputname, STYLE=inputstyle, OUTDOOR='outdoor',WOTIME='total time', COMMENTS= 'comments')
    wui=WorkoutUIs(WONAME=inputname, WOTIME=timerange,COMMENTS=['textbox'])
    if inputreps:
        wo.WOREPS='reps'
        wui.WOREPS= reprange
    else:
        wo.WOREPS=[]
        wui.WOREPS= []
    if inputcycles:
        wo.WOCYCLES='cycles'
        wui.WOCYCLES= cyclerange
    else:
        wo.WOCYCLES=[]
        wui.WOCYCLES= []
    if inputgrade:
        wo.WOMAXAVG='grade'
        wo.CLEANS='# clean at max'
        wui.CLEANS=reprange
        if inputstyle=='boulder':
            wui.WOMAXAVG=boulderrange
        elif inputstyle=='route':
            wui.WOMAXAVG=routerange
        else:
            wui.WOMAXAVG='textfield'
    else:
        wo.WOMAXAVG=[]
        wui.WOMAXAVG=[]
        wo.CLEANS=[]
        wui.CLEANS=[]
    if inputstyle=='boulder':
        wo.METRIC='boulder'
    elif inputstyle=='route':
        wo.METRIC='route'
    else:
        wo.METRIC=[]
    if inputother1 !='':
        wo.OTHER1=inputother1
        wui.OTHER1='textfield'
    else:
        wo.OTHER1=[]
        wui.OTHER1=[]
    if inputother2 !='':
        wo.OTHER2=inputother2
        wui.OTHER2='textfield'
    else:
        wo.OTHER2=[]
        wui.OTHER2=[]
    if inputother3 !='':
        wo.OTHER3=inputother3
        wui.OTHER3='textfield'
    else:
        wo.OTHER3=[]
        wui.OTHER3=[]
    if inputother4 !='':
        wo.OTHER4=inputother4
        wui.OTHER4='textfield'
    else:
        wo.OTHER4=[]
        wui.OTHER4=[]
    wo.save()
    wui.save()
    #chosen=Workouts.objects.get(WONAME=inputname)
    workout=wo
    print workout.WONAME
    context={'workout': workout, 'userid':username, 'goal': goal, 'myphoto':myphoto, 'headertext':headertext, 'footertext':footertext}
    return render(request, 'trainapp/newworkoutupdate.html', context)