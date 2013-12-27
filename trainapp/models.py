from django.db import models

othermax=30

# Create your models here.

class Usernames(models.Model):
    USERID = models.CharField(max_length=30)
    GOAL=models.CharField(max_length=150)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.USERID

class PossMetrics(models.Model):
    METRIC = models.CharField(max_length=30)
    GRADERANGE=models.CharField(max_length=300)
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.METRIC
        
class Metrics(models.Model):
    METRIC = models.CharField(max_length=30)
    GRADE = models.CharField(max_length=15)
    USERID=  models.CharField(max_length=30)
    DATE=models.CharField(max_length=30)
    OUTDOOR = models.BooleanField()
    COMMENTS= models.TextField()
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.METRIC

class WorkoutEntries(models.Model):
    WONAME = models.CharField(max_length=30)
    USERID=  models.CharField(max_length=30)
    OUTDOOR = models.BooleanField()
    WOTIME = models.IntegerField()
    WOREPS=  models.IntegerField()
    WOCYCLES=  models.IntegerField()
    WOMAXAVG = models.CharField(max_length=5)
    CLEANS=  models.IntegerField()
    COMMENTS= models.TextField()
    OTHER1= models.CharField(max_length=othermax)
    OTHER2= models.CharField(max_length=othermax)
    OTHER3= models.CharField(max_length=othermax)
    OTHER4= models.CharField(max_length=othermax)
    DATE=models.CharField(max_length=30)
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.WONAME
        
class Workouts(models.Model):
    WONAME = models.CharField(max_length=30)
    OUTDOOR = models.CharField(max_length=30)
    WOTIME = models.CharField(max_length=30)
    WOREPS=  models.CharField(max_length=30)
    WOCYCLES=  models.CharField(max_length=30)
    WOMAXAVG = models.CharField(max_length=30)
    CLEANS=  models.CharField(max_length=30)
    COMMENTS= models.CharField(max_length=30)
    OTHER1= models.CharField(max_length=30)
    OTHER2= models.CharField(max_length=30)
    OTHER3= models.CharField(max_length=30)
    OTHER4= models.CharField(max_length=30)
    METRIC = models.CharField(max_length=30)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.WONAME
    
#    WOs.append({'WONAME':'boulder', 'INDOUT':'outdoor?', 'WOTIME':'time', 'WOREPS': 'reps at max', 'WOCYCLES': [], 'WOMAXAVGRANGE': 'max grade', 'CLEANS':'clean at max', 'METRIC':'boulder (send)', 'OTHER1':[], 'OTHER2':[], 'OTHER3':[], 'OTHER4':[], 'COMMENTS': 'comments'})
#wo2=Workouts(WONAME='boulder', INDOUT='outdoor?',WOTIME='time', WOREPS= 'reps at max', WOCYCLES= [], WOMAXAVG= 'max grade', CLEANS='clean at max', METRIC='boulder (clean)', OTHER1=[], OTHER2=[], OTHER3=[], OTHER4=[], COMMENTS= 'comments')
    
class WorkoutUIs(models.Model): 
    WONAME = models.CharField(max_length=30)
    WOTIME = models.CharField(max_length=30)
    WOREPS=  models.CharField(max_length=30)
    WOCYCLES=  models.CharField(max_length=30)
    WOMAXAVG = models.CharField(max_length=30)
    CLEANS=  models.CharField(max_length=30)
    COMMENTS= models.CharField(max_length=30)
    OTHER1= models.CharField(max_length=30)
    OTHER2= models.CharField(max_length=30)
    OTHER3= models.CharField(max_length=30)
    OTHER4= models.CharField(max_length=30)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.WONAME

    
#defaultUIs={'WONAME':[], 'INDOUT':['radio',['indoor', 'outdoor']], 'WOTIME':['scroll',timerange], 'WOREPS': ['scroll', reprange], 'WOCYCLES': ['scroll', cyclerange], 'WOMAXAVGRANGE': ['textfield'], 'CLEANS':['textfield'], 'OTHER1':[], 'OTHER2':[], 'OTHER3':[], 'OTHER4':[], 'COMMENTS': ['textbox']}
#wui2=WorkoutUIs(WONAME='TR', INDOUT=['radio',['indoor', 'outdoor']], WOTIME=['select',timerange], WOREPS= ['select', reprange], WOCYCLES= ['select', cyclerange], WOMAXAVG= ['textfield'], CLEANS=['textfield'], OTHER1=[], OTHER2=[], OTHER3=[], OTHER4=[], COMMENTS= ['textbox'])    
    
    