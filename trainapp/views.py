from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import datetime, time

from trainapp.models import Metrics, WorkoutEntries, Usernames, Workouts, WorkoutUIs, PossMetrics
from trainapp.analyzefunctions import *

global routerange, boulderrange
routerange=[]
for x in range(5,15):
    for l in ['a','b','c','d']:
        routerange.append('5.'+str(x)+l)
boulderrange=['v'+str(x) for x in range(0,14)]
 
def index(request):
    title='TrainTracker'
    stored_users=Usernames.objects.all()
    print stored_users
    try:
        usernames=[induser.USERID for induser in stored_users]
    except:
        usernames=[]
    context = {'pagetitle': title, 'usernames': usernames}
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
    print myphoto
    metricreports = Metrics.objects.order_by('USERID')[:5]
    template = loader.get_template('trainapp/choose.html')
    context ={'metricreports': metricreports, 'userid':username, 'goal': goal, 'myphoto':myphoto}
    #return HttpResponse(template.render(context))
    return render(request, 'trainapp/choose.html', context)
    
def chooseworkout(request, username):
    u=Usernames.objects.get(USERID=username)
    goal=u.GOAL           
    myphoto='trainapp/'+username+'.jpg'
    context={'userid': username, 'goal': goal, 'myphoto':myphoto}
    # get wo possibilities
    workouts=Workouts.objects.all()
    context['wooptions']=[workout.WONAME for workout in workouts]
    return render(request, 'trainapp/chooseworkout.html', context)
def choosemetric(request, username):
    u=Usernames.objects.get(USERID=username)
    goal=u.GOAL           
    myphoto='trainapp/'+username+'.jpg'
    # get wo possibilities
    metrics=PossMetrics.objects.all()
    context={'userid': username, 'metricoptions':[metric.METRIC for metric in metrics], 'goal': goal, 'myphoto':myphoto}
    return render(request, 'trainapp/choosemetric.html', context)
def dataentry(request, username):
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
    context={'userid': username, 'workout':workout, 'workoutui':workoutUI, 'propnames': propnames, 'workouttimes':workouttimes,'workoutreps':workoutreps,'workoutcycles':workoutcycles,'workoutgrades':workoutgrades, 'goal': goal, 'myphoto':myphoto}
    # still want to provide wo possibilities
    workouts=Workouts.objects.all()
    context['wooptions']=[workout.WONAME for workout in workouts]
    return render(request, 'trainapp/dataentry.html', context)
    
def updated(request, username):
    u=Usernames.objects.get(USERID=username)
    goal=u.GOAL           
    myphoto='trainapp/'+username+'.jpg'
    wk=request.POST['WONAME'].encode('ascii','ignore')
    entry=WorkoutEntries(WONAME=wk)
    #set default
    entry.WOTIME=0
    entry.INDOUT=0
    entry.WOREPS=0
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
        entry.INDOUT=request.POST['INDOUT'].encode('ascii','ignore')
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
        print entry.COMMENTS
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
    datevar=time.strftime("%Y-%m-%d")
    entry.DATE=datevar
    workout = get_object_or_404(Workouts, WONAME=wk)
    propobjs=workout._meta.fields
    propnames=[prop.name for prop in propobjs]
    context={'propnames':propnames, 'entry':entry, 'workout': workout, 'userid':username, 'goal': goal, 'myphoto':myphoto}
    entry.save()
    metric=workout.METRIC
    if metric:
        for x in range(entry.CLEANS):
            m=Metrics(METRIC=metric, GRADE=entry.WOMAXAVG, DATE=datevar.strftime("%Y-%m-%d"), USERID=username, OUTDOOR=entry.INDOUT)
            m.save()
    #should add optional metric save here as well
    return render(request, 'trainapp/updated.html', context)
def metrics(request, username):
    u=Usernames.objects.get(USERID=username)
    goal=u.GOAL           
    myphoto='trainapp/'+username+'.jpg'
    metric=request.POST['METRIC'].encode('ascii','ignore')
    print metric
    metricinfo=PossMetrics.objects.get(METRIC=metric)
    graderange=metricinfo.GRADERANGE[1:-1].replace("'","").replace("[","").replace("]","").split(",")
    metricvals=Metrics._meta.fields
    metricnames=[mval.name for mval in metricvals]
    metrics=PossMetrics.objects.all()
    metricoptions=[thism.METRIC for thism in metrics]
    context={'userid': username, 'fieldnames':metricnames, 'metric': metric, 'metricoptions': metricoptions, 'graderange':graderange, 'goal': goal, 'myphoto':myphoto}
    return render(request, 'trainapp/metrics.html', context)
def report(request,username):
    u=Usernames.objects.get(USERID=username)
    goal=u.GOAL           
    myphoto='trainapp/'+username+'.jpg'
    metric=request.POST['METRIC'].encode('ascii','ignore')
    print metric
    mentry=Metrics(METRIC=metric)
    datevar=time.strftime("%Y-%m-%d")
    mentry.DATE=datevar
    mentry.USERID=username
    mentry.GRADE=''
    try:
        mentry.GRADE=request.POST['GRADE'].encode('ascii','ignore')
    except:
        pass
    mentry.OUTDOOR=0
    try:
        mentry.OUTDOOR=request.POST['OUTDOOR'].encode('ascii','ignore')
    except:
        pass
    mentry.COMMENTS=''
    try:
        mentry.COMMENTS=request.POST['COMMENTS'].encode('ascii','ignore')
    except:
        pass
    mentry.save()
    metricvals=Metrics._meta.fields
    metricnames=[mval.name for mval in metricvals]
    context={'userid': username, 'fieldnames':metricnames, 'mentry':mentry, 'goal': goal, 'myphoto':myphoto}
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
    context={'userid': username, 'pmnames':pmnames, 'wonames':wonames, 'allnames': allnames, 'goal': goal, 'myphoto':myphoto}
    return render(request, 'trainapp/choosedata.html', context)
def viewdata(request, username):
    u=Usernames.objects.get(USERID=username)
    goal=u.GOAL           
    myphoto='trainapp/'+username+'.jpg'
    datachoices=request.POST.getlist('data')
    allchoices=sortdata(datachoices)
    #temp hack until can flexibly deal with multiple metrics
    bins=[]
    binneddata=[]
    counts=[]    
    if allchoices:
        print allchoices[0].name
        bins=allchoices[0].bins
        binneddata=allchoices[0].binneddata
        counts=allchoices[0].counts
    print bins
    context={'userid': username,'datachoices':datachoices, 'bins':bins, 'binneddata': binneddata, 'counts':counts, 'goal': goal, 'myphoto':myphoto}
    return render(request, 'trainapp/viewdata.html', context)
        