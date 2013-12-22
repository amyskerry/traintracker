from django.contrib import admin

# Register your models here.
from django.contrib import admin
from trainapp.models import Metrics, WorkoutEntries

class MetricAdmin(admin.ModelAdmin):
    fields = ['USERID', 'METRIC', 'GRADE', 'DATE', 'OUTDOOR', 'COMMENTS']
    
admin.site.register(Metrics, MetricAdmin)
admin.site.register(WorkoutEntries)

