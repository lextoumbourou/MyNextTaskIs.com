from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User)
    task = models.CharField(max_length=200)
    is_complete = models.BooleanField()
    created = models.DateField()
    time_taken = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.task

class TaskAdmin(admin.ModelAdmin):
    pass

admin.site.register(Task, TaskAdmin)

