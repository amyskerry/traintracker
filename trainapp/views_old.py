from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import datetime

from trainapp.models import Metrics, WorkoutEntries, TempVals, Workouts, WorkoutUIs

def index(request):
    title='TrainTracker'
    context = {'pagetitle': title,}
    return render(request, 'trainapp/index.html', context)
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
def redirect(request,username):
    nextstep=request.POST['choice']
    username=request.POST['userid']
    if nextstep=="enter workout":
        HttpResponse= dataentry(request,username)
    else:
        HttpResponse=metrics(request,username)
    return HttpResponse
def dataentry(request, username):
    return HttpResponse("add a data entry %s." % username)
def metrics(request,username):
    return HttpResponse("update your metrics here %s..")
def viewdata(request):
    return HttpResponse("see your data")