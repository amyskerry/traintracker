from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import datetime

from trainapp.models import Metrics, WorkoutEntries, TempVals, Workouts, WorkoutUIs

def index(request):
    title='TrainTracker'
    context = {'pagetitle': title}
    return render(request, 'trainapp/index.html', context)
def updated(request, username):
    output="all up to date"
    return HttpResponse(output)
def homepage(request):
    try:
        user=request.POST['green']            
        datevar=datetime.datetime.now()
        date=datevar.strftime("%Y-%m-%d %H:%M")
        p=TempVals(USERID=user, DATE=date)
        p.save()
    except:
        pass
    metricreports = Metrics.objects.order_by('USERID')[:5]
    template = loader.get_template('trainapp/choose.html')
    context = RequestContext(request, {
        'metricreports': metricreports, 'userid':p.USERID
    })
    return HttpResponse(template.render(context))
    
def chooseworkout(request, username):
    context={'userid': username}
    # get wo possibilities
    workouts=Workouts.objects.all()
    context['wooptions']=[workout.WONAME for workout in workouts]
    return render(request, 'trainapp/chooseworkout.html', context)
def dataentry(request, username):
    wk=request.POST['wochoice'] # find user choice
    # get parameters and ui specs for that workout
    workout = get_object_or_404(Workouts, WONAME=wk)
    workoutUI = get_object_or_404(WorkoutUIs, WONAME=wk)
    propobjs=workout._meta.fields
    propnames=[prop.name for prop in propobjs]
    WOTIME_FORM=workoutUI.WOTIME[0]
    context={'userid': username, 'workout':workout, 'workoutui':workoutUI, 'propnames': propnames, 'workouttimes':[30,60,90], 'WOTIME_FORM'=WOTIME_FORM}
    # still want to provide wo possibilities
    workouts=Workouts.objects.all()
    context['wooptions']=[workout.WONAME for workout in workouts]
    return render(request, 'trainapp/dataentry.html', context)
    
def metrics(request,username):
    return HttpResponse("update your metrics here %s..")
def viewdata(request):
    return HttpResponse("see your data")