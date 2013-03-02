from datetime import datetime, timedelta
import json

from django.core.context_processors import csrf
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from lazysignup.decorators import allow_lazy_user

from justtwotasks.tasks.models import Task
import justtwotasks.settings as settings


@allow_lazy_user
def request_dispatcher(request, task=None):
    """
    Route to the correct view depending on HTTP method
    """
    if (request.method == 'DELETE') and (task is not None):
        return delete_task(request, task)


@allow_lazy_user
def delete_task(result, task):
    """
    Delete a task if it exists
    """
    try:
        task = Task.objects.get(pk=task)
    except Task.DoesNotExist:
        return Http404
    task.delete()
    return HttpResponse(status=200)


@allow_lazy_user
def main(request):
    """Collect todays tasks and return template to display to user"""
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
    
    # Get all of today's tasks, since only 1 will be incomplete, 
    # we'll know it'll be the first one
    tasks = Task.objects.filter(
        user=user, created=date.date()).order_by('is_complete', 'id')

    data = serializers.serialize('json', tasks)
    return HttpResponse(data)


@allow_lazy_user
def update_task(request):
    """
    Get or create the tasks for a day then return 
    the current tasks as Json
    """
    date = get_date(request)
    user = request.user
    if request.method == 'POST':
        json_data = json.loads(request.raw_post_data)
        if 'task' in json_data:
            if 'pk' in json_data and int(json_data['pk']) != 0:
                task = Task.objects.get(user=user, pk=json_data['pk'])
                task.task = json_data['task']
                task.is_complete = json_data['is_complete']
                task.save()
            # Otherwise, it's brand new
            else:
                Task.objects.create(
                    user=user, task=json_data['task'], 
                    created=date, is_complete=False)

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

    slogan = "{0} completed tasks"

    if date.date() == today.date():
        slogan = slogan.format("Today's")
    elif date.date() == yesterday.date():
        slogan = slogan.format("Yesterday's")
    elif date.date() == the_day_before.date():
        slogan = slogan.format("The day before's")
    else:
        slogan = slogan.format("The "+str(date.date())+"'s")

    return slogan


def is_today(date):
    """Return true if the requested date is today"""
    is_today = False
    if date.date() == datetime.today().date():
        is_today = True

    return is_today 
