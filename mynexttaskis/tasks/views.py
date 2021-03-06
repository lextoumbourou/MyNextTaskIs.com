from datetime import datetime, timedelta
import json

from django.core.context_processors import csrf
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from lazysignup.decorators import allow_lazy_user

from mynexttaskis.tasks.models import Task, Category
from mynexttaskis.tasks import utils
import mynexttaskis.settings as settings


def request_dispatcher(request, task=None):
    """
    Route to the correct view depending on HTTP method
    """
    # GET - /api/task/ - Return all tasks 
    if (request.method == 'GET') and (task is None):
        return get_tasks(request)
    # GET - /api/task/playing - Return playing task
    elif (request.method == 'GET') and (task == 'playing'):
        return get_active_task(request)
    # GET - /api/task/category?categories=Blah,Test,Moo
    # Return tasks that match categories
    elif (request.method == 'GET') and (task == 'category'):
        return get_tasks_by_category(request)
    # POST - /api/task/<int> - Update task and return all tasks
    elif (request.method == 'POST') and (task is not None) and task.isdigit():
        return update_task(request, task)
    # POST - /api/task or /api/task/new - Create new task and return task
    elif (request.method == 'POST') and ((task is None) or (task == 'new')):
        return create_task(request)
    # DELETE - /api/task/<int> - Delete a task and return all tasks
    elif (request.method == 'DELETE') and (task is not None) and task.isdigit():
        return delete_task(request, task)


@allow_lazy_user
def get_tasks_by_category(request):
    """
    Get tasks by category
    """
    tasks = []
    if 'categories' in request.GET:
        categories = request.GET['categories'].split(',')
        tasks = Task.objects.filter(
            user=request.user, categories__name__in=categories)

    return HttpResponse(serializers.serialize('json', tasks))

@allow_lazy_user
def create_task(request):
    """Create a new task and return json data for the task"""
    json_data = json.loads(request.raw_post_data)
    if 'task' in json_data:
        task_string = json_data['task']
        categories = utils.get_categories(task_string)
        task = Task.objects.create(
            user=request.user, task=task_string,
            is_complete=False, created=datetime.today())
        task.save()
        for category in categories:
            # Add category if it doesn't exist
            obj, created = Category.objects.get_or_create(name=category)
            task.categories.add(obj)

    return HttpResponse(serializers.serialize('json', [task])) 


@allow_lazy_user
def delete_task(request, task):
    """Delete a task if it exists"""
    try:
        task = Task.objects.get(pk=task)
    except Task.DoesNotExist:
        return Http404
    if task.user == request.user:
        task.delete()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=401)


@allow_lazy_user
def get_active_task(request):
    """Return single active task as JSON"""
    task = Task.objects.filter(user=request.user, is_complete=False, is_in_progress=True)
    return HttpResponse(serializers.serialize('json', task)) 


@allow_lazy_user
def get_tasks(request):
    """Retrieve the requested day's tasks (default today)
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
def update_task(request, task):
    """Get or create the tasks for a day then return 
    the current tasks as Json
    """
    date = get_date(request)
    user = request.user
    task = Task.objects.get(pk=task)
    categories = []

    if task.user != user:
        return HttpResponse(status=401) 

    json_data = json.loads(request.raw_post_data)
    if 'task' in json_data:
        task.task = json_data['task']
        categories = utils.get_categories(json_data['task'])
    if 'is_complete' in json_data:
        task.is_complete = json_data['is_complete']
    if 'is_paused' in json_data:
        task.is_paused = json_data['is_paused']
    if 'is_in_progress' in json_data:
        task.is_in_progress = json_data['is_in_progress']
    if 'time_taken' in json_data:
        task.time_taken = json_data['time_taken']
    if 'start_time' in json_data and json_data['start_time']:
        task.start_time = datetime.fromtimestamp(
            int(json_data['start_time']) / 1000)
    if 'end_time' in json_data and json_data['end_time']:
        task.end_time = datetime.fromtimestamp(
            int(json_data['end_time']) / 1000)

    task.save()

    for category in categories:
        # Add category if it doesn't exist
        obj, created = Category.objects.get_or_create(name=category)
        task.categories.add(obj)

    data = serializers.serialize('json', [task])
    return HttpResponse(data)


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
