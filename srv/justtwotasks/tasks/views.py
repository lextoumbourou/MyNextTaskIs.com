from datetime import datetime, timedelta

from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from lazysignup.decorators import allow_lazy_user

from justtwotasks.tasks.models import Task

MAX_TASKS = 2

@allow_lazy_user
def main(request):
    """Collects todays tasks and return template to display to user"""
    task_to_edit = None;

    # Determine if we need to edit tasks
    if 'edit_task' in request.GET:
        task_to_edit = int(request.GET['edit_task'])

    date = get_date(request)
    slogan = get_slogan(date)

    # Get date strings for displaying the backwards and forwards buttons
    today = datetime.today()
    yesterday = date - timedelta(days=1) 
    tomorrow = date + timedelta(days=1)

    user = request.user

    print "Yesterday is "+str(yesterday.date())
    print "Date is "+str(date.date())

    # Get all of today's tasks
    tasks = Task.objects.filter(user=user,
                                created__year=date.year,
                                created__month=date.month,
                                created__day=date.day).order_by('id')

    tasks_to_create = range(1, (MAX_TASKS - len(list(tasks)))+1)

    args = {'tasks':tasks,
            'task_to_edit':task_to_edit,
            'tasks_to_create':tasks_to_create,
            'today':today,
            'tomorrow':tomorrow,
            'yesterday':yesterday,
            'is_today':is_today(date),
            'slogan':slogan,}

    return render_to_response('tasks.html', 
                              args,
                              context_instance=RequestContext(request))


@allow_lazy_user
def add_tasks(request):
    """Take an array of tasks and add to the database, if a task_id is
    provided, will update existing task. Redirects home when finished.

    """
    date = get_date(request)

    if request.method == 'POST' and 'tasks[]' in request.POST:
        tasks = request.POST.getlist('tasks[]')
        user = request.user
        if 'task_ids[]' in request.POST:
            task_ids = request.POST.getlist('task_ids[]')

        # Ensure we only have no more than the max tasks processed
        tasks = tasks[:MAX_TASKS]

        for i in enumerate(tasks):
            key = i[0]
            # If we've set the key, we're updating an existing task
            if int(task_ids[key]):
                task = Task.objects.get(user=user, pk=int(task_ids[key]))
                task.task = tasks[key]
                task.save()
            # Otherwise, it's brand new
            else:
                Task.objects.create(user=user, task=tasks[key], is_complete=False)

    return HttpResponseRedirect("/")


@allow_lazy_user
def delete_task(request):
    """Delete a single task, if it exists then redirect user home"""
    if request.method == 'GET' and 'task' in request.GET:
        user = request.user
        task = Task.objects.get(user=user, pk=int(request.GET['task']))
        task.delete()

    return HttpResponseRedirect("/")


@allow_lazy_user
def complete_task(request):
    """Set a task to the opposite completion status to what it current is
    eg if it's False, make it True. Then, redirect home

    """
    if request.method == 'GET' and 'task' in request.GET:
        user = request.user
        task = Task.objects.get(user=user, pk=int(request.GET['task']))
        if task.is_complete:
            task.is_complete = False
        else:
            task.is_complete = True
        task.save()

    return HttpResponseRedirect("/")


def get_date(request):
    """Return a requested date or today"""
    # Initialise key variables with sensible defaults
    today = datetime.today()
    date = today 

    if request.method == 'GET':
        # Determine what day's tasks to display
        if 'date' in request.GET:
            print "Here I am!"
            date = datetime.strptime(request.GET['date'], '%Y%m%d')

    return date


def get_slogan(date):
    """Build the slogan based on the date"""
    today = datetime.today()
    yesterday = today - timedelta(days=1) 
    the_day_before = yesterday - timedelta(days=1) 

    slogan = "What two things {0} you accomplish {1}?"

    if date.date() == today.date():
        slogan = slogan.format("will", "today")
    elif date.date() == yesterday.date():
        slogan = slogan.format("did", "yesterday")
    elif date.date() == the_day_before.date():
        slogan = slogan.format("did", "the day before")
    else:
        slogan = slogan.format("did", "on the "+str(date.date()))

    return slogan

def is_today(date):
    """Return true if the requested date is today"""
    is_today = False
    if date.date() == datetime.today().date():
        is_today = True

    return is_today 



