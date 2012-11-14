from datetime import datetime, timedelta
import json

from django.core.context_processors import csrf
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from lazysignup.decorators import allow_lazy_user

from justtwotasks.tasks.models import Task
import justtwotasks.settings as settings

MAX_TASKS = 2

@allow_lazy_user
def main(request):
    """Collects todays tasks and return template to display to user"""
    date = get_date(request)
    slogan = get_slogan(date)

    # Get date strings for displaying the backwards and forwards buttons
    today = datetime.today()
    yesterday = date - timedelta(days=1) 
    tomorrow = date + timedelta(days=1)

    user = request.user

    args = {'date':date,
            'today':today,
            'tomorrow':tomorrow,
            'yesterday':yesterday,
            'is_today':is_today(date),
            'slogan':slogan,
            'debug':settings.TEMPLATE_DEBUG}

    return render_to_response('tasks.html', 
                              args,
                              context_instance=RequestContext(request))

@allow_lazy_user
def get_tasks(request):
    """
    Retrieve the requested day's tasks (default today)
    and return result as Json
    """
    date = get_date(request)
    user = request.user

    # Get all of today's tasks
    tasks = Task.objects.filter(user=user,
                                created=date.date()).order_by('id')[:MAX_TASKS]

    data = serializers.serialize('json', tasks)
    return HttpResponse(data)


@allow_lazy_user
def update_tasks(request):
    """
    Get or create the tasks for a day then return 
    the current tasks as Json
    """
    date = get_date(request)
    user = request.user
    if request.method == 'POST':
        json_data = json.loads(request.raw_post_data)
        if 'tasks' in json_data:
            for t in json_data['tasks']:
                # If we've set the key, we're updating an existing task
                if int(t['pk']) > 0:
                    task = Task.objects.get(user=user, pk=t['pk'])
                    task.task = t['task']
                    task.is_complete = t['is_complete']
                    task.save()
                # Otherwise, it's brand new
                else:
                    Task.objects.create(user=user, 
                                        task=t['task'], 
                                        created=date,
                                        is_complete=False)

    return get_tasks(request)


def get_date(request):
    """Return a requested date or today"""
    # Initialise key variables with sensible defaults
    today = datetime.today()
    date = today 
    # Determine what day's tasks to display
    if 'date' in request.GET:
        try:
            date = datetime.strptime(request.GET['date'], '%Y%m%d')
        except ValueError:
            pass

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

