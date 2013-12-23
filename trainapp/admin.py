from django.contrib import admin

# Register your models here.
from django.contrib import admin
from trainapp.models import Metrics, WorkoutEntries, Workouts, WorkoutUIs, Usernames, PossMetrics

class MetricAdmin(admin.ModelAdmin):
    fields = ['USERID', 'METRIC', 'GRADE', 'DATE', 'OUTDOOR', 'COMMENTS']
    
admin.site.register(Metrics, MetricAdmin)
admin.site.register(WorkoutEntries)
admin.site.register(Workouts)
admin.site.register(WorkoutUIs)
admin.site.register(Usernames)
admin.site.register(PossMetrics)

