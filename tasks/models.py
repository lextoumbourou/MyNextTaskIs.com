from django.db import models
from django.contrib import admin

class Task(models.Model):
    task = models.CharField(max_length=200)
    is_complete = models.BooleanField()
    created = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.task

class TaskAdmin(admin.ModelAdmin):
    pass

admin.site.register(Task, TaskAdmin)


