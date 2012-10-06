from datetime import datetime, timedelta

from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from justtwotasks.tasks.models import Task

MAX_TASKS = 2

def main(request):
    """Collects todays tasks and return template to display to user"""
    # Initialise key variables with sensible defaults
    today = datetime.today()
    date = today 
    task_to_edit = None;

    if request.method == 'GET':
        # Determine what day's tasks to display
        if 'date' in request.GET:
            date = datetime.strptime(request.GET['date'], '%Y%m%d')

        # Determine if we need to edit tasks
        if 'edit_task' in request.GET:
            task_to_edit = int(request.GET['edit_task'])

    # Get date strings for displaying the backwards and forwards buttons
    yesterday = date - timedelta(days=1) 
    tomorrow = date + timedelta(days=1)

    # Get all of today's tasks
    tasks = Task.objects.filter(created__year=date.year,
                                created__month=date.month,
                                created__day=date.day).order_by('id')

    tasks_to_create = range(1, (MAX_TASKS - len(list(tasks)))+1)

    args = {'tasks':tasks,
            'task_to_edit':task_to_edit,
            'tasks_to_create':tasks_to_create,
            'today':today,
            'tomorrow':tomorrow,
            'yesterday':yesterday,
            'date_to_view':date}

    return render_to_response('tasks.html', 
                              args,
                              context_instance=RequestContext(request))

def add_tasks(request):
    """Take an array of tasks and add to the database, if a task_id is
    provided, will update existing task. Redirects home when finished.

    """
    if request.method == 'POST' and 'tasks[]' in request.POST:
        tasks = request.POST.getlist('tasks[]')
        if 'task_ids[]' in request.POST:
            task_ids = request.POST.getlist('task_ids[]')

        # Ensure we only have no more than the max tasks processed
        tasks = tasks[:MAX_TASKS]

        for i in enumerate(tasks):
            key = i[0]
            # If we've set the key, we're updating an existing task
            if int(task_ids[key]):
                task = Task.objects.get(pk=int(task_ids[key]))
                task.task = tasks[key]
                task.save()
            # Otherwise, it's brand new
            else:
                Task.objects.create(task=tasks[key], is_complete=False)

    return HttpResponseRedirect("/")

def delete_task(request):
    """Delete a single task, if it exists then redirect user home"""
    if request.method == 'GET' and 'task' in request.GET:
        task = Task.objects.get(pk=int(request.GET['task']))
        task.delete()

    return HttpResponseRedirect("/")

def complete_task(request):
    """Set a task to the opposite completion status to what it current is
    eg if it's False, make it True. Then, redirect home

    """
    if request.method == 'GET' and 'task' in request.GET:
        task = Task.objects.get(pk=int(request.GET['task']))
        if task.is_complete:
            task.is_complete = False
        else:
            task.is_complete = True
        task.save()

    return HttpResponseRedirect("/")


